# 🚀 n8n Workflow Popularity System

> An automated, evidence-driven platform for discovering, analyzing, scoring, and exposing popular **n8n workflows** across YouTube, the n8n Community Forum, and Google Trends.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/n8n-Automation-orange?logo=n8n" alt="n8n">
  <img src="https://img.shields.io/badge/FastAPI-REST_API-009688?logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite" alt="SQLite">
  <img src="https://img.shields.io/badge/Status-Production%20Prototype-success" alt="Status">
</p>

---

## 📌 Overview

The **n8n Workflow Popularity System** is a data-driven automation platform that identifies popular n8n workflow topics by collecting measurable popularity signals from multiple sources.

Instead of relying on a single platform or subjective assumptions, the system combines:

* 📺 **YouTube** — views, likes, comments and engagement ratios
* 💬 **n8n Community Forum** — views, replies and likes
* 📈 **Google Trends** — search interest, average interest and growth
* ⚙️ **n8n** — automated collection and processing
* 🐍 **Python** — Google Trends collection and data processing
* 🚀 **FastAPI** — REST API layer
* 🗄️ **SQLite** — persistent storage

The architecture is designed to scale toward **20,000+ evidence records** while maintaining source traceability and avoiding fabricated data.

---

## ✨ Key Features

### 🔍 Multi-Source Discovery

Collects n8n-related popularity signals from:

| Source        | Evidence                           |
| ------------- | ---------------------------------- |
| YouTube       | Views, likes, comments             |
| n8n Forum     | Views, replies, likes              |
| Google Trends | Interest, average interest, growth |

### 📊 Popularity Scoring

Each source uses a documented scoring methodology based on its available signals.

### 🧹 Data Validation

Filters irrelevant content and invalid metrics before storing records.

### ♻️ Deduplication

Uses source-specific identifiers to prevent duplicate records.

### 🌎 Country Segmentation

Supports geographic analysis where reliable country-level evidence is available.

Currently demonstrated:

* 🇺🇸 United States
* 🇮🇳 India

### 🔌 REST API

FastAPI exposes the collected data through documented REST endpoints.

### ⏰ Automated Collection

n8n collectors use scheduled execution for recurring data collection.

### 🚨 Error Handling

An n8n Error Trigger workflow captures workflow execution failures.

### 📈 Scalable Architecture

The current implementation demonstrates real collected evidence while keeping the architecture extensible to larger datasets.

---

# 🏗️ System Architecture

```text
                     ┌─────────────────────┐
                     │      YouTube        │
                     │  YouTube Data API   │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │   n8n Collector     │
                     └──────────┬──────────┘
                                │
                                │
┌─────────────────────┐         │         ┌─────────────────────┐
│   n8n Community     │─────────┼────────▶│   Data Processing   │
│       Forum         │         │         │ Validation / Dedup  │
└─────────────────────┘         │         └──────────┬──────────┘
                                │                    │
┌─────────────────────┐         │                    ▼
│   Google Trends     │─────────┘          ┌─────────────────────┐
│  Python / pytrends  │                    │ Popularity Scoring  │
└─────────────────────┘                    └──────────┬──────────┘
                                                       │
                                                       ▼
                                            ┌─────────────────────┐
                                            │   SQLite Database   │
                                            └──────────┬──────────┘
                                                       │
                                                       ▼
                                            ┌─────────────────────┐
                                            │       FastAPI       │
                                            │      REST API       │
                                            └──────────┬──────────┘
                                                       │
                                                       ▼
                                            ┌─────────────────────┐
                                            │ JSON / API Clients  │
                                            └─────────────────────┘
```

---

# 📊 Current Dataset

The current implementation contains **172+ real evidence records**.

| Source              |  Records |
| ------------------- | -------: |
| YouTube             |     145+ |
| n8n Community Forum |       18 |
| Google Trends       |        9 |
| **Total**           | **172+** |

> The 20,000+ requirement is treated as a scalability target. The project does not fabricate records to reach that number.

---

# 📺 YouTube Collector

The YouTube collector searches for n8n-related workflow content using keywords such as:

```text
n8n workflow
n8n automation
n8n AI agent
n8n Gmail automation
n8n WhatsApp automation
n8n Google Sheets automation
n8n Slack automation
n8n CRM automation
```

### Collected Signals

* Video ID
* Title
* Description
* Channel
* Published date
* Views
* Likes
* Comments
* Source URL
* Collection timestamp

### Derived Metrics

```text
like_to_view_ratio = likes / views

comment_to_view_ratio = comments / views
```

### YouTube Score

```text
50% → Log-normalized Views
30% → Like / View Ratio
20% → Comment / View Ratio
```

---

# 💬 n8n Community Forum Collector

The system uses the n8n Community's Discourse API to discover relevant topics.

### Collected Signals

* Topic ID
* Topic title
* Topic URL
* Views
* Replies
* Likes
* Creation date
* Last activity
* Collection timestamp

### Forum Score

```text
50% → Log-normalized Views
30% → Replies
20% → Likes
```

Forum content is filtered to focus on workflow and automation-related discussions.

---

# 📈 Google Trends Collector

Google Trends is collected using Python and `pytrends`.

### Metrics

```text
Current Interest
Average Interest
Growth %
Interest Score
Average Score
Growth Score
```

### Google Trends Score

```text
50% → Current Interest
30% → Average Interest
20% → Growth
```

### Important Data Note

Google Trends provides **relative search interest on a 0–100 scale**.

These values should **not** be interpreted as exact search-volume counts.

---

# 🌎 Geographic Segmentation

The system distinguishes between:

* Source country
* Creator country
* Audience country
* Target-market country

Country information is only stored when reliable evidence is available.

For unavailable information:

```text
country = unknown
```

The system never guesses geographic information.

---

# 🧠 Popularity Methodology

Popularity is treated as an evidence-based metric rather than an absolute truth.

Each platform provides different signals, so the scoring methodology is source-specific.

After platform scoring, an additional normalized:

```text
overall_score
```

is generated for cross-platform analysis.

### Why normalization?

YouTube views, Forum replies, and Google Trends interest are fundamentally different measurements.

Normalization reduces the risk of directly comparing raw values that have different meanings and scales.

---

# 🗄️ Database

The current prototype uses SQLite for lightweight deployment.

### Main Table

```text
workflows
```

### Core Fields

```text
id
external_id
title
description
source_platform
source_url
country
views
likes
comments
replies
like_to_view_ratio
comment_to_view_ratio
popularity_score
overall_score
collected_at
```

### Google Trends Fields

```text
current_interest
average_interest
growth_percent
interest_score
average_score
growth_score
```

The database layer can be migrated to PostgreSQL for production-scale deployments.

---

# 🚀 REST API

FastAPI provides access to the collected dataset.

## API Documentation

After starting the server:

```text
http://127.0.0.1:8000/docs
```

FastAPI automatically provides interactive Swagger documentation.

---

## Endpoints

### Get Workflows

```http
GET /workflows
```

Supported filters:

```text
platform
country
keyword
limit
offset
```

Example:

```http
GET /workflows?platform=youtube&keyword=gmail&limit=10
```

---

### Top Workflows

```http
GET /workflows/top
```

---

### YouTube Workflows

```http
GET /workflows/youtube
```

---

### Forum Workflows

```http
GET /workflows/forum
```

---

### Google Trends

```http
GET /workflows/google
```

---

### Single Workflow

```http
GET /workflows/{workflow_id}
```

---

### Bulk Ingestion

```http
POST /workflows/bulk
```

The endpoint allows normalized workflow records to be inserted programmatically.

---

# ⚙️ n8n Automation

## YouTube Pipeline

```text
Schedule Trigger
       ↓
Keyword Generation
       ↓
YouTube Search API
       ↓
Flatten & Deduplicate
       ↓
YouTube Statistics API
       ↓
Normalization
       ↓
Validation
       ↓
Engagement Metrics
       ↓
Popularity Score
       ↓
Database / API
```

## Forum Pipeline

```text
Schedule Trigger
       ↓
n8n Community API
       ↓
Relevance Filtering
       ↓
Metric Calculation
       ↓
Popularity Score
       ↓
Database / JSON
```

## Error Pipeline

```text
Error Trigger
       ↓
Error Extraction
       ↓
Structured Error Record
       ↓
Monitoring / Notification Layer
```

---

# 🛡️ Data Quality & Reliability

The system applies several data-quality principles.

### Relevance Filtering

Unrelated content is removed before storage.

### Metric Validation

Invalid or negative metric values are rejected.

### Deduplication

Source identifiers prevent repeated records.

```text
YouTube
→ video_id

Forum
→ forum_topic_id

Google Trends
→ keyword + country
```

### Traceability

Each record retains:

```text
source
source URL
external ID
collection timestamp
```

This makes popularity evidence traceable back to its origin.

---

# 🔄 Data Processing Pipeline

```text
COLLECT
   ↓
VALIDATE
   ↓
NORMALIZE
   ↓
DEDUPLICATE
   ↓
CALCULATE METRICS
   ↓
CALCULATE SCORE
   ↓
STORE
   ↓
EXPOSE THROUGH API
```

---

# 🛠️ Tech Stack

| Technology        | Purpose                         |
| ----------------- | ------------------------------- |
| Python            | Data processing & Google Trends |
| n8n               | Workflow automation             |
| FastAPI           | REST API                        |
| SQLAlchemy        | ORM                             |
| SQLite            | Database                        |
| YouTube Data API  | YouTube evidence                |
| Discourse API     | n8n Forum evidence              |
| pytrends          | Google Trends                   |
| Swagger / OpenAPI | API documentation               |

---

# 📁 Project Structure

```text
n8n-workflow-popularity-system/
│
├── n8n/
│   ├── workflows/
│   │   ├── youtube_collector.json
│   │   ├── forum_collector.json
│   │   └── error_handler.json
│   │
│   ├── google_trends.py
│   ├── google_trends_data.json
│   ├── youtube_data.json
│   └── forum_data.json
│
├── api/
│   ├── main.py
│   ├── import_data.py
│   ├── migrate_db.py
│   ├── update_google_trends.py
│   ├── calculate_overall_score.py
│   └── workflows.db
│
├── README.md
└── .gitignore
```

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd n8n-workflow-popularity-system
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```powershell
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy pandas pytrends
```

---

## 4. Configure API Credentials

Store API credentials using environment variables or n8n credentials.

Never commit:

```text
API keys
tokens
passwords
.env files
```

---

## 5. Run FastAPI

```bash
cd api
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## 6. Run Google Trends Collector

From the project directory:

```bash
python google_trends.py
```

This generates:

```text
google_trends_data.json
```

---

## 7. Import Data

```bash
cd api
python import_data.py
```

---

# 🧪 Testing

The system was tested across:

* Data collection
* API ingestion
* Duplicate protection
* Metric calculation
* Popularity scoring
* Database persistence
* API filtering
* Pagination
* Keyword search
* Country filtering
* Swagger API
* Scheduled n8n workflows
* Error handling

Example:

```http
GET /workflows?platform=youtube
```

```http
GET /workflows?keyword=gmail
```

```http
GET /workflows?country=US
```

---

# 📈 Scalability

The current dataset demonstrates the architecture using real evidence.

For larger-scale deployment:

```text
SQLite
   ↓
PostgreSQL

Local execution
   ↓
Docker / Cloud

Basic deduplication
   ↓
Semantic similarity + embeddings

Single API
   ↓
Cached / horizontally scalable API
```

The collection architecture can be extended through:

* API pagination
* More keywords
* More geographic regions
* More source platforms
* Historical collection
* Scheduled execution
* Parallel processing

---

# ⚠️ Limitations

### YouTube

API quota limits the number of requests available within a project.

### Google Trends

Google Trends provides relative interest rather than exact search volume.

### Country Data

Audience country is not always directly available from public source APIs.

### Cross-Platform Comparison

Different platforms measure popularity differently. Therefore, normalized scores should be interpreted as analytical indicators rather than universal popularity measurements.

### Current Scale

The current implementation demonstrates the architecture using 172+ real records rather than artificially generating 20,000 records.

---

# 🔮 Future Improvements

* [ ] PostgreSQL production deployment
* [ ] Redis caching
* [ ] Authentication & authorization
* [ ] Advanced semantic deduplication
* [ ] Historical popularity tracking
* [ ] More country-specific datasets
* [ ] Additional social/community sources
* [ ] Dashboard for analytics
* [ ] Automated notifications
* [ ] Docker deployment
* [ ] Cloud deployment
* [ ] CI/CD pipeline

---

# 🎯 Project Objective

The core objective is simple:

> **Identify which n8n workflow topics are gaining real attention, explain that popularity using measurable evidence, and make the results accessible through an automated API-driven system.**

The project focuses on:

```text
Real Evidence
     +
Reliable Data Processing
     +
Transparent Scoring
     +
Automation
     +
API Accessibility
```

---

# 👨‍💻 Author

**Pavan Kumar Verma**

B.Tech CSE — AI & Data Science

Interested in:

* Artificial Intelligence
* Machine Learning
* Data Engineering
* Backend Development
* Automation
* LLM Applications

---

## ⭐ If you find this project useful

Give the repository a ⭐ and feel free to explore the implementation.

---

<p align="center">
  Built with Python, n8n, FastAPI & Data Engineering
</p>
