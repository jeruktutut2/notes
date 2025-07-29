use std::sync::Arc;
use crate::{models::{entities::test1::Test1, requests::{create_request::CreateRequest, delete_request::DeleteRequest, update_request::UpdateRequest}, responses::{create_response::CreateResponse, get_by_id_response::GetByIdResponse, http_response::Response, update_response::UpdateResponse}}, repositories::mysql_repository::{MysqlRepository, MysqlRepositoryImpl}, utils::mysql_util::{MysqlUtil, MysqlUtilImpl}};

pub trait MysqlService {
    async fn create(&self, create_request: CreateRequest) -> Response<CreateResponse>;
    async fn get_by_id(&self, id: i32) -> Response<GetByIdResponse>;
    async fn update(&self, update_request: UpdateRequest) -> Response<UpdateResponse>;
    async fn delete(&self, delete_request: DeleteRequest) -> Response<()>;
}

pub struct MysqlServiceImpl {
    mysql_util: Arc<MysqlUtilImpl>,
    mysql_repository: Arc<MysqlRepositoryImpl>
}

impl MysqlServiceImpl {
    pub fn new(mysql_util: Arc<MysqlUtilImpl>, mysql_repository: Arc<MysqlRepositoryImpl>) -> MysqlServiceImpl {
        return MysqlServiceImpl {
            mysql_util,
            mysql_repository
        };
    }
}

impl MysqlService for MysqlServiceImpl {
    async fn create(&self, create_request: CreateRequest) -> Response<CreateResponse> {
        let mut tx = match self.mysql_util.begin().await {
            Ok(tx) => tx,
            Err(err) => {
                println!("err: {}", err);
                // return GenericResponse::set_internal_server_error_http_response()
                return Response::set_internal_server_error_response();
            }
        };

        let mut test1 = Test1 { id: 0, test: create_request.test };
        let (rows_affected, last_inserted_id) = match self.mysql_repository.create(&mut tx, &test1).await {
            Ok((rows_affected, last_inserted_id)) => (rows_affected, last_inserted_id),
            Err(err) => {
                match self.mysql_util.rollback(tx).await {
                    Ok(()) => (),
                    Err(err) => {
                        println!("err: {}", err);
                        return Response::set_internal_server_error_response();
                    }
                }
                println!("err: {}", err);
                return Response::set_internal_server_error_response()
            }
        };
        if rows_affected != 1 {
            return Response::set_internal_server_error_response()
        }
        test1.id = last_inserted_id as i32;

        match self.mysql_util.commit(tx).await {
            Ok(()) => (),
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        }
        // return GenericResponse::set_internal_server_error_http_response()
        // return HttpResponse::set_internal_server_error_http_response();
        let create_response = CreateResponse{id: test1.id, test: test1.test};
        return Response::set_created_response(create_response);
    }

    async fn get_by_id(&self, id: i32) -> Response<GetByIdResponse> {
        let test1 = match self.mysql_repository.get_by_id(self.mysql_util.get_pool().await, id).await {
            Ok(test1) => test1,
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        };
        let get_by_id_response = GetByIdResponse{id: test1.id, test: test1.test};
        return Response::set_ok_response(get_by_id_response);
    }
    async fn update(&self, update_request: UpdateRequest) -> Response<UpdateResponse> {
        let mut tx = match self.mysql_util.begin().await {
            Ok(tx) => tx,
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        };
        let test1 = Test1{id: update_request.id, test: update_request.test};
        let rows_affected = match self.mysql_repository.update(&mut tx, &test1).await {
            Ok(rows_affected) => rows_affected,
            Err(err) => {
                match self.mysql_util.rollback(tx).await {
                    Ok(()) => (),
                    Err(err) => {
                        println!("err: {}", err);
                        return Response::set_internal_server_error_response();
                    }
                }
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        };
        if rows_affected != 1 {
            return Response::set_internal_server_error_response();
        }
        match self.mysql_util.commit(tx).await {
            Ok(()) => (),
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        }
        let update_response = UpdateResponse{id: test1.id, test: test1.test};
        Response::set_ok_response(update_response)
    }
    async fn delete(&self, delete_request: DeleteRequest) -> Response<()> {
        let mut tx = match self.mysql_util.begin().await {
            Ok(tx) => tx,
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        };
        let rows_affected = match self.mysql_repository.delete(&mut tx, delete_request.id).await {
            Ok(rows_affected) => rows_affected,
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        };
        if rows_affected != 1 {
            return Response::set_internal_server_error_response()
        }
        match self.mysql_util.commit(tx).await {
            Ok(()) => (),
            Err(err) => {
                println!("err: {}", err);
                return Response::set_internal_server_error_response();
            }
        }
        Response::set_no_content_response()
    }
}