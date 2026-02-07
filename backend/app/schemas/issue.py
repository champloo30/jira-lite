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
  description: Optional[str]
  status: Optional[str]

class IssueOut(BaseModel):
  id: int
  title: str
  description: str
  status: str
  created_by: int
  assigned_to: int | None

  class Config:
    from_attributes = True
