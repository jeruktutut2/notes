use std::sync::Arc;

use uuid::Uuid;

use crate::{models::{entities::test1::Test1, requests::{create_request::CreateRequest, delete_request::DeleteRequest, update_request::UpdateRequest}, responses::{create_response::CreateResponse, get_all_response::GetAllResponse, get_by_id_response::GetByIdResponse, response::Response, update_response::UpdateResponse}}, repositories::test1_repository::{Test1Repository, Test1RepositoryImpl}, utils::cockroachdb_util::{CockroachDbUtil, CockroachDbUtilImpl}};

pub trait Test1Service {
    async fn create(&self, create_request: CreateRequest) -> Response<CreateResponse>;
    async fn get_by_id(&self, id: Uuid) -> Response<GetByIdResponse>;
    async fn get_all(&self) -> Response<Vec<GetAllResponse>>;
    async fn update(&self, update_request: UpdateRequest) -> Response<UpdateResponse>;
    async fn delete(&self, delete_request: DeleteRequest) -> Response<()>;
}

pub struct Test1ServiceImpl {
    cockroachdb_util: Arc<CockroachDbUtilImpl>,
    test1_repository: Arc<Test1RepositoryImpl>
}

impl Test1ServiceImpl {
    pub fn new(cockroachdb_util: Arc<CockroachDbUtilImpl>, test1_repository: Arc<Test1RepositoryImpl>) -> Test1ServiceImpl {
        Test1ServiceImpl { 
            cockroachdb_util,
            test1_repository
         }
    }
}

impl Test1Service for Test1ServiceImpl {
    async fn create(&self, create_request: CreateRequest) -> Response<CreateResponse> {
        let mut tx = match self.cockroachdb_util.begin().await {
            Ok(tx) => tx,
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response()
            }
        };

        let test1 = Test1 {id: Uuid::now_v7(), test: create_request.test};
        let rows_affected = match self.test1_repository.create(&mut tx, &test1).await {
            Ok(id) => id,
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        };
        if rows_affected != 1 {
            return Response::set_internal_server_error_response();
        }

        match self.cockroachdb_util.commit(tx).await {
            Ok(()) => (),
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        }
        return Response::set_created_response(CreateResponse::set_craeate_response(test1));
    }

    async fn get_by_id(&self, id: Uuid) -> Response<GetByIdResponse> {
        let test1 = match self.test1_repository.get_by_id(self.cockroachdb_util.get_pool().await, id).await {
            Ok(test1) => test1,
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            } 
        };
        return Response::set_ok_response(GetByIdResponse::set_get_by_id_response(test1));
    }

    async fn get_all(&self) -> Response<Vec<GetAllResponse>> {
        let test1s = match self.test1_repository.get_all(self.cockroachdb_util.get_pool().await).await {
            Ok(test1s) => test1s,
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            } 
        };
        return Response::set_ok_response(GetAllResponse::set_get_all_response(test1s));
    }

    async fn update(&self, update_request: UpdateRequest) -> Response<UpdateResponse> {
        let mut tx = match self.cockroachdb_util.begin().await {
            Ok(tx) => tx,
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        };

        let test1 = Test1 {id: update_request.id, test: update_request.test};
        let rows_affected = match self.test1_repository.update(&mut tx, &test1).await {
            Ok(rows_affected) => rows_affected,
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        };

        if rows_affected != 1 {
            return Response::set_internal_server_error_response();
        }

        match self.cockroachdb_util.commit(tx).await {
            Ok(()) => (),
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        }

        return Response::set_ok_response(UpdateResponse::set_update_response(test1))
    }

    async fn delete(&self, delete_request: DeleteRequest) -> Response<()> {
        let mut tx = match self.cockroachdb_util.begin().await {
            Ok(tx) => tx,
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        };
        
        let rows_affected = match self.test1_repository.delete(&mut tx, delete_request.id).await {
            Ok(rows_affected) => rows_affected,
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        };

        if rows_affected != 1 {
            return Response::set_internal_server_error_response();
        }

        match self.cockroachdb_util.commit(tx).await {
            Ok(()) => (),
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        }

        return Response::set_no_content_response()
    }
}