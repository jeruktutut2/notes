use validator::Validate;
use crate::helpers::validator_helper::get_validation_error;
use crate::models::requests::create_request::CreateRequest;
use crate::models::responses::create_response::CreateResponse;
use crate::models::responses::response::Response;

pub trait Test1Service {
    async fn create(&self, create_request: CreateRequest) -> Response<CreateResponse>;
}

pub struct Test1ServiceImpl {}

impl Test1ServiceImpl {
    pub fn new() -> Self {
        Test1ServiceImpl {}
    }
}

impl Test1Service for Test1ServiceImpl {
    async fn create(&self, create_request: CreateRequest) -> Response<CreateResponse> {
        if let Err(err) = create_request.validate() {
            return Response::set_validation_error(get_validation_error(err));
        }
        Response::set_created_response(CreateResponse::new(create_request.email, create_request.username, create_request.phone_number, create_request.password))
    }
}