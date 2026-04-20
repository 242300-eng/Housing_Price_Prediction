# 🏠 Aashiyana Insights AI 2026

![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey?style=for-the-badge&logo=flask)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?style=for-the-badge&logo=scikit-learn)
![MongoDB](https://img.shields.io/badge/MongoDB-NoSQL-green?style=for-the-badge&logo=mongodb)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)
![CI/CD](https://img.shields.io/badge/CI/CD-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen?style=for-the-badge&logo=pytest)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

> **Aashiyana Insights AI** is an end-to-end, **production-ready** Machine Learning web application to predict property prices across **60+ major Indian cities**. Built for accuracy, scalability, and a premium user experience.

---

## 📋 Table of Contents
- [Live Demo](#-live-demo)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [ML Pipeline](#-ml-pipeline-highlights)
- [Architecture](#-system-architecture)
- [Installation](#%EF%B8%8F-installation--setup)
- [Docker Usage](#-docker-usage)
- [API Reference](#-api-reference)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Authors](#-authors)

---

## 🌐 Live Demo
> *Coming Soon — Deploying on Render.com*

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🏙️ **60+ Cities** | Multi-city support covering all Indian state capitals |
| 📍 **Dynamic Locality Areas** | City-specific sub-areas (e.g., Bandra in Mumbai, Whitefield in Bangalore) with variable pricing |
| 🔢 **Investment Score** | AI-driven score (1–10) based on city tier, locality, and amenities |
| ⭐ **Neighborhood Ratings** | Quality ratings: Safety, Connectivity, Schools, Lifestyle |
| 💳 **EMI Calculator** | Integrated mortgage estimator with affordability checker |
| 🔐 **User Authentication** | Secure login/signup with session management |
| 📊 **Prediction History** | Logged-in users can track past predictions |
| 🎫 **Help Ticket System** | Users can raise queries, admin can resolve them |
| 🌙 **Dark Mode** | Full dark/light mode toggle |
| 📄 **PDF Report** | Download prediction report as PDF |
| 🐳 **Dockerized** | Platform-independent deployment |
| ⚙️ **CI/CD Pipeline** | GitHub Actions: auto-test + Docker build on every push |

---

## 🚀 Tech Stack

### Backend
- **Python 3.9** — Core language
- **Flask** — Web framework & routing
- **PyMongo** — MongoDB driver for NoSQL data storage
- **Scikit-Learn** — Random Forest Regressor ML model
- **Gunicorn** — Production WSGI server

### Frontend
- **HTML5 / CSS3 / JavaScript** — Structure, styling, interactivity
- **Bootstrap 5** — Responsive grid & components
- **Custom Glassmorphism UI** — Premium design system

### DevOps
- **Docker** — Containerization
- **GitHub Actions** — CI/CD automation
- **Procfile** — Heroku/Render/Railway deployment

### Data & ML
- **Pandas / NumPy** — Data manipulation
- **MinMaxScaler** — Feature normalization
- **MongoDB** — Dynamic city & pricing data

---

## 📈 ML Pipeline Highlights

```
Raw Data (Kaggle - 318,851 rows)
    ↓
Data Cleaning (IQR Outlier Removal, Null Handling)
    ↓
Feature Engineering (MinMaxScaler, One-Hot Encoding)
    ↓
Model Selection (Linear Regression → KNN → Decision Tree → Random Forest)
    ↓
Hyperparameter Tuning (GridSearchCV)
    ↓
✅ Random Forest Regressor → 94% Train | 90% Test Accuracy
    ↓
Production API (Flask) + Feature Normalization Layer
```

**Key ML Choices:**
- **Why Random Forest?** Best accuracy, handles non-linear relationships, resistant to overfitting.
- **Why MinMaxScaler?** Preserves distribution shape while normalizing all features to [0, 1].
- **Why IQR?** Robust outlier removal without assuming data distribution.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────┐
│              USER BROWSER               │
│  (HTML + Bootstrap + Custom CSS + JS)   │
└─────────────────┬───────────────────────┘
                  │ HTTP Request
┌─────────────────▼───────────────────────┐
│            FLASK APPLICATION            │
│  ┌──────────────────────────────────┐   │
│  │  Routes: /, /rent, /compare,    │   │
│  │  /admin, /login, /dashboard     │   │
│  └──────────────┬───────────────────┘   │
│  ┌──────────────▼───────────────────┐   │
│  │  Business Logic Layer            │   │
│  │  (Prediction, EMI, Analytics)   │   │
│  └──────────────┬───────────────────┘   │
└─────────────────┼───────────────────────┘
                  │
       ┌──────────┴──────────┐
       ▼                     ▼
┌──────────────┐    ┌──────────────────┐
│   MONGODB    │    │  ML MODEL FILE   │
│  (Cities,    │    │ (Housing_Model   │
│   Users,     │    │  Random Forest)  │
│   Tickets)   │    └──────────────────┘
└──────────────┘
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- MongoDB (local) or MongoDB Atlas (cloud)
- Docker (optional)

### 1. Clone & Navigate
```bash
git clone https://github.com/tufailmir07/Housing_Price_Prediction.git
cd Housing_Price_Prediction
```

### 2. Set Environment Variables
Create a `.env` file in the root:
```env
FLASK_SECRET_KEY=your_super_secret_key
ADMIN_EMAIL=admin@yoursite.com
ADMIN_PASSWORD=your_admin_password
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Seed the Database
```bash
python migrate_to_mongo.py   # Populates MongoDB from JSON files
python seed_areas.py         # Adds locality-specific data
```

### 5. Run the Application
```bash
python app.py
```
Visit: [http://localhost:5000](http://localhost:5000)

---

---

## ☁️ Deployment on Render

To deploy this project on [Render](https://render.com), follow these steps:

1.  **Create a MongoDB Atlas Cluster**:
    - Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
    - Create a free cluster and a database named `housing_db`.
    - Get your connection string (e.g., `mongodb+srv://<user>:<password>@cluster0.mongodb.net/housing_db`).
2.  **Create a New Web Service on Render**:
    - Connect your GitHub repository.
    - Select **Python** as the environment.
    - Set **Build Command**: `pip install -r requirements.txt`
    - Set **Start Command**: `gunicorn app:app`
3.  **Configure Environment Variables**:
    - `FLASK_SECRET_KEY`: A secure random string.
    - `MONGO_URI`: Your MongoDB Atlas connection string.
    - `ADMIN_EMAIL`: Your admin email.
    - `ADMIN_PASSWORD`: Your admin password.
4.  **Seed the Database**:
    - Once deployed, you can use Render's "Shell" to run:
      ```bash
      python migrate_to_mongo.py
      python seed_areas.py
      ```

---

## 🐳 Docker Usage

```bash
# Build Image
docker build -t housing-app .

# Run Container
docker run -p 5000:5000 --env-file .env housing-app
```

---

## 📡 API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | `GET` | Home / Prediction Form |
| `/` | `POST` | Submit prediction, get result |
| `/api/city_areas/<city>` | `GET` | Get locality areas for a city |
| `/rent` | `GET/POST` | Rent estimation |
| `/compare` | `GET/POST` | Compare two properties |
| `/insights` | `GET` | Market insights page |
| `/login` | `GET/POST` | User login |
| `/signup` | `GET/POST` | User registration |
| `/dashboard` | `GET` | User prediction history |
| `/admin` | `GET` | Admin panel (admin only) |
| `/contact` | `GET/POST` | Submit help ticket |

---

## 🧪 Testing

```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v
```

**Test Coverage:**
- `tests/test_app.py` — API route response tests
- `tests/test_scaling.py` — MinMaxScaler normalization logic tests

---

## 📁 Project Structure

```
Housing_Price_Prediction/
├── app.py                    # Main Flask application
├── train_model.py            # ML model training script
├── migrate_to_mongo.py       # Database migration/seed script
├── seed_areas.py             # Locality areas seed script
├── check_mongo.py            # MongoDB connection validator
├── inspect_model.py          # Tool to inspect Random Forest features
├── requirements.txt          # Python dependencies
├── LICENSE                   # MIT License file
├── Procfile                  # Deployment config
├── Dockerfile                # Docker container config
├── .dockerignore
├── .env                      # Environment variables (not committed)
├── .github/
│   └── workflows/
│       └── main.yml          # CI/CD pipeline
├── static/
│   ├── style.css             # Main stylesheet
│   ├── enhancements.js       # UI interactivity & Dark mode
│   └── property_images/      # Property & city images
├── templates/
│   ├── index.html            # Home / Prediction page
│   ├── results.html          # Results page
│   ├── rent.html             # Rent estimation
│   ├── compare.html          # Property comparison
│   ├── admin.html            # Admin dashboard
│   ├── login.html            # Login page
│   ├── signup.html           # Signup page
│   ├── dashboard.html        # User dashboard
│   ├── contact.html          # Help / Contact page
│   └── about.html            # About the project
└── tests/
    ├── test_app.py           # Route tests
    └── test_scaling.py       # ML scaling tests
```

---

## 👥 Authors

| Name | Role |
|------|------|
| **Tufail Ahmad Mir** | Project Lead & Backend Architect |
| **Tejpartap Singh** | DevOps & Frontend Specialist |
| **Gaurav Uniyal** | Data Scientist & Analyst |

---

## 📜 License

This project is licensed under the **MIT License**.

---

*Developed with ❤️ for the Indian Real Estate Market (2026).*
