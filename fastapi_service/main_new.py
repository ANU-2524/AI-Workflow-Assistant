"""
FastAPI service main module.
Handles task management, Gmail integration, and voice commands.
"""

import logging
import logging.handlers
import os
from datetime import datetime
from typing import List, Optional, Dict

from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, Field, validator
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.automap import automap_base
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import spacy

from config import (
    CORS_ORIGINS, DATABASE_URL, FASTAPI_DEBUG, JWT_SECRET_KEY,
    KAFKA_BOOTSTRAP_SERVERS, LOG_FILE, LOG_LEVEL, 
    GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI
)
from auth import get_current_user, create_access_token
from db import SessionLocal
from models import EmailAuth

# ============================================
# LOGGING SETUP
# ============================================

def setup_logging():
    """Configure logging for the FastAPI service."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=15 * 1024 * 1024,  # 15MB
        backupCount=10
    )
    file_handler.setLevel(LOG_LEVEL)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logging()

# ============================================
# DATABASE SETUP
# ============================================

logger.info(f"Connecting to database: {DATABASE_URL.split('@')[1]}")

try:
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=FASTAPI_DEBUG
    )
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    logger.info(f"Database tables: {tables}")
    
    # Auto-reflection
    AutomapBase = automap_base()
    AutomapBase.prepare(engine, reflect=True)
    Task = AutomapBase.classes.tasks_task
    
except Exception as e:
    logger.error(f"Failed to connect to database: {str(e)}")
    raise

def get_db():
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

# ============================================
# NLP SETUP
# ============================================

try:
    nlp = spacy.load("en_core_web_sm")
    logger.info("Spacy model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load Spacy model: {str(e)}")
    nlp = None

# ============================================
# FASTAPI APP SETUP
# ============================================

app = FastAPI(
    title="AI Workflow Assistant API",
    description="API for task management, Gmail integration, and voice commands",
    version="1.0.0",
    debug=FASTAPI_DEBUG
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """Handle rate limit exceeded errors."""
    logger.warning(f"Rate limit exceeded for {request.client.host}")
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Rate limit exceeded"}
    )

# ============================================
# RESPONSE MODELS
# ============================================

class TaskBase(BaseModel):
    """Base model for task operations."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    due_date: datetime
    priority: str = Field(default="medium")
    status: str = Field(default="pending")
    is_completed: bool = Field(default=False)
    
    @validator('priority')
    def validate_priority(cls, v):
        if v not in ['low', 'medium', 'high']:
            raise ValueError('Invalid priority. Must be: low, medium, or high')
        return v
    
    @validator('status')
    def validate_status(cls, v):
        if v not in ['pending', 'in_progress', 'completed']:
            raise ValueError('Invalid status')
        return v
    
    @validator('title')
    def sanitize_title(cls, v):
        """Remove potentially dangerous characters."""
        if any(char in v for char in ['<', '>', '"', "'"]):
            raise ValueError('Title contains invalid characters')
        return v.strip()

class TaskCreate(TaskBase):
    """Model for creating tasks."""
    pass

class TaskOut(TaskBase):
    """Model for task responses."""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class CommandRequest(BaseModel):
    """Model for voice command requests."""
    command: str = Field(..., min_length=1, max_length=500)
    user_id: Optional[int] = None

class CommandResponse(BaseModel):
    """Model for voice command responses."""
    feedback: str
    action: Optional[str] = None
    url: Optional[str] = None
    contact: Optional[str] = None
    message: Optional[str] = None

# ============================================
# UTILITY FUNCTIONS
# ============================================

def extract_chat_intent(cmd: str) -> tuple:
    """
    Extract contact and message from chat command using NLP.
    
    Args:
        cmd: Voice command string
        
    Returns:
        Tuple of (contact_name, message_text)
    """
    if not nlp:
        logger.warning("Spacy model not available, using fallback extraction")
        return None, ""
    
    try:
        doc = nlp(cmd)
        contact = None
        message = ""
        
        for ent in doc.ents:
            if ent.label_ in ("PERSON", "ORG"):
                contact = ent.text
                break
        
        if contact:
            parts = cmd.split(contact)
            if len(parts) > 1:
                message = parts[1]
            else:
                for pfx in ["message", "tell", ":"]:
                    if pfx in cmd:
                        message = cmd.split(pfx, 1)[-1]
        
        return contact, message.strip()
    except Exception as e:
        logger.error(f"Error extracting chat intent: {str(e)}")
        return None, ""

# ============================================
# HEALTH CHECK ENDPOINT
# ============================================

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "AI Workflow Assistant API"
    }

# ============================================
# TASK ENDPOINTS
# ============================================

@app.get("/tasks", response_model=List[TaskOut], tags=["Tasks"])
@limiter.limit("30/minute")
async def get_tasks(
    request: Request,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Get all tasks for the current user.
    
    Requires: Valid JWT authentication
    Rate limit: 30 requests/minute
    """
    try:
        logger.info(f"Fetching tasks for user: {current_user.get('sub')}")
        tasks = db.query(Task).all()
        return tasks
    except Exception as e:
        logger.error(f"Error fetching tasks: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch tasks"
        )

@app.post("/tasks", response_model=TaskOut, tags=["Tasks"], status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def create_task(
    request: Request,
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Create a new task.
    
    Requires: Valid JWT authentication
    Rate limit: 10 requests/minute
    """
    try:
        logger.info(f"Creating task for user: {current_user.get('sub')}")
        
        db_task = Task()
        for key, value in task.dict().items():
            setattr(db_task, key, value)
        
        db_task.created_at = datetime.utcnow()
        db_task.updated_at = datetime.utcnow()
        
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        
        logger.info(f"Task created successfully: {db_task.id}")
        return db_task
        
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task"
        )

@app.put("/tasks/{task_id}", response_model=TaskOut, tags=["Tasks"])
@limiter.limit("10/minute")
async def update_task(
    request: Request,
    task_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Update an existing task.
    
    Requires: Valid JWT authentication
    """
    try:
        logger.info(f"Updating task {task_id} for user: {current_user.get('sub')}")
        
        db_task = db.query(Task).filter(Task.id == task_id).first()
        
        if not db_task:
            logger.warning(f"Task not found: {task_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        
        for key, value in task.dict().items():
            setattr(db_task, key, value)
        
        db_task.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_task)
        
        logger.info(f"Task {task_id} updated successfully")
        return db_task
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task {task_id}: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task"
        )

@app.delete("/tasks/{task_id}", tags=["Tasks"])
@limiter.limit("10/minute")
async def delete_task(
    request: Request,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Delete a task.
    
    Requires: Valid JWT authentication
    """
    try:
        logger.info(f"Deleting task {task_id}")
        
        db_task = db.query(Task).filter(Task.id == task_id).first()
        
        if not db_task:
            logger.warning(f"Task not found: {task_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        
        db.delete(db_task)
        db.commit()
        
        logger.info(f"Task {task_id} deleted successfully")
        return {"detail": "Task deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task"
        )

# ============================================
# VOICE COMMAND ENDPOINT
# ============================================

@app.post("/api/agentic-command", response_model=CommandResponse, tags=["Commands"])
@limiter.limit("20/minute")
async def agentic_command(
    request: Request,
    cmd_request: CommandRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    Process voice commands.
    
    Supports:
    - Chat: "Message [name]: [message]"
    - Browser: "Open YouTube/Google/Slack/etc"
    - Docs: "Create Google Document"
    
    Requires: Valid JWT authentication
    """
    try:
        cmd = cmd_request.command.lower().strip()
        logger.info(f"Processing command: {cmd}")
        
        contact, message = extract_chat_intent(cmd)
        
        if contact and message:
            logger.info(f"Chat command detected: {contact} - {message}")
            return CommandResponse(
                feedback=f"Messaged {contact}: {message}",
                action="chat",
                contact=contact,
                message=message
            )
        
        # Intent matching
        commands = {
            "youtube": ("https://www.youtube.com", "Opening YouTube!"),
            "google": ("https://www.google.com", "Opening Google search!"),
            "slack": ("https://slack.com/signin", "Opening Slack!"),
            "whatsapp": ("https://web.whatsapp.com", "Opening WhatsApp Web!"),
            "zoom": ("https://zoom.us", "Opening Zoom!"),
            "linkedin": ("https://linkedin.com", "Opening LinkedIn!"),
            "github": ("https://github.com", "Opening GitHub!"),
        }
        
        for keyword, (url, feedback) in commands.items():
            if keyword in cmd:
                logger.info(f"Action command detected: {keyword}")
                return CommandResponse(
                    feedback=feedback,
                    action="open",
                    url=url
                )
        
        if "create google document" in cmd or "open google document" in cmd:
            logger.info("Google Docs command detected")
            return CommandResponse(
                feedback="Creating Google Doc!",
                action="open",
                url="https://docs.new"
            )
        
        logger.info(f"Command not recognized: {cmd}")
        return CommandResponse(
            feedback=f"Command not recognized: {cmd}",
            action=None,
            url=None
        )
        
    except Exception as e:
        logger.error(f"Error processing command: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process command"
        )

# ============================================
# GMAIL ENDPOINTS (PLACEHOLDERS)
# ============================================

@app.get("/gmail/start", tags=["Gmail"])
async def gmail_start(user_id: int, current_user: Dict = Depends(get_current_user)):
    """Start Gmail OAuth flow."""
    logger.info(f"Initiating Gmail OAuth for user: {user_id}")
    # TODO: Implement Gmail OAuth flow
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Coming soon")

@app.get("/gmail/callback", tags=["Gmail"])
async def gmail_callback(request: Request, db: Session = Depends(get_db)):
    """Handle Gmail OAuth callback."""
    logger.info("Gmail callback received")
    # TODO: Implement callback handling
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Coming soon")

# ============================================
# STARTUP AND SHUTDOWN EVENTS
# ============================================

@app.on_event("startup")
async def startup_event():
    """Initialize app on startup."""
    logger.info("Application startup")
    logger.info(f"Debug mode: {FASTAPI_DEBUG}")
    logger.info(f"CORS origins: {CORS_ORIGINS}")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown."""
    logger.info("Application shutdown")
    try:
        engine.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("FASTAPI_HOST", "0.0.0.0"),
        port=int(os.getenv("FASTAPI_PORT", "9000")),
        reload=FASTAPI_DEBUG
    )
