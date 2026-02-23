<div align="center">

<!-- Animated Wave Header -->
<img src="https://capsule-render.vercel.app/api?type=waving&height=210&color=0:0ea5e9,100:22c55e&text=Incident%20Monitoring%20Dashboard&fontSize=52&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Flask%20%7C%20SQLite%20%7C%20Incident%20Management%20%7C%20SLA%20dan%20Uptime%20Tracking&descAlignY=58" />

<!-- Typing SVG -->
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&duration=3000&pause=700&color=0EA5E9&center=true&vCenter=true&width=900&lines=System+Monitoring+dan+Incident+Management+Dashboard;SLA+Tracker+dan+Uptime+Calculation+with+Export+CSV;Stable+Flask+app+with+SQLite+schema+dan+validation" />

<p>
  <img src="https://img.shields.io/badge/Python-3.11+-3776ab" />
  <img src="https://img.shields.io/badge/Flask-3.x-000000" />
  <img src="https://img.shields.io/badge/Database-SQLite-0b5fff" />
  <img src="https://img.shields.io/badge/Focus-IT%20Operations%20dan%20IT%20Support-22c55e" />
</p>

</div>

---

## Overview
**Incident Monitoring Dashboard** is a responsive Flask + SQLite web app that simulates an internal IT operations workflow:
incident logging, status tracking, SLA and uptime calculation, and structured operational reporting.

It is designed to be stable, easy to demonstrate, and recruiter-friendly for IT Operations and IT Support roles.

---

## Key Features
- 📊 **Dashboard**
  - Weekly incident count
  - Status summary
  - Simple severity and category breakdown
- 🧾 **Incident Management**
  - Create incidents with category, severity, and SLA target
  - Filter by status and severity, plus keyword search
  - Detail page includes RCA and resolution notes
  - Update status with SLA breach detection when resolved
- ⏱️ **SLA Tracker**
  - SLA target hours per incident
  - SLA breach tracking and compliance summary
- 📤 **Reporting**
  - Export incident list to CSV for operational reporting

---

## Tech Stack
- 🐍 Python (Flask)
- 🗄️ SQLite
- 🧩 Jinja templates, HTML, CSS
- 🧯 Centralized error handling and input validation

---

## Data Model (SQLite)
### `incidents`
Typical fields used:
- `title`, `description`, `category`, `severity`, `status`
- `reported_by`, `assigned_to`
- `downtime_minutes`
- `root_cause`, `resolution`
- `sla_target_hours`, `sla_breached`
- `created_at`, `updated_at`, `resolved_at`

---

## Getting Started
### Requirements
- Python **3.11+**
- (Optional) Poetry

### Option A: Run with Poetry
```bash
poetry install
poetry run python app.py
```

### Option B: Run with pip
```bash
python -m venv .venv
# Windows PowerShell
# .\.venv\Scripts\Activate.ps1
# macOS / Linux
# source .venv/bin/activate

pip install flask gunicorn
python app.py
```

The app runs on `http://localhost:5000` by default.

---

## Useful Routes
- `/` → dashboard
- `/incidents` → incident list (filters and search)
- `/incidents/new` → create incident
- `/export/csv` → export incident data to CSV
- `/how-to-use` → usage guidance page (if available)

---

## Screenshots
Add images into `attached_assets/` then reference them here, for example:
- `attached_assets/dashboard.png`
- `attached_assets/incidents.png`
- `attached_assets/incident_detail.png`
- `attached_assets/sla_report.png`

---

## Recruiter Notes
- ✅ Demonstrates incident lifecycle management and reporting discipline  
- ✅ Shows SLA awareness with breach detection and compliance summary  
- ✅ Uses simple, stable architecture suitable for internal tools  

---

## License
For educational and portfolio purposes.
