# LeishAI: AI-Powered Leishmaniasis Detection System

## 1. Project Objective

This project aims to build a full-stack web application to assist in the diagnosis of canine leishmaniasis. It allows for the registration of animal service data, stores this information in a relational database, and uses a trained Machine Learning model to provide real-time infection predictions.

This repository is intended to serve as a reference model for the scientific community, demonstrating a practical application of AI in veterinary health.

## 2. Core Components

The system is divided into three main parts:

-   **Backend (FastAPI)**: A robust API responsible for business logic, data management (CRUD operations), and serving the ML model.
-   **Frontend (React)**: A modern, responsive user interface for data entry, visualization of results, and interaction with the system.
-   **AI Model (Scikit-learn / XGBoost)**: A machine learning model trained on animal clinical data to predict the likelihood of leishmaniasis.

## 3. Technology Stack

-   **Backend**: Python, FastAPI, SQLAlchemy, PostgreSQL
-   **Frontend**: JavaScript, React, Axios, Recharts
-   **Machine Learning**: Pandas, Scikit-learn, Joblib
-   **DevOps**: Docker, Git

## 4. Project Structure

LeishAI/
├── backend/            # FastAPI application
│   └── .gitkeep
├── frontend/           # React application
│   └── .gitkeep
└── ia_model/           # Notebooks, model training scripts, and saved model
└── .gitkeep

## 5. Getting Started

*(This section will be filled in as the project develops)*

---