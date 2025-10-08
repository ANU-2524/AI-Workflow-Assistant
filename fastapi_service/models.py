from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
Base = declarative_base()

class Task():
    __tablename__ = "tasks_task"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey('auth_user.id'))
    priority = Column(String(10))
    status = Column(String(15))
    is_completed = Column(Boolean, default=False)
    suggested = Column(Boolean, default=False) 

class EmailAuth(Base) :
    __tablename__ = "email_auth"
    id = Column(Integer , primary_key=True)
    user_id = Column(Integer , nullable = False)
    email = Column(String , nullable = False)
    access_token = Column(String , nullable = False)
    refresh_token = Column(String , nullable = True)
    token_expiry = Column(DateTime , nullable = True)
    created_at = Column(DateTime , default = datetime.utcnow)
    
