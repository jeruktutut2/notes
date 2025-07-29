use std::sync::Arc;

use rumqttc::ClientError;

use crate::utils::mqtt_util::MqttUtilImpl;

pub trait MqttProducer {
    async fn send_message(&self, message: String) -> Result<(), ClientError>;
}

pub struct MqttProducerImpl {
    mqtt_util: Arc<MqttUtilImpl>
}

impl MqttProducerImpl {
    pub fn new(mqtt_util: Arc<MqttUtilImpl>) -> MqttProducerImpl {
        MqttProducerImpl { 
            mqtt_util
        }
    }
}

impl MqttProducer for MqttProducerImpl {
    async fn send_message(&self, message: String) -> Result<(), ClientError> {
        self.mqtt_util.client.lock().await.publish("test/topic", rumqttc::QoS::AtLeastOnce, false, message).await
    }
}