pub trait PanicService {
    async fn check_panic(&self) -> String;
}

pub struct PanicServiceImpl {

}

impl PanicServiceImpl {
    pub fn new() -> PanicServiceImpl {
        PanicServiceImpl {  }
    }
}

impl PanicService for PanicServiceImpl {
    async fn check_panic(&self) -> String {
        panic!("something went wrong")
    }
}