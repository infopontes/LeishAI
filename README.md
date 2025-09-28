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
ProjetoDoutorado
Gem personalizado

Mostrar raciocínio
Perfeita observação! É exatamente este o fluxo de trabalho ideal: fazemos um progresso, e imediatamente documentamos como replicar esse progresso. Isso torna o projeto imensamente mais fácil de ser retomado por você no futuro ou por qualquer outra pessoa.

Vamos atualizar a seção "Getting Started" do seu README.md.

Passo 1: Atualizar o README.md
Abra o arquivo README.md que está na raiz do projeto LeishAI e substitua todo o seu conteúdo por esta versão atualizada. A única mudança é na seção 5, que agora contém as instruções para rodar o backend.

Markdown

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

```bash
LeishAI/
├── README.md
├── backend              # FastAPI application
│   ├── main.py
│   ├── poetry.lock
│   └── pyproject.toml
├── frontend             # React application
└── ia_model             # Notebooks, model training scripts, and saved model
```


## 5. Getting Started

### Running the Backend Server

1.  Navigate to the backend directory:
    ```sh
    cd backend
    ```

2.  Activate the Poetry virtual environment:
    ```sh
    poetry shell
    ```

3.  Run the development server:
    ```sh
    uvicorn main:app --reload
    ```

4.  The API will be available at the following URLs:
    -   **API Root**: `http://127.0.0.1:8000/`
    -   **Interactive Docs (Swagger UI)**: `http://127.0.0.1:8000/docs`
    -   **Reference Docs (ReDoc)**: `http://127.0.0.1:8000/redoc`

---