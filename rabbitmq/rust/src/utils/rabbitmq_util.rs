use std::process;

use rabbitmq_stream_client::{error::StreamCreateError, types::{ByteCapacity, OffsetSpecification, ResponseCode}, ConsumerHandle, Environment, NoDedup, Producer};
use tokio::task;
use futures::{StreamExt};

pub trait RabbitMQUtil {
    async fn set_consumer(&self) -> ConsumerHandle;
    async fn set_producer(&self) -> Producer<NoDedup>;
}

pub struct RabbitMQUtilImpl {
    environment: Environment
}

impl RabbitMQUtilImpl {
    pub async fn new() -> RabbitMQUtilImpl {
        let environment = match Environment::builder().host("localhost").username("user").password("password").port(5552).build().await {
            Ok(environment) => environment,
            Err(err) => {
                println!("error environtment: {}", err);
                process::exit(1);
            }
        };
        RabbitMQUtilImpl {
            environment
        }
    }
}

impl RabbitMQUtil for RabbitMQUtilImpl {
    async fn set_consumer(&self) -> ConsumerHandle {
        let mut consumer = match  self.environment.consumer().offset(OffsetSpecification::First).build("notification_stream").await {
            Ok(consumer) => consumer,
            Err(err) => {
                println!("error: {}", err);
                process::exit(1);
            }
        };
        let handle = consumer.handle();
        task::spawn(async move {
            // pending there is no method next
            while let Some(delivery) = consumer.next().await {
                let d = delivery.unwrap();
                println!("Got message: {:#?} with offset: {}",
                     d.message().data().map(|data| String::from_utf8(data.to_vec()).unwrap()),
                     d.offset(),);
            }
        });
        handle
    }

    async fn set_producer(&self) -> Producer<NoDedup> {
        let producer = match self.environment.producer().build("notification_stream").await {
            Ok(producer) => producer,
            Err(err) => {
                println!("error: {}", err);
                process::exit(1);
            }
        };
        producer
    }
}