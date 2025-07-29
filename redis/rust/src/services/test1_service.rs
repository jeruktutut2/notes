use std::sync::Arc;
use tokio::sync::Mutex;
use uuid::Uuid;
use crate::models::entities::test1::Test1;
use crate::models::requests::create_request::CreateRequest;
use crate::models::requests::delete_request::DeleteRequest;
use crate::models::responses::create_response::CreateResponse;
use crate::models::responses::get_response::GetResponse;
use crate::models::responses::response::Response;
use crate::utils::redis_util::{RedisUtil, RedisUtilImpl};

pub trait Test1Service {
    async fn create(&mut self, create_request: CreateRequest) -> Response<CreateResponse>;
    async fn get(&mut self, key: &str) -> Response<GetResponse>;
    async fn delete(&mut self, delete_request: DeleteRequest) -> Response<()>;
}

pub struct Test1ServiceImpl {
    redis_util: Arc<Mutex<RedisUtilImpl>>
}

impl Test1ServiceImpl {
    pub fn new(redis_util: Arc<Mutex<RedisUtilImpl>>) -> Self {
        Test1ServiceImpl {
            redis_util
        }
    }
}

impl Test1Service for Test1ServiceImpl {
    async fn create(&mut self, create_request: CreateRequest) -> Response<CreateResponse> {
        let test1 = Test1 {id: Uuid::new_v4().to_string(), test: create_request.test};
        let test_string = match serde_json::to_string(&test1) {
            Ok(test_string) => test_string,
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        };
        if let Err(err) = self.redis_util.lock().await.set(test1.id.as_str(), &test_string).await {
            println!("err: {}", err);
            return Response::set_internal_server_error_response();
        };
        Response::set_created_response(CreateResponse::set_create_response(test1))
    }

    async fn get(&mut self, key: &str) -> Response<GetResponse> {
        let test1_string = match self.redis_util.lock().await.get(key).await {
            Ok(Some(test1_string)) => test1_string,
            Ok(None) => {
                return Response::set_not_found_response("cannot find test1 with id: ".to_string() + key)
            }
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        };
        let test1 = match serde_json::from_str::<Test1>(&test1_string) {
            Ok(test1) => test1,
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response()
            }
        };
        Response::set_ok_response(GetResponse::set_get_response(test1))
    }

    async fn delete(&mut self, delete_request: DeleteRequest) -> Response<()> {
        if let Err(err) = self.redis_util.lock().await.del(&delete_request.id).await {
            println!("err: {}", err);
            return Response::set_internal_server_error_response()
        }
        Response::set_no_content_response()
    }
}