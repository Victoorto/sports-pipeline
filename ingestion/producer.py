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
BASE_URL = "https://api.football-data.org/v4/competitions/{}/matches?status=FINISHED"

headers = {"X-Auth-Token":API_KEY}

COMPETITIONS = ["PL", "PD", "BL1", "SA", "FL1"]

def fetch_and_send():
    total = 0
    for comp in COMPETITIONS:
        URL = BASE_URL.format(comp)
        response = requests.get(URL, headers=headers)
        if response.status_code == 200:
            matches = response.json().get("matches", [])
            for match in matches:
                producer.send('football-matches', value=match)
            total += len(matches)
            producer.flush()
            print(f'Total matches: {len(matches)}')
        else:
            print(f'Error: {response.status_code}')
    print(f'Total Matches sent: {total}')

while True:
    fetch_and_send()
    time.sleep(60)
    