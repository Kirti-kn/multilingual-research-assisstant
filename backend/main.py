from fastapi import FastAPI
from backend.routes import router
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_credentials.json"

app = FastAPI()
app.include_router(router)

@app.get("/")
def read_root():
    return {"message":"FastAPI backend is running!"}
