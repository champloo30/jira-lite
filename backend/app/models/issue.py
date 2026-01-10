from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.database import Base

class Issue(Base):
  __tablename__ = 'issues'

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, nullable=False)
  description = Column(Text)
  status = Column(String, default='Open')
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
