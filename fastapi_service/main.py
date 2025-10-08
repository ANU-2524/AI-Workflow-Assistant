from sqlalchemy.orm import Session
from db import SessionLocal
# from models import Task
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
# from datetime import datetime
from google_auth_oauthlib.flow import Flow
from fastapi import FastAPI, Depends, HTTPException, Request
# from google_auth_oauthlib.flow import Flow
from fastapi import Body
from fastapi.responses import RedirectResponse
from googleapiclient.discovery import build
from fastapi.responses import RedirectResponse
from models import EmailAuth
from google.oauth2.credentials import Credentials
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import create_engine, inspect
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
inspector = inspect(engine)
print("Tables seen by SQLAlchemy:", inspector.get_table_names())
from sqlalchemy.ext.automap import automap_base

AutomapBase = automap_base()
AutomapBase.prepare(engine, reflect=True)
Task = AutomapBase.classes.tasks_task

CLIENT_SECRET_FILE = "creds/client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
REDIRECT_URI = "http://localhost:9000/gmail/callback"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],  # Add all frontend origins here!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = ""
    due_date: datetime
    priority: str = "medium"
    status: str = "pending"
    is_completed: bool = False 
    
class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    class Config:
        orm_mode = True
        
    #  TASKS API's 
@app.get("/tasks", response_model=List[TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

# POST (create a new task)

@app.post("/tasks", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task()  # automap class: no kwargs in constructor
    # Set all fields from input
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    # Set the NOT NULL required fields for the Django schema
    db_task.created_at = datetime.now()
    db_task.updated_at = datetime.now()
    # Example: if your table also needs user_id, set it here:
    # db_task.user_id = user_id
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task



# PUT (update a task)
@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(Task).get(task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.patch("/tasks/{task_id}")
def patch_task(task_id: int, payload: dict = Body(...), db: Session = Depends(get_db)):
    db_task = db.query(Task).get(task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in payload.items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return {"ok": True}

# DELETE (delete a task)
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).get(task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted"}

        # GMAIL API's
        
@app.get("/gmail/start")
def gmail_start(user_id: int):
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    auth_url, state = flow.authorization_url(access_type='offline', prompt='consent', include_granted_scopes='true')
    custom_state = f"{state}:{user_id}"
    url_with_custom_state = auth_url.replace(f"state={state}", f"state={custom_state}")
    return RedirectResponse(url_with_custom_state)


@app.get("/gmail/callback")
def gmail_callback(request: Request, db: Session = Depends(get_db)):
    raw_state = request.query_params.get("state", "")
    # Split on ":" to get real user_id
    try:
        oauth_state, user_id_str = raw_state.split(":")
        user_id = int(user_id_str)
    except Exception:
        user_id = 1  # fallback if something goes wrong

    code = request.query_params.get("code")
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    flow.fetch_token(code=code)
    creds = flow.credentials
    gmail = build('gmail', 'v1', credentials=creds)
    profile = gmail.users().getProfile(userId='me').execute()
    user_email = profile['emailAddress']

    # SAVE THE TOKENS for the CORRECT user_id!
    existing = db.query(EmailAuth).filter_by(user_id=user_id, email=user_email).first()
    if existing:
        db.delete(existing)
        db.commit()
    auth_row = EmailAuth(
        user_id=user_id,
        email=user_email,
        access_token=creds.token,
        refresh_token=getattr(creds, "refresh_token", ""),
        token_expiry=creds.expiry
    )
    db.add(auth_row)
    db.commit()
    
    return RedirectResponse(url="http://localhost:8000/?gmail_connected=1") 



@app.get("/gmail/list")
def gmail_list(user_id: int, db: Session = Depends(get_db)):
    emails = db.query(EmailAuth).filter_by(user_id=user_id).all()
    return [
        {"email": e.email, "token_expiry": e.token_expiry}
        for e in emails
    ]
    


@app.get('/gmail/fetch')
def gmail_fetch(user_id: int, db: Session = Depends(get_db)):
    auth_row = db.query(EmailAuth).filter_by(user_id=user_id).first()
    if not auth_row:
        return {'error': 'No Gmail linked for this user'}
    creds = Credentials(
        token=auth_row.access_token,
        refresh_token=auth_row.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id="931647934966-9rqai26slvjp81sreo9vudf2rl32qim3.apps.googleusercontent.com",
        client_secret="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"
    )
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', maxResults=10, labelIds=['INBOX']).execute()
    messages = results.get('messages', [])
    output = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        output.append({
            'id': msg['id'],
            'snippet': msg_data.get('snippet'),
            'payload': msg_data.get('payload', {}),
            'internalDate': msg_data.get('internalDate')
        })
    return output

KEYWORDS = ["assignment", "deadline", "project", "reminder", "action", "submit"]

@app.post('/gmail/suggest_tasks')
def gmail_suggest_tasks(user_id: int, db: Session = Depends(get_db)):
    print(f"=== DEBUGGING suggest_tasks for user_id={user_id} ===")
    
    auth_row = db.query(EmailAuth).filter_by(user_id=user_id).first()
    if not auth_row:
        print("ERROR: No Gmail linked for this user")
        return {'error': 'No Gmail linked for this user'}
    
    print(f"Found auth for email: {auth_row.email}")
    
    creds = Credentials(
        token=auth_row.access_token,
        refresh_token=auth_row.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id="931647934966-9rqai26slvjp81sreo9vudf2rl32qim3.apps.googleusercontent.com",
        client_secret="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"
    )
    
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', maxResults=10, labelIds=['INBOX']).execute()
    messages = results.get('messages', [])
    print(f"Found {len(messages)} messages in inbox")
    
    created_tasks = []
    for i, msg in enumerate(messages):
        print(f"\n--- Processing message {i+1}/{len(messages)} ---")
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        
        subject = ''
        payload_headers = msg_data.get('payload', {}).get('headers', [])
        for h in payload_headers:
            if h['name'] == "Subject":
                subject = h['value']
        snippet = msg_data.get('snippet', '')
        
        print(f"Subject: '{subject}'")
        print(f"Snippet: '{snippet[:100]}...'")
        
        # FORCE CREATE TASK (temporary debug)
        if True:  # This will match ALL emails
            print("FILTER: Matched (forced)")
            
            # Check if task already exists
            existing = db.query(Task).filter_by(title=subject, user_id=user_id, suggested=True).first()
            if existing:
                print(f"SKIP: Task already exists with title '{subject}'")
            else:
                print(f"CREATE: New suggested task")
                try:
                    new_task = Task(
                            user_id=user_id,
                            title=subject if subject else "No Subject",
                            description=snippet,
                            due_date=datetime.now(),
                            priority="medium",
                            status="pending",
                            is_completed=False,
                            suggested=True,
                            # add these:
                            created_at=datetime.now(),
                            updated_at=datetime.now(),
                        )
                    db.add(new_task)
                    created_tasks.append(subject)
                    print(f"SUCCESS: Added task '{subject}'")
                except Exception as e:
                    print(f"ERROR creating task: {e}")
        else:
            print("FILTER: No match")
    
    try:
        db.commit()
        print(f"COMMIT: Successfully saved {len(created_tasks)} tasks")
    except Exception as e:
        print(f"ERROR during commit: {e}")
    
    print(f"=== FINAL RESULT: {created_tasks} ===")
    suggested_rows = db.query(Task).filter_by(user_id=user_id, suggested=True).all()
    return {
        "suggested_tasks": [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description
            }
            for t in suggested_rows
        ]
    }
