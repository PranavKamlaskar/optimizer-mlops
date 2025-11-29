# optimizer-mlops

## System & Folder Setup
mkdir ai-cicd-optimizer
cd ai-cicd-optimizer
mkdir -p infra jenkins mlflow prometheus grafana fastapi docker data logs

You'll place each service in the correct directory.

## Install Core Tools
docker and docker-compose 
<https://github.com/PranavKamlaskar/quicknotes/blob/main/Install%20docker>

## Install Python + Virtual Environment
sudo apt install python3 python3-pip python3-venv -y
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip


## Install the ML Stack (Local Development)
pip install torch scikit-learn pandas numpy mlflow fastapi uvicorn[standard] python-multipart
pip install prometheus_client


##Setup MLflow (local SQLite mode)
https://github.com/PranavKamlaskar/quicknotes/blob/main/setup%20mlflow%20server

## Setup FastAPI Inference Service
https://github.com/PranavKamlaskar/optimizer-mlops/tree/323037f8eded418658bc8c8f51e6c3a487126883/api
api

uvicorn api.app:app --host 0.0.0.0 --port 8000

curl http://localhost:8000/health



## setup prometheus 

Set Up Prometheus
<https://github.com/PranavKamlaskar/quicknotes/blob/main/Set%20Up%20Prometheus>

## Setup grafana 

<https://github.com/PranavKamlaskar/quicknotes/blob/main/Set%20Up%20Grafana>

## Setup Jenkins Server

<https://github.com/PranavKamlaskar/quicknotes/blob/main/ssetup%20jenkins>

## Setup GitHub Actions

<https://github.com/PranavKamlaskar/quicknotes/blob/main/Set%20Up%20GitHub%20Actions>

# phase 2 


## Create Data Pipeline Folder Structure
ai-cicd-optimizer/
└── data/
    ├── raw/               # raw logs
    ├── parsed/            # cleaned logs + metadata
    ├── datasets/          # final training sets
└── scripts/
    ├── jenkins_log_fetch.py
    ├── gha_log_fetch.py
    ├── log_parser.py
    ├── build_metadata_schema.json
    ├── dataset_builder.py


## Define Build Metadata Schema
scripts/build_metadata_schema.json
<https://github.com/PranavKamlaskar/optimizer-mlops/blob/main/scripts/build_metadata_schema.json>

## Jenkins Log Collector Script

Create file: scripts/jenkins_log_fetch.py
<https://github.com/PranavKamlaskar/optimizer-mlops/blob/main/scripts/jenkins_log_fetch.py>

## GitHub Actions Log Collector Script

Create file: scripts/gha_log_fetch.py

<https://github.com/PranavKamlaskar/optimizer-mlops/blob/main/scripts/gha_log_fetch.py>

## Log Parsing & Cleaning Script

Create file: scripts/log_parser.py
<https://github.com/PranavKamlaskar/optimizer-mlops/blob/main/scripts/log_parser.py>

## Build the Training Dataset

Create file: scripts/dataset_builder.py
<https://github.com/PranavKamlaskar/optimizer-mlops/blob/main/scripts/dataset_builder.py>



# Execute Phase 2 Pipeline

Fetch logs
python scripts/jenkins_log_fetch.py
python scripts/gha_log_fetch.py

Parse logs
python scripts/log_parser.py

Build dataset
python scripts/dataset_builder.py

This dataset is used in Phase 3 to train the baseline ML model.

Phase 2 Deliverables
✔ Raw logs from Jenkins + GitHub Actions
✔ Cleaned logs
✔ Structured metadata
✔ Error-line extracted text
✔ Training dataset (build_dataset.csv)
