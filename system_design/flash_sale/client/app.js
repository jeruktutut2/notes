const FLASH_SALE_ID = "44444444-4444-4444-4444-444444444444";
let currentPayOrderId = null;

document.addEventListener("DOMContentLoaded", () => {
    loadFlashSaleDetail();
    loadOrders();
    loadEvents();

    setInterval(loadFlashSaleDetail, 3000);
    setInterval(loadOrders, 4000);
});

function getSelectedUserId() {
    return document.getElementById("userSelector").value;
}

async function loadFlashSaleDetail() {
    try {
        const res = await fetch(`/api/v1/flash-sales/${FLASH_SALE_ID}`);
        if (!res.ok) return;
        const data = await res.json();

        document.getElementById("remainingStock").innerText = data.remaining_stock;
        document.getElementById("originalStock").innerText = data.original_stock;
        
        const badge = document.getElementById("saleStatusBadge");
        badge.innerText = data.status;
        if (data.status === "ACTIVE") {
            badge.className = "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs px-3 py-1 rounded-full font-mono font-semibold";
        } else if (data.status === "SOLD_OUT") {
            badge.className = "bg-rose-500/10 text-rose-400 border border-rose-500/20 text-xs px-3 py-1 rounded-full font-mono font-semibold";
        }

        const pct = (data.remaining_stock / data.original_stock) * 100;
        const bar = document.getElementById("stockProgressBar");
        bar.style.width = `${pct}%`;
        if (data.remaining_stock === 0) {
            bar.className = "bg-rose-600 h-full w-full transition-all duration-500";
        } else {
            bar.className = "bg-gradient-to-r from-brand-600 to-amber-500 h-full w-full transition-all duration-500";
        }
    } catch (e) {
        console.error("Error loading flash sale detail:", e);
    }
}

async function attemptPurchase() {
    const userId = getSelectedUserId();
    const buyBtn = document.getElementById("buyBtn");
    buyBtn.disabled = true;
    buyBtn.classList.add("opacity-50");

    try {
        const res = await fetch(`/api/v1/flash-sales/${FLASH_SALE_ID}/purchase`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-User-ID": userId,
                "X-Idempotency-Key": `idemp_${userId}_${Date.now()}`
            },
            body: JSON.stringify({ user_id: userId })
        });

        const result = await res.json();

        if (res.status === 202) {
            alert(`✅ PURCHAES ACCEPTED!\nOrder ID: ${result.data.order_id}\nRemaining stock: ${result.data.remaining_stock}`);
            pushSystemNotification(userId, "ORDER_REQUESTED", `Purchase request accepted. Order ID: ${result.data.order_id}`);
            setTimeout(loadOrders, 1000);
        } else if (res.status === 410) {
            alert("❌ SOLD OUT! Stock has been depleted.");
            pushSystemNotification(userId, "SOLD_OUT", "Purchase failed: Stock sold out!");
        } else if (res.status === 409) {
            alert("⚠️ ALREADY PURCHASED! User limit reached.");
            pushSystemNotification(userId, "ALREADY_PURCHASED", "Purchase rejected: User already bought this item.");
        } else {
            alert(`Error: ${result.error?.message || "Purchase failed"}`);
        }

        loadFlashSaleDetail();
    } catch (e) {
        alert("Network or Gateway error: " + e.message);
    } finally {
        buyBtn.disabled = false;
        buyBtn.classList.remove("opacity-50");
    }
}

async function preheatStock() {
    try {
        const res = await fetch(`/api/v1/flash-sales/${FLASH_SALE_ID}/preheat`, { method: "POST" });
        const result = await res.json();
        alert(`🔄 Stock Pre-heated!\nMessage: ${result.message}\nStock: ${result.stock_loaded}`);
        pushSystemNotification(getSelectedUserId(), "STOCK_PREHEATED", `Stock pre-heated to ${result.stock_loaded} units.`);
        loadFlashSaleDetail();
        loadOrders();
    } catch (e) {
        alert("Preheat error: " + e.message);
    }
}

async function checkReconciliation() {
    try {
        const res = await fetch(`/api/v1/inventory/reconcile?flash_sale_id=${FLASH_SALE_ID}`, { method: "POST" });
        const result = await res.json();
        alert(`🦀 RUST RECONCILIATION RESULT:\nStatus: ${result.message}\nRedis Stock: ${result.redis_stock}\nDB Orders: ${result.db_orders}\nOriginal: ${result.original_stock}`);
    } catch (e) {
        alert("Reconciliation error: " + e.message);
    }
}

async function loadOrders() {
    try {
        const res = await fetch("/api/v1/orders");
        if (!res.ok) return;
        const orders = await res.json();

        const tbody = document.getElementById("ordersTableBody");
        if (!orders || orders.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5" class="p-4 text-center text-slate-500">No orders found in PostgreSQL database.</td></tr>`;
            return;
        }

        tbody.innerHTML = orders.map(o => {
            let statusColor = "text-amber-400 bg-amber-400/10 border-amber-400/20";
            if (o.status === "PAID") statusColor = "text-emerald-400 bg-emerald-400/10 border-emerald-400/20";
            if (o.status === "PAYMENT_FAILED" || o.status === "CANCELLED") statusColor = "text-rose-400 bg-rose-400/10 border-rose-400/20";

            const userLabel = o.user_id.startsWith("2222") ? "User 1 (Budi)" : "User 2 (Siti)";
            
            let actionBtn = "-";
            if (o.status === "AWAITING_PAYMENT") {
                actionBtn = `<button onclick="openPaymentModal('${o.id}')" class="bg-brand-600 hover:bg-brand-500 text-white px-2.5 py-1 rounded text-xs transition">Pay Now</button>`;
            }

            return `
                <tr class="hover:bg-slate-800/40">
                    <td class="p-3 font-semibold text-slate-200">${o.id.substring(0, 8)}...</td>
                    <td class="p-3 text-slate-400">${userLabel}</td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded border text-[10px] ${statusColor}">${o.status}</span></td>
                    <td class="p-3 text-slate-300">Rp ${Number(o.price).toLocaleString()}</td>
                    <td class="p-3">${actionBtn}</td>
                </tr>
            `;
        }).join("");
    } catch (e) {
        console.error("Error loading orders:", e);
    }
}

function openPaymentModal(orderId) {
    currentPayOrderId = orderId;
    document.getElementById("modalOrderId").innerText = orderId;
    document.getElementById("paymentModal").classList.remove("hidden");
}

function closePaymentModal() {
    document.getElementById("paymentModal").classList.add("hidden");
    currentPayOrderId = null;
}

async function submitPayment(action) {
    if (!currentPayOrderId) return;

    try {
        const res = await fetch(`/api/v1/payments/pay/${currentPayOrderId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: action, payment_method: "E_WALLET" })
        });
        const result = await res.json();
        
        closePaymentModal();
        alert(`Payment result: ${result.message}`);

        pushSystemNotification(getSelectedUserId(), action === "SUCCESS" ? "PAYMENT_SUCCESS" : "PAYMENT_FAILED", result.message);

        loadOrders();
        loadFlashSaleDetail();
    } catch (e) {
        alert("Payment error: " + e.message);
    }
}

async function loadEvents() {
    try {
        const res = await fetch("/api/v1/notifications/events");
        if (!res.ok) return;
        const events = await res.json();

        const feed = document.getElementById("eventsFeed");
        if (!events || events.length === 0) return;

        feed.innerHTML = events.slice().reverse().map(e => `
            <div class="bg-slate-950 border border-slate-800 p-3 rounded-xl space-y-1 text-xs font-mono">
                <div class="flex justify-between items-center text-slate-400">
                    <span class="text-brand-400 font-bold">${e.event_type}</span>
                    <span>${new Date(e.timestamp).toLocaleTimeString()}</span>
                </div>
                <div class="text-slate-200">${e.message}</div>
            </div>
        `).join("");
    } catch (e) {
        console.error("Error loading notification events:", e);
    }
}

async function pushSystemNotification(userId, eventType, message) {
    try {
        await fetch("/api/v1/notifications/push", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId, event_type: eventType, message: message })
        });
        loadEvents();
    } catch (e) {
        console.error("Error pushing notification:", e);
    }
}
