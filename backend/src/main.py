from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from src.core.config import settings
from src.core.limiter import limiter

from src.api.v1 import (
    router_animals,
    router_assessments,
    router_auth,
    router_breeds,
    router_owners,
    router_roles,
    router_users,
)

app = FastAPI(
    title="LeishAI API",
    version="0.1.0",
    description="API para o projeto LeishAI",
)

print(f"🧪 TESTING mode: {settings.TESTING}")


# Ativar o Limiter na aplicação APENAS se não estiver em modo de teste
if not settings.TESTING:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Configuração do CORS
origins = ["http://localhost", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão dos Routers
app.include_router(router_auth.router)
app.include_router(router_users.router)
app.include_router(router_roles.router)
app.include_router(router_breeds.router)
app.include_router(router_owners.router)
app.include_router(router_animals.router)
app.include_router(router_assessments.router)


@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz da API."""
    return {"message": "Welcome to the LeishAI API"}
