import json
from kafka import KafkaConsumer
from core.database import engine, metadata
from datetime import datetime
from sqlalchemy import Table, Column, Integer, DateTime, text

interactions = Table('interactions', metadata,
                     Column('user_id', Integer),
                     Column('item_id', Integer),
                     Column('interaction_score', Integer),
                     Column('timestamp', DateTime)
                    )

metadata.create_all(engine)

consumer = KafkaConsumer(
    'user_interactions',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Listening for messages on 'user_interactions' topic...")
for message in consumer:
    event = message.value

    # This turns 1773086023.52 into 2026-03-09 21:54:23...
    raw_ts = event.get('timestamp')
    if raw_ts:
        event['timestamp'] = datetime.fromtimestamp(raw_ts)

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO interactions (user_id, item_id, interaction_score, timestamp)
                VALUES (:user_id, :item_id, :interaction_score, :timestamp)
            """),
            event
        )
        conn.commit()
    print(f"Inserted event into DB: {event}")