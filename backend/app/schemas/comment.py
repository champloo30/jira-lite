from pydantic import BaseModel
from datetime import datetime

class CommentBase(BaseModel):
  content: str

class CommentCreate(CommentBase):
  pass

class CommentOut(CommentBase):
  id: int
  user_id: int
  issue_id: int
  created_at: datetime

  class Config:
    from_attributes = True
