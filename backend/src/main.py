from fastapi import FastAPI

# Create a FastAPI application instance
app = FastAPI(
    title="LeishAI API",
    description="API for Canine Leishmaniasis Prediction",
    version="0.1.0"
)

# Define an endpoint (route) for the API root "/"
# The method is GET, used to request data from a resource.
@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Welcome to the LeishAI API"}