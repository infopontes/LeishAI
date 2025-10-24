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
    router_users,  # Mantendo a sua estrutura atual
    router_prediction,
)

app = FastAPI(
    title="LeishAI API",
    version="0.1.0",
    description="API for the LeishAI project",
)

# Enable Limiter in the application
# Mantendo a sua abordagem com settings.TESTING
if not settings.TESTING:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion of Routers (mantendo a sua estrutura atual)
app.include_router(router_auth.router)
app.include_router(router_users.router)  # Mantido
app.include_router(router_roles.router)
app.include_router(router_breeds.router)
app.include_router(router_owners.router)
app.include_router(router_animals.router)
app.include_router(router_assessments.router)
app.include_router(router_prediction.router)


@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz da API."""
    return {"message": "Welcome to the LeishAI API"}
