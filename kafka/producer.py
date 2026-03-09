import json
import time
import random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def stream_user_activity():
    print("Starting stream... Press Ctrl+C to stop.")
    while True:
        data={
            'user_id': random.randint(1, 100),
            'item_id': random.randint(1, 50),
            'interaction_score': random.randint(1, 5),
            'timestamp': time.time()
        }

        producer.send('user_interactions', value=data)
        print(f"Sent: {data}")
        time.sleep(2)

if __name__ == "__main__":
    stream_user_activity()