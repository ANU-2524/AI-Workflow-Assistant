# AI Workflow Assistant...

> **Transform your daily work into effortless productivity!** This intelligent assistant reads your emails, listens to your voice, and helps you manage tasks and collaborate with your team—all from one beautiful dashboard.
>
> Demo Vedio - https://drive.google.com/file/d/1LZqobOUxahzOquqxVM9eRkhaJnZ-N8Mf/view?usp=sharing 

## ✨ What Makes It Special...?

Say goodbye to task chaos! Our AI Workflow Assistant brings everything together:

- **🎤 Voice Commands** - Just speak! "Open YouTube", "Search Google", "Open Slack" - it gets done instantly
- **📧 Smart Email Integration** - Connect Gmail and auto-extract tasks from your emails
- **✍️ Quick Task Creation** - Add tasks with priority, due dates, and descriptions in seconds
- **💬 Real-time Team Chat** - Collaborate with teammates without switching apps
- **📊 Unified Dashboard** - See all your tasks, pending items, and team status at a glance
- **👥 Team Collaboration** - Connect with team members, send messages, and stay in sync
- **🔐 Google OAuth Login** - Secure, one-click authentication

---

## 🎯 Key Features

### 📱 Three Ways to Add Tasks

| Feature | Description |
|---------|-------------|
| **🎤 Voice Input** | Speak naturally and create tasks instantly |
| **⌨️ Manual Entry** | Type task details with priority and due date |
| **📧 Email Sync** | Automatically extract action items from emails |

### 🎛️ Smart Task Management

- **Task Overview** - See total tasks, pending items, and overdue reminders
- **Priority Levels** - High, Medium, Low categorization
- **Due Date Tracking** - Never miss a deadline
- **Status Updates** - Pending, In Progress, Completed
- **Suggested Tasks** - AI recommends tasks from your emails

### 👥 Team Collaboration Features

- **Team Members** - Connect with colleagues and build your team network
- **Connection Requests** - Send and receive collaboration invites
- **Direct Chat** - Real-time messaging with connected team members
- **Online Status** - See who's available at a glance

### 🗣️ Voice Assistant Commands

The magic mic supports:
- Open YouTube, Google, Slack
- Search Google, Create Google Docs
- Open WhatsApp Web, GitHub, LinkedIn, Zoom
- **And more commands coming soon!**

---

## 🏗️ System Architecture

```mermaid
graph TD
    A["👤 User Login"] -->|Google OAuth| B["🏠 Main Dashboard"]
    
    B --> C{"Input Method"}
    
    C -->|🎤 Voice| D["Voice Assistant<br/>Ready to Listen"]
    C -->|⌨️ Type| E["Add Task Form"]
    C -->|📧 Email| F["Gmail Integration"]
    
    D --> D1["Voice Commands<br/>YouTube, Google, Slack,<br/>WhatsApp, GitHub, LinkedIn"]
    D1 --> G
    
    E --> E1["Task Details<br/>Title, Description,<br/>Priority, Due Date"]
    E1 --> G
    
    F --> F1["📨 Sync Emails<br/>Connect Gmail"]
    F1 --> G["📋 Task Management<br/>Create & Store Tasks"]
    
    G --> H["📊 Dashboard Display<br/>Total Tasks | Pending | Overdue"]
    
    H --> I{"Task Status"}
    I -->|Pending| J["⏳ Show in Tasks List"]
    I -->|Completed| K["✅ Archive Task"]
    I -->|Overdue| L["🎯 Track Progress"]
    
    J --> N["Dashboard Updated"]
    K --> N
    L --> N
    
    B --> O["👥 Team Collaboration"]
    O --> O1["Team Members<br/>Connect & Manage"]
    O1 --> O2["Connection Requests<br/>Accept/Reject"]
    O2 --> O3["💬 Chat Dashboard<br/>Real-time Team Chat"]
    O3 --> O4["Real-time Updates<br/>Messages & Presence"]
    
    N --> P["🎯 Final Output<br/>Organized Workflow"]
    O4 --> P
    
    P --> Q["✨ Productivity Boost<br/>Manage tasks, collaborate,<br/>stay organized!"]
    
    style A fill:#6366f1,stroke:#4f46e5,stroke-width:2px,color:#fff
    style B fill:#06b6d4,stroke:#0891b2,stroke-width:2px,color:#fff
    style D fill:#8b5cf6,stroke:#7c3aed,stroke-width:2px,color:#fff
    style E fill:#8b5cf6,stroke:#7c3aed,stroke-width:2px,color:#fff
    style F fill:#8b5cf6,stroke:#7c3aed,stroke-width:2px,color:#fff
    style G fill:#ec4899,stroke:#be185d,stroke-width:2px,color:#fff
    style H fill:#f59e0b,stroke:#d97706,stroke-width:2px,color:#fff
    style I fill:#10b981,stroke:#059669,stroke-width:2px,color:#fff
    style O fill:#f43f5e,stroke:#e11d48,stroke-width:2px,color:#fff
    style O3 fill:#06b6d4,stroke:#0891b2,stroke-width:2px,color:#fff
    style Q fill:#14b8a6,stroke:#0d9488,stroke-width:2px,color:#fff
```

---

🚀 Quick Start

Prerequisites

Python 3.9+

Kafka, PostgreSQL

Docker & Docker Compose

Google API credentials

Gmail API access

Installation
1. Clone the Repository

bash
git clone https://github.com/ANU-2524/AI-Workflow-Assistant.git
cd AI-Workflow-Assistant

2. Set Up Environment Variables
Create a .env file (see .env.example for keys like DATABASE_URL, DJANGO_SECRET_KEY, DEBUG).

3. Start with Docker

bash
docker-compose up --build
Django : 8000

FastAPI: 9000

PostgreSQL & Kafka included!

4. Access the App
Open your browser:

text
http://localhost:8000

5. Login with Google

Click “Login with Google”

Authorize access (for smart task extraction from Gmail!)

👀 Usage Examples
Voice:
“Hey, open Slack” → Slack opens in your browser

Email:
“Please review the project proposal by Friday” → Task auto-created, due Friday!

Teamwork:
Dashboard → Connect → Chat → Type or speak to message your team, live!

Quick Tasks:
Add tasks with title, priority, due date, status—all tracked in the dashboard

🛠️ Tech Stack
Backend:

FastAPI / Django (Python 3.9+), PostgreSQL

Google OAuth, Gmail API 


Infra:

Docker, Docker Compose...

🤝 Contributing
Fork & feature branch

Code & commit

Pull request!

Follow PEP8 & ESLint, write simple commit messages

Feature ideas needed:

More voice commands

Mobile app

Slack & Teams integration

Advanced analytics & suggestions


🙋 Need help?
GitHub Issues

Raise Issue...

🎉 Made with 💖 by Anu... !!
