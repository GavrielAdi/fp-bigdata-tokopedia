from confluent_kafka import Producer
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "product-input"

producer = Producer({'bootstrap.servers': KAFKA_BROKER})

def delivery_report(err, msg):
    if err:
        logging.error(f"Message delivery failed: {err}")
    else:
        logging.info(f"Message delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}")

def send_to_kafka(features):
    try:
        message = {"features": features}
        producer.produce(TOPIC_NAME, json.dumps(message), callback=delivery_report)
        producer.flush()
    except Exception as e:
        logging.error(f"Error sending to Kafka: {str(e)}")
