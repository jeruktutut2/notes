use std::process;

use chrono::Local;
use rdkafka::{consumer::{Consumer, StreamConsumer}, message::Message, ClientConfig};
use tokio_stream::StreamExt;

pub struct KafkaConsumerImpl {

}

impl KafkaConsumerImpl {
    pub fn new() -> KafkaConsumerImpl {
        println!("{} kafka: creating consumer", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string());
        const BROKER: &str = "localhost:9092";
        const TOPIC: &str = "text-messages";
        const GROUP_ID: &str = "text-message-consumer-group-table";
        let consumer: StreamConsumer = match ClientConfig::new()
            .set("bootstrap.servers", BROKER)
            .set("group.id", GROUP_ID)
            .set("auto.offset.reset", "earliest")
            .create() {
                Ok(consumer) => consumer,
                Err(err) => {
                    println!("error creating consumer: {}", err);
                    process::exit(1);
                }
            };
        tokio::spawn(async move {
            consumer.subscribe(&[TOPIC]).expect("cannot subscribe to: topic");
            // consumer need to be static if i put it above tokio::spawn, so just put it in tokio::spawn
            let mut stream = consumer.stream();
            while let Some(Ok(messsage)) = stream.next().await {
                if let Some(payload) = messsage.payload_view::<str>() {
                    println!("Received: {:?} with key {:?}", payload, messsage.key());
                }
            }
        });
        println!("{} kafka: created consumer", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string());
        KafkaConsumerImpl {  }
    }
}