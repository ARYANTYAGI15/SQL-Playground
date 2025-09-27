from fastapi import FastAPI
from app.database import engine
from app import models
from app.api import query,ask

app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=engine)

app.include_router(query.router, prefix="/api", tags=["Query"])
app.include_router(ask.router, prefix="/api", tags=["Ask"])
@app.get("/")
def root():
    return {"message": "Hello, DB is connected!"}
