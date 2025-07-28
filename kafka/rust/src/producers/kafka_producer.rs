use rdkafka::{producer::FutureProducer, ClientConfig};

pub trait KafkaProducer {
    async fn get_producer(&self) -> FutureProducer;
}

pub struct KafkaProducerImpl {
    producer: FutureProducer
}

impl KafkaProducerImpl {
    pub fn new() -> KafkaProducerImpl {
        const BROKER: &str = "localhost:9092";
        let producer: FutureProducer = ClientConfig::new()
            .set("bootstrap.servers", BROKER)
            .create()
            .expect("Producer creation failed");
        KafkaProducerImpl { 
            producer
         }
    }
}

impl KafkaProducer for KafkaProducerImpl {
    async fn get_producer(&self) -> FutureProducer {
        self.producer.clone()
    }
}