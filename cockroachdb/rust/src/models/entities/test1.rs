use sqlx::prelude::FromRow;
use uuid::Uuid;

#[derive(Debug, FromRow)]
pub struct Test1 {
    pub id: Uuid,
    pub test: String
}