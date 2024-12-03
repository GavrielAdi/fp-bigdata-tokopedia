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
            
            # Example: Save to Delta Lake or process the data
            save_to_lakehouse(record)

    except KeyboardInterrupt:
        print("Consumer stopped.")
    finally:
        consumer.close()

def save_to_lakehouse(record):
    """Example function to save data to Delta Lake."""
    print(f"Saving to lakehouse: {record}")
    # Here you would write the data to Delta Lake

if __name__ == "__main__":
    consume_messages()
