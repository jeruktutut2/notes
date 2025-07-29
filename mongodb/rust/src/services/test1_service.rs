use std::sync::Arc;

use mongodb::bson::oid::ObjectId;

use crate::{models::{entities::test1::Test1, requests::{create_request::CreateRequest, delete_request::DeleteRequest, update_request::UpdateRequest}, responses::{create_response::CreateResponse, get_by_id_response::GetByIdResponse, response::Response, update_response::UpdateResponse}}, repositories::test1_repository::{Test1Repository, Test1RepositoryImpl}};

pub trait Test1Service {
    async fn create(&self, create_request: CreateRequest) -> Response<CreateResponse>;
    async fn get_by_id(&self, id: String) -> Response<GetByIdResponse>;
    async fn update_by_id(&self, update_request: UpdateRequest) -> Response<UpdateResponse>;
    async fn delete_by_id(&self, delete_request: DeleteRequest) -> Response<()>;
}

pub struct Test1ServiceImpl {
    test1_repository: Arc<Test1RepositoryImpl>
}

impl Test1ServiceImpl {
    pub fn new(test1_repository: Arc<Test1RepositoryImpl>) -> Test1ServiceImpl {
        Test1ServiceImpl {
            test1_repository
        }
    }
}

impl Test1Service for Test1ServiceImpl {
    async fn create(&self, create_request: CreateRequest) -> Response<CreateResponse> {
        let test1 = Test1 {id: ObjectId::new(), test: create_request.test};
        if let Err(err) = self.test1_repository.create(&test1).await {
            println!("error: {}", err);
            return Response::set_internal_server_error_response()
        }
        Response::set_created_response(CreateResponse::set_create_response(test1))
    }

    async fn get_by_id(&self, id: String) -> Response<GetByIdResponse> {
        let object_id = match ObjectId::parse_str(&id) {
            Ok(object_id) => object_id,
            Err(err) => {
                println!("error: {}", err);
                return Response::set_internal_server_error_response();
            }
        };
        let test1_option = match self.test1_repository.get_by_id(object_id).await {
            Ok(test1_option) => test1_option,
            Err(err) => {
                println!("error: {}", err);
                return Response::set_internal_server_error_response();
            }
        };

        let test1 = match test1_option {
            Some(test1) => test1,
            None => {
                println!("cannot find tes1 with id: {}", &id);
                return Response::set_not_found_response("cannot find test1 with id: ".to_owned() + &id);
            }
        };
        Response::set_ok_response(GetByIdResponse::set_get_by_id_response(test1))
    }

    async fn update_by_id(&self, update_request: UpdateRequest) -> Response<UpdateResponse> {
        let object_id = match ObjectId::parse_str(update_request.id) {
            Ok(object_id) => object_id,
            Err(err) => {
                println!("error: {}", err);
                return Response::set_internal_server_error_response();
            }
        };
        let test1 = Test1 { id: object_id, test: update_request.test };
        if let Err(err) = self.test1_repository.update_by_id(&test1).await {
            println!("error: {}", err);
            return Response::set_internal_server_error_response();
        }
        Response::set_ok_response(UpdateResponse::set_update_response(test1))
    }

    async fn delete_by_id(&self, delete_request: DeleteRequest) -> Response<()> {
        let object_id = match ObjectId::parse_str(delete_request.id) {
            Ok(object_id) => object_id,
            Err(err) => {
                println!("error: {}", err);
                return Response::set_internal_server_error_response();
            }
        };
        if let Err(err) = self.test1_repository.delete_by_id(object_id).await {
            println!("error: {}", err);
            return Response::set_internal_server_error_response();
        }
        Response::set_no_content_response()
    }
}