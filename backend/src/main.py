from fastapi import FastAPI
from src.api.v1 import router_users, router_auth

# Create a FastAPI application instance
app = FastAPI(
    title="LeishAI API",
    description="API for Canine Leishmaniasis Prediction",
    version="0.1.0",
)

# routers na aplicação principal
app.include_router(router_auth.router)

# Inclui o router de usuários na aplicação principal
app.include_router(router_users.router)


# Define an endpoint (route) for the API root "/"
# The method is GET, used to request data from a resource.
@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Welcome to the LeishAI API"}
