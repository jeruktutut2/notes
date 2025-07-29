use std::sync::Arc;

use crate::producers::mqtt_producer::{MqttProducer, MqttProducerImpl};

pub trait MqttService {
    async fn send_message(&self, message: String) -> String;
}

pub struct MqttServiceImpl {
    mqtt_producer: Arc<MqttProducerImpl>
    
}

impl MqttServiceImpl {
    pub fn new(mqtt_producer: Arc<MqttProducerImpl>) -> MqttServiceImpl {
        MqttServiceImpl { 
            mqtt_producer
        }
    }
}

impl MqttService for MqttServiceImpl {
    async fn send_message(&self, message: String) -> String {
        match self.mqtt_producer.send_message(message).await {
            Ok(_) => (),
            Err(err) => {
                println!("error mqtt service: {}", err);
                return "error".to_string();
            }
        }
        "ok".to_string()
    }
}