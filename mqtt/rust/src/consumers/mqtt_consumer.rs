use std::{process, sync::Arc};

use chrono::Local;
use rumqttc::{Event, Packet};

use crate::utils::mqtt_util::MqttUtilImpl;

pub struct MqttConsumerImpl {
}

impl MqttConsumerImpl {
    pub async fn new(mqtt_util: Arc<MqttUtilImpl>) -> MqttConsumerImpl {
        println!("{} kafka: subscribing to test/topic", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string());
        match mqtt_util.client.lock().await.subscribe("test/topic", rumqttc::QoS::AtMostOnce).await {
            Ok(_) => {
                println!("{} kafka: subscribed to test/topic", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string());
            },
            Err(err) => {
                println!("{} kafka: cannot subscribe to test/topic", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string());
                println!("error mqtt util: {}", err);
                process::exit(1);
            }
        }

        tokio::spawn(async move {
            while let Ok(event) = mqtt_util.event_loop.lock().await.poll().await {
                if let Event::Incoming(Packet::Publish(p)) = event {
                    println!("{} Received on {}: {}", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string(), p.topic, String::from_utf8_lossy(&p.payload));
                }
            }
        });

        MqttConsumerImpl { 
        }
    }
}