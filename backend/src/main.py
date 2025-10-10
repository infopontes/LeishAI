from fastapi import FastAPI
from src.api.v1 import router_users, router_auth, router_roles

app = FastAPI(
    title="LeishAI API",
    version="0.1.0",
    description="API para o projeto LeishAI",
)

app.include_router(router_auth.router)
app.include_router(router_users.router)
app.include_router(router_roles.router)


@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz da API."""
    return {"message": "Welcome to LeishAI API"}
