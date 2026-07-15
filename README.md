# SECOP II ETL Pipeline

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![DigitalOcean](https://img.shields.io/badge/DigitalOcean-Droplet-0080FF?logo=digitalocean&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automated-2088FF?logo=githubactions&logoColor=white)

</p>

Production-ready ETL pipeline that incrementally extracts Colombian public procurement contracts from **SECOP II**, transforms the data into a dimensional model, and loads it into a PostgreSQL data warehouse designed for analytical workloads.

---

## Overview

SECOP II is Colombia's official public procurement platform and publishes millions of contract records through the Socrata Open Data API.

This project automates the complete ETL process by:

- Extracting contract data incrementally from the SECOP II API.
- Cleaning and validating raw records.
- Transforming the data into a Star Schema.
- Loading the processed data into PostgreSQL.
- Running automatically through GitHub Actions.

The pipeline is designed following Data Engineering best practices with an emphasis on modularity, reproducibility, maintainability, and scalability.

---

## Features

- Incremental extraction strategy
- Modular ETL architecture
- Star Schema data model
- PostgreSQL data warehouse
- Dockerized deployment
- Automated GitHub Actions workflow
- Logging and execution monitoring
- Data quality validation

---


## Getting Started

Clone the repository:

```bash
git clone https://github.com/bryanmg20/secop2-etl-pipeline.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start PostgreSQL:

```bash
docker compose up -d
```

### Initial Load

Run the pipeline in **initial mode** to populate an empty database with all available records.

```bash
python main.py --mode initial
```

### Incremental Load

After the initial load, run the pipeline in **incremental mode** to ingest only newly published records.

```bash
python main.py --mode incremental
```
---

## Documentation

- [Architecture](docs/architecture.md)
- [Data Dictionary](docs/data_dictionary.md)