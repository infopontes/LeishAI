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
📦 Project Root
├── README.md
│
├── backend/                        # FastAPI backend project
│   ├── alembic/                    # Database migrations (Alembic)
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/               # Migration scripts
│   │       ├── 53bf8d2f70e6_create_user_table.py
│   │       ├── 15b1870dd74c_add_owner_and_animal_models.py
│   │       ├── ...
│   │       └── fe8353f6c31b_add_full_name_and_institution_to_user_.py
│   │
│   ├── alembic.ini                 # Alembic configuration file
│   ├── dataset.csv                 # Dataset used for testing or seeding
│   ├── docker-compose.yml          # Docker setup for backend services
│   ├── ml_models/                  # Pre-trained ML models
│   │   ├── leish_model_v1.joblib
│   │   └── training_columns_v1.joblib
│   │
│   ├── scripts/                    # Database seeding and utilities
│   │   ├── seed.py
│   │   └── seeds/
│   │       ├── seed_breeds.py
│   │       ├── seed_from_csv.py
│   │       └── seed_users.py
│   │
│   ├── src/                        # Core backend source code
│   │   ├── main.py                 # FastAPI entry point
│   │   │
│   │   ├── api/v1/                 # API routes (versioned)
│   │   │   ├── dependencies.py
│   │   │   ├── router_animals.py
│   │   │   ├── router_assessments.py
│   │   │   ├── router_auth.py
│   │   │   ├── router_breeds.py
│   │   │   ├── router_owners.py
│   │   │   ├── router_prediction.py
│   │   │   ├── router_roles.py
│   │   │   └── router_users.py
│   │   │
│   │   ├── core/                   # Core configurations and security
│   │   │   ├── config.py
│   │   │   ├── limiter.py
│   │   │   └── security.py
│   │   │
│   │   ├── db/                     # Database access and models
│   │   │   ├── database.py
│   │   │   ├── crud/               # CRUD operations
│   │   │   │   ├── crud_animal.py
│   │   │   │   ├── crud_assessment.py
│   │   │   │   ├── crud_breed.py
│   │   │   │   ├── crud_owner.py
│   │   │   │   ├── crud_role.py
│   │   │   │   └── crud_user.py
│   │   │   └── models/             # SQLAlchemy models
│   │   │       ├── animal.py
│   │   │       ├── assessment.py
│   │   │       ├── base.py
│   │   │       ├── breed.py
│   │   │       ├── enums.py
│   │   │       ├── owner.py
│   │   │       ├── role.py
│   │   │       └── user.py
│   │   │
│   │   ├── ml/                     # ML service integration
│   │   │   └── prediction_service.py
│   │   │
│   │   └── schemas/                # Pydantic schemas
│   │       ├── animal.py
│   │       ├── assessment.py
│   │       ├── breed.py
│   │       ├── owner.py
│   │       ├── prediction.py
│   │       ├── role.py
│   │       └── user.py
│   │
│   ├── tests/                      # Unit and integration tests
│   │   ├── conftest.py
│   │   ├── test_main.py
│   │   ├── test_users_db.py
│   │   └── api/
│   │       ├── test_animals_api.py
│   │       ├── test_assessments_api.py
│   │       ├── test_breeds_api.py
│   │       ├── test_owners_api.py
│   │       ├── test_prediction_api.py
│   │       ├── test_users_api.py
│   │       └── test_utils.py
│   │
│   ├── poetry.lock
│   └── pyproject.toml
│
├── frontend/                       # Placeholder for frontend project
│
└── ia_model/                       # Machine Learning workspace
    ├── data/                       # Raw datasets
    │   └── raw/leish_dataset.csv
    │
    ├── models/                     # Trained ML models
    │   ├── leish_model_v1.joblib
    │   └── training_columns_v1.joblib
    │
    ├── notebooks/                  # Jupyter notebooks (EDA, training, etc.)
    │   ├── 01-EDA.ipynb
    │   ├── 02-Model_Training.ipynb
    │   ├── 03-Advanced_Imbalanced_Learning.ipynb
    │   ├── 04-Undersampling_Experiment.ipynb
    │   └── 05-SVM_Experiments.ipynb
    │
    ├── src/                        # Python modules for ML workflow
    │   ├── data/data_loader.py
    │   ├── models/
    │   └── preprocessing/
    │
    ├── scripts/                    # Utility scripts for data/model handling
    ├── poetry.lock
    └── pyproject.toml
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
