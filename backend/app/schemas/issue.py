from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class IssueCreate(BaseModel):
  title: str
  description: str | None = None

class IssueResponse(BaseModel):
  id: int
  status: str
  create_at: datetime

class Config:
  orm_mode = True

class IssueUpdate(BaseModel):
  title: Optional[str]
  descriptional: Optional[str]
  status: Optional[str]

