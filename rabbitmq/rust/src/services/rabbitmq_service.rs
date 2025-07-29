use rabbitmq_stream_client::{types::Message, NoDedup, Producer};

pub trait RabbitMQService {
    async fn send_message(&self, message: String) -> String;
}

pub struct RabbitMQServiceImpl {
    producer: Producer<NoDedup>
}

impl RabbitMQServiceImpl {
    pub fn new(producer: Producer<NoDedup>) -> RabbitMQServiceImpl {
        RabbitMQServiceImpl {
            producer
        }
    }
}

impl RabbitMQService for RabbitMQServiceImpl {
    async fn send_message(&self, message: String) -> String {
        let confirmation_status = match self.producer.send_with_confirm(Message::builder().body(message).build()).await {
            Ok(confirmation_status) => confirmation_status,
            Err(err) => {
                println!("error: {}", err);
                return "error".to_string();
            }
        };
        println!("{:?}", confirmation_status);
        "ok".to_string()
    }
}