from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class Comment(Base):
  __tablename__ = "comments"

  id = Column(Integer, primary_key=True, index=True)
  content = Column(Text, nullable=False)

  issue_id = Column(Integer, ForeignKey("issue.id", ondelete="CASCADE"), nullable=False)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  issue = relationship("Issue", back_populates="comments")
  author = relationship("User")
