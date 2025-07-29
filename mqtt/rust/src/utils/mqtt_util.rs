use std::{sync::Arc, time::Duration};

use rumqttc::{AsyncClient, EventLoop, MqttOptions};
use tokio::sync::Mutex;

pub struct MqttUtilImpl {
    pub client: Arc<Mutex<AsyncClient>>,
    pub event_loop: Arc<Mutex<EventLoop>>
}

impl MqttUtilImpl {
    pub fn new() -> MqttUtilImpl {
        let mut mqtt_options = MqttOptions::new("mqtt_consumer", "localhost", 1883);
        mqtt_options.set_keep_alive(Duration::from_secs(60));
        let (client, event_loop) = AsyncClient::new(mqtt_options, 10);
        MqttUtilImpl {
            client: Arc::new(Mutex::new(client)),
            event_loop: Arc::new(Mutex::new(event_loop))
        }
    }
}