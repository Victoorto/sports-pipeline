# ⚽ Sports Analytics Pipeline

A real-time data engineering pipeline that ingests live football match data from the Football-Data.org API, streams it through Apache Kafka, and processes it in Databricks following the Medallion Architecture.

## 🏗️ Architecture

Football-Data API → Apache Kafka → Databricks (Bronze → Silver → Gold) → Dashboard


## 🛠️ Tech Stack

- **Ingestion**: Python, Apache Kafka, REST API
- **Processing**: Apache Spark (PySpark), Databricks, Delta Tables, Apache Iceberg
- **Orchestration**: Apache Airflow *(coming soon)*
- **Visualization**: Streamlit *(coming soon)*
- **Infrastructure**: Docker, Docker Compose
- **Cloud**: Databricks Community Edition


## 📁 Project Structure

        sports-pipeline/
        |
        ├── docker/
        |   └── docker-compose.yml       # Kafka + Zookeeper setup
        |
        ├── ingestion/
        |   │   ├── producer.py              # Fetches data from API and sends to Kafka
        |   │   ├── consumer.py              # Kafka consumer for debugging
        |   │   └── kafka_to_json.py         # Saves Kafka messages to JSON files
        |
        ├── transformations/
        |   │   └── (PySpark transformations via Databricks notebooks)
        |
        ├── notebooks/
        |   │   ├── 01_ingest_matches_bronze.py    # Raw data ingestion
        |   │   ├── 02_transform_matches_silver.py # Data cleaning and enrichment
        |   │   └── 03_aggregate_matches_gold.py   # Business aggregations
        |
        ├── .env.example
        ├── requirements.txt
        └── README.md

## 🥉🥈🥇 Medallion Architecture

| Layer | Table | Description |
|-------|-------|-------------|
| Bronze | `football_matches_bronze` | Raw data as received from the API |
| Silver | `football_matches_silver` | Cleaned data, typed columns, enriched with match result |
| Gold | `football_wins_gold` | Teams ranked by total wins |
| Gold | `football_goals_gold` | Goals and averages per competition |
| Gold | `football_results_gold` | Distribution of match results |

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- Databricks Community Edition account
- Football-Data.org API key (free tier)

### 1. Clone the repository
```bash
git clone https://github.com/tu-usuario/sports-pipeline.git
cd sports-pipeline
```

### 2. Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your API key
```

### 3. Start Kafka
```bash
cd docker
docker-compose up -d
```

### 4. Run the producer
```bash
cd ingestion
python producer.py
```

### 5. Save Kafka messages to JSON
```bash
python ingestion/kafka_to_json.py
```

### 6. Upload JSON to Databricks
Upload the generated file from `data/` to your Databricks volume and run the notebooks in order.

## 🔄 Streaming Variant

This project includes a streaming variant for environments with full Databricks access (Azure/AWS/GCP). Instead of saving to JSON, Kafka connects directly to Databricks using Spark Structured Streaming:

```python
df_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "your-kafka-server:9092") \
    .option("subscribe", "football-matches") \
    .load()
```

See `transformations/streaming_variant.py` for the full implementation.

## 📊 Data Coverage

- **Competitions**: Premier League, La Liga, Bundesliga, Serie A, Ligue 1
- **Records**: ~1,468 finished matches
- **Source**: [Football-Data.org](https://www.football-data.org/)

## 👤 Author

**Victor Tapia**  
Junior Data Engineer  
[LinkedIn](https://www.linkedin.com/in/victoorto/) | [GitHub](https://github.com/Victoorto)