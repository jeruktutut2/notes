use std::{sync::Arc, time::Duration};

use chrono::Utc;
use rdkafka::{producer::FutureRecord, util::Timeout};

use crate::producers::kafka_producer::{KafkaProducer, KafkaProducerImpl};

pub trait KafkaService {
    async fn send_message(&self, message: String) -> String;
}

pub struct KafkaServiceImpl {
    kafka_producer: Arc<KafkaProducerImpl>
}

impl KafkaServiceImpl {
    pub fn new(kafka_producer: Arc<KafkaProducerImpl>) -> KafkaServiceImpl {
        KafkaServiceImpl { 
            kafka_producer
        }
    }
}

impl KafkaService for KafkaServiceImpl {
    async fn send_message(&self, message: String) -> String {
        const TOPIC: &str = "text-messages";
        let key = Utc::now().timestamp_millis().to_string();
        let record = FutureRecord::to(TOPIC).key(key.as_str()).payload(&message);
        let producer = self.kafka_producer.get_producer().await;
        match producer.send(record,Timeout::After(Duration::from_secs(5))).await {
            Ok(delivery) => println!("producer sent: {:?}", delivery),
            Err(err) => {
                println!("error: {:?}", err);
                return "error".to_string()
            }
        }
        "ok".to_string()
    }
}