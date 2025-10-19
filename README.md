# 🧬 LeishAI Project 🔬🐾

**LeishAI** aims to provide an AI-powered tool to assist veterinarians in the diagnosis of canine leishmaniasis based on clinical signs.  
This repository contains the **backend API** and the **machine learning model development** components.

---

## ✨ Features

### 🧩 Backend (FastAPI API)

- **RESTful API:** Provides endpoints for managing core entities:
  - Users & Authentication (JWT-based)
  - Roles & Permissions (Admin, Veterinarian, Coordinator)
  - Owners
  - Breeds
  - Animals
  - Clinical Assessments
- **AI Prediction Endpoint:** Integrates the trained machine learning model via a `/predict` endpoint to provide diagnosis predictions based on input clinical data and confidence scores.
- **Data Validation:** Uses Pydantic for robust request and response validation.
- **Database Management:** SQLAlchemy ORM with PostgreSQL and Alembic for schema migrations.
- **Asynchronous:** Built with FastAPI for high performance.
- **Security:**
  - Password hashing (`passlib` with `bcrypt`).
  - Role-Based Access Control (RBAC).
  - Rate limiting (`slowapi`) on authentication and registration.
  - CORS configured for frontend integration.
- **Testing:** Comprehensive Pytest suite with ~94% code coverage.
- **Dependency Management:** Managed with Poetry.
- **Data Seeding:** Includes scripts to populate the database with initial roles, users, breeds, and imported CSV data.
- **Dockerized Database:** Easy setup with Docker Compose.

---

### 🤖 IA Model (Machine Learning)

- **Data Pipeline:** Extracts, cleans, and preprocesses data from the backend PostgreSQL database.
- **Exploratory Data Analysis (EDA):** Jupyter notebooks for feature visualization and distribution analysis.
- **Preprocessing:** Handles missing values and performs One-Hot Encoding for categorical data.
- **Model Experimentation:** Trained and evaluated:
  - Logistic Regression
  - Random Forest
  - XGBoost
  - Support Vector Machine (SVM)
- **Imbalanced Data Handling:** Explored `class_weight`, SMOTE, and RandomUnderSampler.
- **Hyperparameter Tuning:** Used `GridSearchCV`, focusing on the **recall** metric.
- **Final Model:** **Balanced Logistic Regression** selected as best-performing model.
- **Artifact Saving:** Saves `.joblib` model and training columns for consistent inference.
- **Dependency Management:** Managed with Poetry.

---

## 🛠️ Tech Stack

| Area | Technologies |
|------|---------------|
| **Backend** | Python, FastAPI, SQLAlchemy, Alembic, PostgreSQL, Docker, Poetry, Pydantic, Passlib, SlowAPI |
| **Machine Learning** | Python, Pandas, Scikit-learn, XGBoost, Imbalanced-learn, Jupyter Lab, Joblib, Poetry |
| **Testing** | Pytest, Pytest-Cov |
| **Linting/Formatting** | Ruff |

---

## 📂 Project Structure

```
LeishAI/
├── backend/                     # FastAPI backend source
│   ├── alembic/                 # Alembic migrations
│   ├── ml_models/               # Saved ML model artifacts
│   ├── scripts/                 # Data seeding scripts
│   ├── src/                     # API, DB, Schemas, Core logic
│   ├── tests/                   # Pytest suite
│   ├── .env.example             # Example environment variables
│   ├── docker-compose.yml
│   └── pyproject.toml
│
├── ia_model/                    # ML model development
│   ├── data/                    # Raw & processed datasets
│   ├── models/                  # Trained model artifacts
│   ├── notebooks/               # Jupyter notebooks (EDA & training)
│   ├── src/                     # ML utilities and data loaders
│   └── pyproject.toml
│
└── README.md                    # This file
```

---

## 🚀 Getting Started

### 🧰 Prerequisites

- Python >= 3.12  
- Poetry (`pip install poetry`)  
- Docker & Docker Compose  

---

### ⚙️ Setup

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd LeishAI
   ```

2. **Setup Backend**
   ```bash
   cd backend
   poetry install
   cp .env.example .env
   # Edit .env with your PostgreSQL credentials
   ```

3. **Setup IA Model**
   ```bash
   cd ../ia_model
   poetry install
   ```

---

### ▶️ Running the Application

1. **Start the Database**
   ```bash
   cd backend
   docker-compose up -d
   ```

2. **Apply Migrations**
   ```bash
   poetry run alembic upgrade head
   ```

3. **Seed the Database**
   ```bash
   poetry run task seed
   ```

4. **Run the Backend Server**
   ```bash
   poetry run task run
   ```
   The API will be available at:  
   🔗 `http://127.0.0.1:8000`  
   Swagger Docs: `http://127.0.0.1:8000/docs`

---

## ✅ Running Tests

To run all backend tests with coverage:

```bash
cd backend
poetry run task test
```

---

## 💾 Database Migrations

Database schema changes are managed using **Alembic**.  
See: [`backend/alembic/README.md`](backend/alembic/README.md)

---

## 🌱 Data Seeding

The backend includes scripts to populate the database with initial roles, users, breeds, and dataset imports.

```bash
cd backend
poetry run task seed
```

---

## 🧠 Machine Learning Workflow

Located in `ia_model/`:

1. **Extract Data**
   ```bash
   poetry run task loader
   ```
   Saves data to:  
   `ia_model/data/raw/leish_dataset.csv`

2. **Explore & Train**
   ```bash
   poetry run task notebook
   ```
   Open Jupyter Lab and explore:
   - `01-EDA.ipynb`
   - `02-Model_Training.ipynb`

   ✅ Final selected model: **Balanced Logistic Regression**

---

## 📚 API Documentation

Once running, interactive documentation is available at:  
🔗 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

**LeishAI** — Artificial Intelligence assisting veterinary diagnostics 🧠🐶  
Developed with ❤️ using **FastAPI**, **Poetry**, and **Scikit-learn**.
