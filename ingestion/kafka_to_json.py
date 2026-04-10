import json 
import os 
from kafka import KafkaConsumer
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

consumer = KafkaConsumer(
    "football-matches",
    bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
    auto_offset_reset='earliest',
    consumer_timeout_ms=5000,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

matches = []
for message in consumer:
    matches.append(message.value)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"data/matches_{timestamp}.json"

os.makedirs("data", exist_ok=True)

with open(filename, "w") as f:
    json.dump(matches, f, indent=2)

print(f"Matches saved {len(matches)} on {filename}")