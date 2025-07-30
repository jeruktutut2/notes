use std::sync::Arc;

use crate::{models::entities::test1::Test1, repositories::test1_repository::{Test1Repository, Test1RepositoryImpl}, utils::postgres_util::{PostgresUtil, PostgresUtilImpl}};

pub trait Test1Service {
    async fn create_without_tx(&self) -> String;
    async fn create_with_tx(&self) -> String;
}

pub struct Test1ServiceImpl {
    postgres_util: Arc<PostgresUtilImpl>,
    test1_repository: Arc<Test1RepositoryImpl>
}

impl Test1ServiceImpl {
    pub fn new(postgres_util: Arc<PostgresUtilImpl>, test1_repository : Arc<Test1RepositoryImpl>) -> Test1ServiceImpl {
        Test1ServiceImpl { 
            postgres_util,
            test1_repository
         }
    }
}

impl Test1Service for Test1ServiceImpl {
    async fn create_without_tx(&self) -> String {
        println!("insert test1 1");
        let mut test1 = Test1 {id: 0, test: "test1 1".to_string()};
        match self.test1_repository.create_without_tx(self.postgres_util.get_pool().await, &test1).await {
            Ok(_) => (),
            Err(err) => {
                println!("error: {}", err);
                return "error".to_string();
            }
        };

        println!("wait test1 1");
        match self.test1_repository.sleep_without_tx(self.postgres_util.get_pool().await).await {
            Ok(_) => (),
            Err(err) => {
                println!("error: {}", err);
                return "error".to_string();
            }
        };

        println!("insert test1 2");
        test1 = Test1 {id: 0, test: "test1 2".to_string()};
        match self.test1_repository.create_without_tx(self.postgres_util.get_pool().await, &test1).await {
            Ok(_) => (),
            Err(err) => {
                println!("error: {}", err);
                return "error".to_string();
            }
        }

        println!("wait test1 2");
        match self.test1_repository.sleep_without_tx(self.postgres_util.get_pool().await).await {
            Ok(_) => (),
            Err(err) => {
                println!("error: {}", err);
                return "error".to_string();
            }
        }

        println!("insert test1 3");
        test1 = Test1 {id: 0, test: "test1 3".to_string()};
        match self.test1_repository.create_without_tx(self.postgres_util.get_pool().await, &test1).await {
            Ok(_) => (),
            Err(err) => {
                println!("error: {}", err);
                return "error".to_string();
            }
        }

        "ok".to_string()
    }

    async fn create_with_tx(&self) -> String {
        let mut tx = match self.postgres_util.begin().await {
            Ok(tx) => tx,
            Err(err) => {
                println!("error: {}", err);
                return "error".to_string();
            }
        };

        println!("insert test1 1");
        let mut test1 = Test1 {id: 0, test: "test1 1".to_string()};
        match self.test1_repository.create_with_tx(&mut tx, &test1).await {
            Ok(_) => (),
            Err(err) => {
                match self.postgres_util.rollback(tx).await {
                    Ok(_) => (),
                    Err(err) => {
                        println!("error: {}", err);
                        return "error".to_string();
                    }
                }
                println!("error: {}", err);
                return "error".to_string();
            }
        };

        println!("wait test1 1");
        match self.test1_repository.sleep_with_tx(&mut tx).await {
            Ok(_) => (),
            Err(err) => {
                println!("error: {}", err);
                match self.postgres_util.rollback(tx).await {
                    Ok(_) => (),
                    Err(err) => {
                        println!("error: {}", err);
                        return "error".to_string();
                    }
                }
                return "error".to_string();
            }
        };

        println!("insert test1 2");
        test1 = Test1 {id: 0, test: "test1 2".to_string()};
        match self.test1_repository.create_with_tx(&mut tx, &test1).await {
            Ok(_) => (),
            Err(err) => {
                println!("error: {}", err);
                match self.postgres_util.rollback(tx).await {
                    Ok(_) => (),
                    Err(err) => {
                        println!("error: {}", err);
                        return "error".to_string();
                    }
                }
                return "error".to_string();
            }
        }

        println!("wait test1 2");
        match self.test1_repository.sleep_with_tx(&mut tx).await {
            Ok(_) => (),
            Err(err) => {
                println!("error: {}", err);
                match self.postgres_util.rollback(tx).await {
                    Ok(_) => (),
                    Err(err) => {
                        println!("error: {}", err);
                        return "error".to_string();
                    }
                }
                return "error".to_string();
            }
        }

        println!("insert test1 3");
        test1 = Test1 {id: 0, test: "test1 3".to_string()};
        match self.test1_repository.create_with_tx(&mut tx, &test1).await {
            Ok(_) => (),
            Err(err) => {
                println!("error: {}", err);
                match self.postgres_util.rollback(tx).await {
                    Ok(_) => (),
                    Err(err) => {
                        println!("error: {}", err);
                        return "error".to_string();
                    }
                }
                return "error".to_string();
            }
        }

        match self.postgres_util.commit(tx).await {
            Ok(_) => (),
            Err(err) => {
                println!("error: {}", err);
                return "error".to_string();
            }
        }

        "ok".to_string()
    }
}