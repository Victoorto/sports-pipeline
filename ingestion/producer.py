import requests 
import json
import time 
from kafka import KafkaProducer
import os 
from dotenv import load_dotenv

load_dotenv()

producer = KafkaProducer(
    bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')

)

API_KEY = os.getenv('API_KEY') #Your API Key 
URL = "https://api.football-data.org/v4/matches"

headers = {"X-Auth-Token":API_KEY}

def fetch_and_send():
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        matches = response.json().get("matches", [])
        for match in matches:
            producer.send('football-matches', value=match)
            print(f'Enviado: {match['homeTeam']['name']} vs {match['awayTeam']['name']}')
        producer.flush()
        print(f'Total Enviados: {len(matches)} partidos')
    else:
        print(f'Error: {response.status_code}')

while True:
    fetch_and_send()
    time.sleep(60)
    