<div align="center">

# 🏥 GraamSehat

### AI-Powered Rural Health Monitoring System

*Empowering ASHA workers with intelligent tools to transform rural healthcare delivery*

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20Site-brightgreen?style=for-the-badge)](https://byteverse-graamsehat.vercel.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
[![Built with React](https://img.shields.io/badge/Frontend-React-61DAFB?style=for-the-badge&logo=react)](https://reactjs.org/)
[![Node.js](https://img.shields.io/badge/Backend-Node.js-339933?style=for-the-badge&logo=node.js)](https://nodejs.org/)

</div>

---

## 📌 Overview

GraamSehat is a full-stack AI-powered platform designed to modernize rural healthcare in India. It equips **ASHA (Accredited Social Health Activist) workers** with real-time patient tracking, ML-based risk prediction, and an offline-first data pipeline — replacing fragmented manual workflows with a unified digital system.

> 🚀 **Live Deployment:** [byteverse-graamsehat.vercel.app](https://byteverse-graamsehat.vercel.app/)

---

## 🔍 Problem Statement

Rural healthcare in India faces deeply systemic challenges:

| Challenge | Impact |
|---|---|
| No real-time patient monitoring | Delayed identification of at-risk patients |
| Poor data synchronization | Inconsistent records across health centers |
| No predictive tools | Reactive rather than preventive care |
| Manual, paper-based processes | High error rates and data loss |

---

## 💡 Our Solution

GraamSehat addresses these gaps through four core pillars:

- **📱 Digital Platform** — A purpose-built interface for ASHA workers to register, track, and manage patient cases from the field
- **🧠 AI Risk Prediction** — A machine learning model that flags high-risk patients based on health parameters, enabling proactive intervention
- **📊 Analytics Dashboard** — Real-time insights into population health trends across villages and regions
- **🔄 Offline-First Sync** — Robust data synchronization that works reliably even in low-connectivity rural environments

---

## ✨ Key Features

- ✅ ASHA Worker Registration & Authentication
- ✅ Patient Case Tracking with Sync Engine
- ✅ AI-Based Health Risk Prediction (TensorFlow / Scikit-learn)
- ✅ Real-Time Health Analytics Dashboard
- ✅ Scalable RESTful Backend Architecture
- ✅ Redis Caching for Performance
- ✅ PostgreSQL for Reliable Persistent Storage

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React (Vite) |
| **Backend** | Node.js + Express |
| **Database** | PostgreSQL |
| **Cache** | Redis |
| **ML Service** | Python, TensorFlow, Scikit-learn |
| **Deployment** | Vercel (Frontend), Render (Backend) |

---

## 📂 Project Structure
```
graamsehat/
├── backend/        # API and database logic
├── frontend/       # User interface (React)
├── ml-service/     # Machine learning model
├── docs/           # Documentation
├── tests/          # Test files
```

---

## 🔌 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/asha/register` | Register a new ASHA worker |
| `GET` | `/api/asha/:phone` | Fetch ASHA worker details by phone |
| `POST` | `/api/sync/cases` | Sync patient cases from field |
| `GET` | `/api/dashboard/summary` | Retrieve aggregated health analytics |

---

## ⚙️ Local Setup

### Prerequisites
- Node.js ≥ 18
- Python ≥ 3.9
- PostgreSQL & Redis running locally

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/graamsehat.git
cd graamsehat
```

### 2. Start the Backend

```bash
cd backend
npm install
npm run dev
```

### 3. Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Start the ML Service

```bash
cd ml-service
pip install -r requirements.txt
python app.py
```

The frontend will be available at `http://localhost:5173` and the backend at `http://localhost:3000` by default.

---

## 🧠 Future Roadmap

- [ ] 📲 Mobile app for ASHA workers (Android-first)
- [ ] 🔔 Real-time patient alert system via SMS/push notifications
- [ ] 🩺 Telemedicine integration for remote consultations
- [ ] 🤖 Advanced ML models (time-series vitals, multi-disease risk stratification)
- [ ] 🌐 Multilingual support (Hindi, regional languages)
- [ ] 📡 FHIR-compliant health data interoperability

---

## 👥 Team — ByteVerse

| Member | Role | Responsibilities |
|---|---|---|
| **Aditya Narayan** | Backend Developer | REST APIs, database architecture, authentication, scalability |
| **Anjali** | Frontend Developer | React UI, API integration, accessibility, user flows |
| **Harshwardhan** | AI/ML Engineer | Model development, data preprocessing, feature engineering, ML-backend integration |
| **Neha Kumari** | Integration & Deployment | System integration, API debugging, Vercel/Render deployment, end-to-end testing |

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
  Built with ❤️ for rural India &nbsp;|&nbsp; ByteVerse Hackathon
</div>
