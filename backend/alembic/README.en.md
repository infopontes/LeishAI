# 🗄️ Alembic Database Migrations

This directory contains the database migration scripts for the **LeishAI** project, managed by **Alembic**.  
Alembic provides a structured and version-controlled way to handle database schema changes.

## 🔧 Common Commands

All commands should be executed from the root directory of the **backend** project.

### 🧩 Generate a New Migration

After making changes to the SQLAlchemy models in `src/db/models/`, generate a new migration script.  
Alembic will compare the models with the current database state and generate the necessary changes.

```bash
poetry run alembic revision --autogenerate -m "A short, descriptive message about the changes"
```

⚠️ **Important:** Always review the script generated in `alembic/versions/` to ensure it accurately reflects the intended changes before applying it.

### 🚀 Apply Migrations

To apply all pending migrations and update the database schema to the latest version:

```bash
poetry run alembic upgrade head
```

### ⏪ Revert Migrations (Downgrade)

To revert a migration, downgrade to a specific version or by one step.  
For example, to revert the last applied migration:

```bash
poetry run alembic downgrade -1
```

### 📜 View Migration History

To view the history of all migrations and identify the current database schema version:

```bash
poetry run alembic history
```
