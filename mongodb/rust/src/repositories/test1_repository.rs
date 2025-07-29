use std::sync::Arc;

use mongodb::{bson::{doc, oid::ObjectId}, Collection};

use crate::{models::entities::test1::Test1, utils::mongo_util::{self, MongoUtil, MongoUtilImpl}};

pub trait Test1Repository {
    async fn create(&self, test1: &Test1) -> mongodb::error::Result<ObjectId>;
    async fn get_by_id(&self, id: ObjectId) -> mongodb::error::Result<Option<Test1>>;
    async fn update_by_id(&self, test1: &Test1) -> mongodb::error::Result<u64>;
    async fn delete_by_id(&self, id: ObjectId) -> mongodb::error::Result<u64>;
}

pub struct Test1RepositoryImpl {
    collection: Arc<Collection<Test1>>
}

impl Test1RepositoryImpl {
    pub fn new(collection: Arc<Collection<Test1>>) -> Test1RepositoryImpl {
        Test1RepositoryImpl {
            collection
        }
    }
}

impl Test1Repository for Test1RepositoryImpl {
    async fn create(&self, test1: &Test1) -> mongodb::error::Result<ObjectId> {
        let result = self.collection.insert_one(test1).await?;
        Ok(result.inserted_id.as_object_id().unwrap())
    }

    async fn get_by_id(&self, id: ObjectId) -> mongodb::error::Result<Option<Test1>> {
        self.collection.find_one(doc! {"_id": id}).await
    }

    async fn update_by_id(&self, test1: &Test1) -> mongodb::error::Result<u64> {
        let filter = doc! {"_id": test1.id};
        let update = doc! {
            "$set": {
                "test": &test1.test
            }
        };
        let result = self.collection.update_one(filter, update).await?;
        Ok(result.modified_count)
    }

    async fn delete_by_id(&self, id: ObjectId) -> mongodb::error::Result<u64> {
        let result = self.collection.delete_one(doc! {"_id": id}).await?;
        Ok(result.deleted_count)
    }
}