use axum::{
    extract::Query,
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use std::env;
use std::net::SocketAddr;
use tower_http::cors::CorsLayer;

#[derive(Deserialize)]
struct InventoryQuery {
    flash_sale_id: Option<String>,
}

#[derive(Serialize)]
struct InventoryStatusResponse {
    service: String,
    flash_sale_id: String,
    redis_remaining_stock: i64,
    db_created_orders: i64,
    original_stock: i64,
    status: String,
}

#[derive(Serialize)]
struct ReconciliationResponse {
    service: String,
    flash_sale_id: String,
    redis_stock: i64,
    db_orders: i64,
    total_accounted: i64,
    original_stock: i64,
    is_balanced: bool,
    discrepancy: i64,
    message: String,
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/health", get(health_check))
        .route("/api/v1/inventory/status", get(get_inventory_status))
        .route("/api/v1/inventory/reconcile", post(reconcile_inventory))
        .layer(CorsLayer::permissive());

    let port: u16 = env::var("PORT")
        .unwrap_or_else(|_| "8085".to_string())
        .parse()
        .expect("PORT must be a number");

    let addr = SocketAddr::from(([0, 0, 0, 0], port));
    println!("Rust Inventory Service (Axum) running on {}", addr);
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn health_check() -> Json<serde_json::Value> {
    Json(serde_json::json!({
        "status": "UP",
        "service": "inventory_service",
        "framework": "Axum (Rust)"
    }))
}

async fn get_inventory_status(Query(query): Query<InventoryQuery>) -> Json<InventoryStatusResponse> {
    let sale_id = query.flash_sale_id.unwrap_or_else(|| "44444444-4444-4444-4444-444444444444".to_string());
    
    let db_host = env::var("DB_HOST").unwrap_or_else(|_| "pgbouncer".to_string());
    let db_port = env::var("DB_PORT").unwrap_or_else(|_| "6432".to_string());
    let redis_url = env::var("REDIS_URL").unwrap_or_else(|_| "redis://redis:6379".to_string());

    let mut redis_stock: i64 = -1;
    if let Ok(client) = redis::Client::open(redis_url) {
        if let Ok(mut con) = client.get_tokio_connection().await {
            let key = format!("flash_sale:{}:stock", sale_id);
            let val: Result<i64, _> = redis::cmd("GET").arg(key).query_async(&mut con).await;
            if let Ok(s) = val {
                redis_stock = s;
            }
        }
    }

    let mut db_orders: i64 = 0;
    let mut orig_stock: i64 = 5;
    let mut sale_status = "ACTIVE".to_string();

    let conn_str = format!("host={} port={} user=postgres password=postgres dbname=flash_sale_db", db_host, db_port);
    if let Ok((client, connection)) = tokio_postgres::connect(&conn_str, tokio_postgres::NoTls).await {
        tokio::spawn(async move {
            if let Err(e) = connection.await {
                eprintln!("Postgres connection error: {}", e);
            }
        });

        if let Ok(row) = client.query_one("SELECT original_stock, status FROM flash_sales WHERE id = $1::uuid", &[&sale_id]).await {
            orig_stock = row.get::<_, i32>(0) as i64;
            sale_status = row.get(1);
        }

        if let Ok(row) = client.query_one("SELECT COUNT(*) FROM orders WHERE flash_sale_id = $1::uuid AND status NOT IN ('CANCELLED', 'EXPIRED', 'PAYMENT_FAILED')", &[&sale_id]).await {
            db_orders = row.get::<_, i64>(0);
        }
    }

    Json(InventoryStatusResponse {
        service: "inventory_service (Rust/Axum)".to_string(),
        flash_sale_id: sale_id,
        redis_remaining_stock: redis_stock,
        db_created_orders: db_orders,
        original_stock: orig_stock,
        status: sale_status,
    })
}

async fn reconcile_inventory(Query(query): Query<InventoryQuery>) -> Json<ReconciliationResponse> {
    let sale_id = query.flash_sale_id.unwrap_or_else(|| "44444444-4444-4444-4444-444444444444".to_string());

    let db_host = env::var("DB_HOST").unwrap_or_else(|_| "pgbouncer".to_string());
    let db_port = env::var("DB_PORT").unwrap_or_else(|_| "6432".to_string());
    let redis_url = env::var("REDIS_URL").unwrap_or_else(|_| "redis://redis:6379".to_string());

    let mut redis_stock: i64 = 0;
    if let Ok(client) = redis::Client::open(redis_url) {
        if let Ok(mut con) = client.get_tokio_connection().await {
            let key = format!("flash_sale:{}:stock", sale_id);
            let val: Result<i64, _> = redis::cmd("GET").arg(key).query_async(&mut con).await;
            if let Ok(s) = val {
                redis_stock = s;
            }
        }
    }

    let mut db_orders: i64 = 0;
    let mut orig_stock: i64 = 5;

    let conn_str = format!("host={} port={} user=postgres password=postgres dbname=flash_sale_db", db_host, db_port);
    if let Ok((client, connection)) = tokio_postgres::connect(&conn_str, tokio_postgres::NoTls).await {
        tokio::spawn(async move {
            let _ = connection.await;
        });

        if let Ok(row) = client.query_one("SELECT original_stock FROM flash_sales WHERE id = $1::uuid", &[&sale_id]).await {
            orig_stock = row.get::<_, i32>(0) as i64;
        }

        if let Ok(row) = client.query_one("SELECT COUNT(*) FROM orders WHERE flash_sale_id = $1::uuid AND status NOT IN ('CANCELLED', 'EXPIRED', 'PAYMENT_FAILED')", &[&sale_id]).await {
            db_orders = row.get::<_, i64>(0);
        }
    }

    let total_accounted = redis_stock + db_orders;
    let discrepancy = orig_stock - total_accounted;
    let is_balanced = discrepancy == 0;

    let message = if is_balanced {
        "RECONCILIATION SUCCESSFUL: Zero discrepancy detected between Redis stock and PostgreSQL orders.".to_string()
    } else {
        format!("RECONCILIATION ALERT: Discrepancy of {} units detected!", discrepancy)
    };

    Json(ReconciliationResponse {
        service: "inventory_service (Rust/Axum)".to_string(),
        flash_sale_id: sale_id,
        redis_stock,
        db_orders,
        total_accounted,
        original_stock: orig_stock,
        is_balanced,
        discrepancy,
        message,
    })
}
