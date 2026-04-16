import json 
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "football-matches",
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda v:json.loads(v.decode('utf-8'))
)

print('Listening Kafka messages ... \n')

for message in consumer:
    match = message.value
    home = match['homeTeam']['name']
    away = match['awayTeam']['name']
    status = match['status']
    date = match['utcDate'][:10]