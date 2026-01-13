from fastapi import FastAPI

from app.database import engine
from app.models import issue
from app.routes import issues_router, auth_router

app = FastAPI()

@app.get("/health")
def health_check():
  return {"status": "ok"}

issue.Base.metadata.create_all(bind=engine)

app.include_router(issues_router)
app.include_router(auth_router)
