from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class Issue(Base):
  __tablename__ = 'issues'

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, nullable=False)
  description = Column(Text)
  status = Column(String, default='open')
  created_by = Column(Integer, ForeignKey('users.id'))
  assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)

  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  owner = relationship("User")
  assignee = relationship("User", foreign_keys=[assigned_to])
  comments = relationship("Comment", back_populates="issue", cascade="all, delete-orphan")
