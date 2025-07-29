use std::sync::Arc;

use crate::{models::{entities::test1::Test1, requests::{create_request::CreateRequest, delete_request::DeleteRequest, update_request::UpdateRequest}, responses::{create_response::CreateResponse, get_by_id_response::GetByIdResponse, response::Response, update_response::UpdateResponse}}, repositories::postgres_repository::{PostgresRepository, PostgresRepositoryImpl}, utils::postgres_util::{PostgresUtil, PostgresUtilImpl}};

pub trait PostgresService {
    async fn create(&self, create_request: CreateRequest) -> Response<CreateResponse>;
    async fn get_by_id(&self, id: i32) -> Response<GetByIdResponse>;
    async fn update(&self, update_request: UpdateRequest) -> Response<UpdateResponse>;
    async fn delete(&self, delete_request: DeleteRequest) -> Response<()>;
}

pub struct PostgresServiceImpl {
    postgres_util: Arc<PostgresUtilImpl>,
    postgres_respository: Arc<PostgresRepositoryImpl>
}

impl PostgresServiceImpl {
    pub fn new(postgres_util: Arc<PostgresUtilImpl>, postgres_repository: Arc<PostgresRepositoryImpl>) -> PostgresServiceImpl {
        PostgresServiceImpl {
            postgres_util: postgres_util,
            postgres_respository: postgres_repository
        }
    }
}

impl PostgresService for PostgresServiceImpl {
    async fn create(&self, create_request: CreateRequest) -> Response<CreateResponse> {
        let mut tx = match self.postgres_util.begin().await {
            Ok(tx) => tx,
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response()
            }
        };

        // if error happened, tx will out of scope and authomatically call rollback
        let mut test1 = Test1 {id: 0, test: create_request.test};
        let id = match self.postgres_respository.create(&mut tx, &test1).await {
            Ok(id) => id,
            Err(err) => {
                println!("err: {}", err);
                // match self.postgres_util.rollback(tx).await {
                //     Ok(()) => (),
                //     Err(err) => {
                //         println!("err: {}", err)
                //         return Response::set_internal_server_error_response();
                //     }
                // }
                return Response::set_internal_server_error_response();
            }
        };
        test1.id = id;

        match self.postgres_util.commit(tx).await {
            Ok(()) => (),
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        }
        return Response::set_created_response(CreateResponse::set_craeate_response(test1));
    }

    async fn get_by_id(&self, id: i32) -> Response<GetByIdResponse> {
        let test1 = match self.postgres_respository.get_by_id(self.postgres_util.get_pool().await, id).await {
            Ok(test1) => test1,
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            } 
        };
        return Response::set_ok_response(GetByIdResponse::set_get_by_id_response(test1));
    }

    async fn update(&self, update_request: UpdateRequest) -> Response<UpdateResponse> {
        let mut tx = match self.postgres_util.begin().await {
            Ok(tx) => tx,
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        };

        let test1 = Test1 {id: update_request.id, test: update_request.test};
        let rows_affected = match self.postgres_respository.update(&mut tx, &test1).await {
            Ok(rows_affected) => rows_affected,
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        };

        if rows_affected != 1 {
            return Response::set_internal_server_error_response();
        }

        match self.postgres_util.commit(tx).await {
            Ok(()) => (),
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        }

        return Response::set_ok_response(UpdateResponse::set_update_response(test1))
    }

    async fn delete(&self, delete_request: DeleteRequest) -> Response<()> {
        let mut tx = match self.postgres_util.begin().await {
            Ok(tx) => tx,
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        };

        let rows_affected = match self.postgres_respository.delete(&mut tx, delete_request.id).await {
            Ok(rows_affected) => rows_affected,
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        };

        if rows_affected != 1 {
            return Response::set_internal_server_error_response();
        }

        match self.postgres_util.commit(tx).await {
            Ok(()) => (),
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        }

        return Response::set_no_content_response()
    }
}