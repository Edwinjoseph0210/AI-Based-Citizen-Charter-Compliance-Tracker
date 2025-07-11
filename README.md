# AI-Based Citizen Charter Compliance Tracker

## Overview
This project monitors whether government departments are meeting service delivery deadlines defined in their Citizen Charters (e.g., birth certificate within 7 days). It scrapes public dashboards or RTI databases, matches actual delivery times with mandated timelines, flags late deliveries, and generates compliance reports and visual trends.

## Components
- **scraper/**: Python Scrapy/BeautifulSoup spiders to collect service request and delivery data.
- **backend/**: Python Flask/FastAPI app with rule engine, API endpoints, and PostgreSQL integration.
- **dashboard/**: Streamlit/Dash app for visualizing compliance, trends, and reports.
- **.env.example**: Example environment variables for configuration.

## Setup
1. Clone the repo and set up Python 3.9+ and PostgreSQL.
2. Copy `.env.example` to `.env` and fill in your configuration.
3. Install dependencies in each component folder (`pip install -r requirements.txt`).
4. Run the scraper to populate the database.
5. Start the backend API server.
6. Launch the dashboard for visualization.

## Optional
- Integrate with Open Data APIs for real-time updates.

---

See each component's README or code comments for further details.