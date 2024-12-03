import csv
from confluent_kafka import Producer
import json

# Kafka configuration
BROKER = "localhost:9092"  # Kafka broker address
TOPIC = "product_reviews"

def delivery_report(err, msg):
    """Callback for message delivery success or failure."""
    if err:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def produce_messages(csv_file):
    """Produce messages to Kafka from a CSV file."""
    producer = Producer({"bootstrap.servers": BROKER})
    
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Create a dictionary that matches your CSV columns
            message = {
                "text": row["text"],
                "rating": row["rating"],
                "category": row["category"],
                "product_name": row["product_name"],
                "product_id": row["product_id"],
                "sold": row["sold"],
                "shop_id": row["shop_id"],
                "product_url": row["product_url"]
            }
            # Convert dictionary to JSON string
            json_message = json.dumps(message)
            
            # Send message to Kafka
            producer.produce(TOPIC, key=row["product_id"], value=json_message, callback=delivery_report)
            producer.flush()

    print("All messages sent successfully.")

if __name__ == "__main__":
    csv_path = "../data/raw/product_reviews_dirty.csv"  # Path to your CSV file
    produce_messages(csv_path)
