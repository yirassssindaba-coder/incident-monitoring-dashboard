# IT Incident Management Dashboard

## Overview
Aplikasi web responsif berbasis Flask (Python) dengan database SQLite untuk sistem pencatatan dan pemantauan insiden IT. Menunjukkan pemahaman konsep SLA, incident management, dan pelaporan operasional.

## Current State
- **Status**: Complete and functional
- **Framework**: Flask with SQLite
- **Port**: 5000

## Project Structure
```
.
├── app.py                    # Main Flask application
├── templates/
│   ├── base.html            # Base template with navigation
│   ├── dashboard.html       # Dashboard with statistics
│   ├── incidents.html       # Incidents list with filtering
│   ├── incident_form.html   # Create/edit incident form
│   ├── incident_detail.html # Incident detail view
│   └── how_to_use.html      # User guide
├── static/
│   └── css/
│       └── style.css        # Custom responsive CSS
├── incidents.db             # SQLite database (auto-created)
└── replit.md                # This file
```

## Features
1. **Dashboard**: Overview statistik insiden, SLA compliance, distribusi kategori/severity
2. **Incident Management**: CRUD operations untuk insiden
3. **SLA Tracking**: Perhitungan otomatis SLA compliance
4. **RCA & Resolution**: Field untuk root cause analysis dan resolusi
5. **Export CSV**: Download laporan insiden dalam format CSV
6. **Filter & Search**: Pencarian dan filter berdasarkan status/severity
7. **How to Use**: Panduan penggunaan untuk user non-teknis

## Severity Levels
- Low, Medium, High, Critical

## Status Options
- Open, In Progress, Pending, Resolved, Closed

## Categories
- Hardware, Software, Network, Security, Database, Application, Other

## Security Features
- Input validation server-side
- Controlled severity/status values
- Try/except error handling
- No SQL injection (parameterized queries)
- Cache-Control headers

## Recent Changes
- January 2026: Initial development - complete application

## Running the Application
```bash
python app.py
```
Application runs on port 5000.
