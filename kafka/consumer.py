from lakehouse import write_to_delta  # Impor fungsi dari lakehouse.py
from confluent_kafka import Consumer
import json

# Kafka configuration
BROKER = "localhost:9092"
TOPIC = "product_reviews"
GROUP_ID = "consumer_group_1"

def consume_messages():
    """Consume messages from Kafka and process them."""
    consumer = Consumer({
        "bootstrap.servers": BROKER,
        "group.id": GROUP_ID,
        "auto.offset.reset": "earliest"
    })
    
    consumer.subscribe([TOPIC])
    
    print(f"Subscribed to topic: {TOPIC}")
    
    try:
        while True:
            msg = consumer.poll(1.0)  # Poll for messages
            
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            
            # Deserialize JSON message
            record = json.loads(msg.value().decode("utf-8"))
            print(f"Received message: {record}")
            
            # Save data to Delta Lake using the function from lakehouse.py
            write_to_delta(record)

    except KeyboardInterrupt:
        print("Consumer stopped.")
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_messages()
