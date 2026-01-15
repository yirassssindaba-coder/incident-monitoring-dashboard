# System Monitoring & Incident Management Dashboard

## 📌 Overview
System Monitoring & Incident Management Dashboard adalah aplikasi web responsif berbasis Flask dan SQLite yang dirancang untuk mensimulasikan sistem pencatatan insiden dan pelaporan operasional IT. Aplikasi ini merepresentasikan praktik kerja dasar IT Operations dan IT Support dalam menangani insiden, memantau SLA, serta menghasilkan laporan operasional yang terstruktur.

---

## 🎯 Project Objectives
- Menunjukkan pemahaman **incident & problem management**
- Menerapkan konsep **SLA dan uptime tracking**
- Menyediakan **dashboard monitoring operasional**
- Membuat aplikasi **stabil, sederhana, dan mudah diuji**
- Menjadi portofolio **internship-oriented & job-ready**

---

## 🧩 Key Features

### 1. Dashboard
- Jumlah insiden minggu berjalan
- Ringkasan status insiden
- Grafik sederhana berdasarkan severity

### 2. Incident Management
- Daftar insiden dengan filter:
  - Service
  - Severity
  - Status
- Form pembuatan insiden
- Detail insiden lengkap dengan:
  - Ringkasan masalah
  - Root Cause Analysis (RCA)
  - Resolution

### 3. SLA Tracker
- Input downtime per service
- Perhitungan uptime otomatis
- Rekap SLA bulanan

### 4. Reporting
- Export data insiden ke CSV
- Siap digunakan untuk laporan internal

---

## 🛠️ Tech Stack
- **Backend:** Flask (Python)
- **Database:** SQLite
- **Frontend:** HTML, CSS, Jinja Template
- **Mode:** Responsive Web + PWA-ready

---

## 🧱 Database Schema

### incidents
- `id`
- `date`
- `service`
- `severity`
- `status`
- `summary`
- `rca`
- `resolution`
- `created_at`

### sla_logs
- `id`
- `service`
- `month`
- `downtime_minutes`

---

## 🔐 Anti-Error Design
- Semua route menggunakan `try/except`
- Validasi input:
  - Date wajib diisi
  - Severity hanya: Low, Medium, High, Critical
- Query sederhana (CRUD only)
- Tidak ada join kompleks
- Error page ramah pengguna
- Empty state saat database kosong

---

## 🧪 Testing Checklist
- [x] Tambah insiden → update status → export CSV
- [x] Input salah → muncul pesan validasi
- [x] Database kosong → dashboard tampil normal
- [x] Aplikasi tetap stabil setelah refresh

---

## 📚 What I Learned
- Incident & problem management workflow
- SLA dan uptime calculation
- Flask routing & error handling
- SQLite schema design
- Ops reporting & dashboard logic

---

## 🚀 Future Improvements
- Autentikasi user & role
- Grafik SLA lanjutan
- Integrasi monitoring real-time
- REST API backend
- Notifikasi insiden

---

## 👤 Author
**[Nama Kamu]**  
IT Support / IT Operations / Junior Backend Developer  

- GitHub: https://github.com/your-username  
- Portfolio: https://your-portfolio-link  

---

## 📄 License
This project is created for educational and portfolio purposes.

---

## 🏁 Recruiter Notes
✔ Relevan untuk IT Ops & IT Support  
✔ Fokus SLA & incident workflow  
✔ Stabil dan mudah diuji  
✔ Cocok untuk internship & entry-level roles  
