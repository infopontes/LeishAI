# 🗄️ Migrações de Banco de Dados com Alembic

Este diretório contém os scripts de migração do banco de dados para o projeto **LeishAI**, geridos pelo [Alembic](https://alembic.sqlalchemy.org/).
O Alembic fornece uma maneira de lidar com as alterações no schema do banco de dados de forma estruturada e com controlo de versão.

---

## 🔧 Comandos Comuns

Todos os comandos devem ser executados a partir do diretório raiz do projeto `backend`.

---

### 🧩 Gerar uma Nova Migração

Após fazer alterações nos modelos **SQLAlchemy** em `src/db/models/`, gere um novo script de migração.  
O Alembic irá comparar os modelos com o estado atual do banco de dados e gerar as alterações necessárias.

```bash
poetry run alembic revision --autogenerate -m "Uma mensagem curta e descritiva sobre as alterações"
```

> ⚠️ **Importante:** Sempre revise o script gerado em `alembic/versions/` para garantir que ele reflete com precisão as alterações pretendidas antes de aplicá-lo.

---

### 🚀 Aplicar Migrações

Para aplicar todas as migrações pendentes e atualizar o schema do banco de dados para a versão mais recente:

```bash
poetry run alembic upgrade head
```

---

### ⏪ Reverter Migrações (Downgrade)

Para reverter uma migração, faça o downgrade para uma versão específica ou apenas um passo anterior.  
Por exemplo, para reverter a última migração aplicada:

```bash
poetry run alembic downgrade -1
```

---

### 📜 Verificar o Histórico de Migrações

Para ver o histórico de todas as migrações e identificar a versão atual do schema do banco de dados:

```bash
poetry run alembic history
```
