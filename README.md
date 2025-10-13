# 🚀 AI Workflow Assistant

> **Transform your daily work into effortless productivity!** This intelligent assistant reads your emails, listens to your voice, and helps you manage tasks and collaborate with your team—all from one beautiful dashboard.

![AI Workflow Assistant](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)
![Python](https://img.shields.io/badge/Backend-Python-3776ab?style=flat-square&logo=python)
![React](https://img.shields.io/badge/Frontend-React-61dafb?style=flat-square&logo=react)

---

## ✨ What Makes It Special?

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
- **Instant Notifications** - Get notified when teammates are online

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

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- Docker & Docker Compose
- Google API credentials
- Gmail API access

### Installation

**1. Clone the Repository**

```bash
git clone https://github.com/your-username/ai-workflow-assistant.git
cd ai-workflow-assistant
```

**2. Set Up Environment Variables**

Create a `.env` file in the root directory:

```env
# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Gmail API
GMAIL_API_KEY=your_gmail_api_key

# Backend
BACKEND_URL=http://localhost:8000
BACKEND_PORT=8000

# Frontend
FRONTEND_URL=http://localhost:3000
FRONTEND_PORT=3000

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ai_workflow

# JWT Secret
JWT_SECRET=your_jwt_secret_key
```

**3. Start with Docker**

```bash
docker-compose up --build
```

This will start:
- Backend API (Port 8000)
- Frontend (Port 3000)
- PostgreSQL Database
- Redis (for real-time features)

**4. Access the Application**

Open your browser and navigate to:

```
http://localhost:3000
```

**5. Login with Google**

Click "Login with Google" and authorize the application to access your:
- Google Account information
- Gmail inbox (for task extraction)

---

## 📖 Usage Examples

### Example 1: Voice Command

```
User: "Hey, open Slack"
Assistant: Opens Slack in your browser
```

### Example 2: Email Task Extraction

```
Incoming Email: "Please review the project proposal by Friday"
Assistant: Auto-creates task "Review project proposal" with due date: Friday
```

### Example 3: Team Collaboration

```
Dashboard → Team Collaboration → Connect with Vinita
→ Chat → Send message: "Hey, how are you?"
→ Real-time message delivered with online status
```

### Example 4: Task Management

```
Add Task:
- Title: "Complete quarterly report"
- Description: "Q3 sales and performance metrics"
- Priority: High
- Due Date: Oct 20, 2025
- Status: Pending
```

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI / Django
- **Language**: Python 3.9+
- **APIs**: Google OAuth 2.0, Gmail API, Google Docs API
- **Database**: PostgreSQL
- **Real-time**: WebSocket / Socket.io
- **Authentication**: JWT

### Frontend
- **Framework**: React 18+
- **UI Library**: Tailwind CSS
- **State Management**: Redux / Context API
- **Real-time**: Socket.io Client
- **Voice**: Web Speech API / Annoy.js

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Cloud Deployment**: Render / Heroku / AWS
- **CDN**: Cloudflare (optional)

---

## 📋 Project Structure

```
ai-workflow-assistant/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── tasks.py
│   │   │   ├── teams.py
│   │   │   └── chat.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   │   ├── team.py
│   │   │   └── message.py
│   │   ├── services/
│   │   │   ├── gmail_service.py
│   │   │   ├── voice_service.py
│   │   │   └── task_service.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── VoiceAssistant.jsx
│   │   │   ├── TaskForm.jsx
│   │   │   ├── TeamCollaboration.jsx
│   │   │   └── ChatDashboard.jsx
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🔐 Security Features

- **Google OAuth 2.0** - Secure authentication
- **JWT Tokens** - Secure session management
- **HTTPS Only** - Encrypted data transmission
- **CORS Protection** - Cross-origin request security
- **Environment Variables** - Sensitive data protection
- **Rate Limiting** - API abuse prevention
- **Input Validation** - XSS and injection prevention

---

## 🌐 Deployment

### Deploy on Render

1. Push your repository to GitHub
2. Create a new Render account at https://render.com
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Add environment variables
6. Deploy!

### Deploy on Heroku

```bash
heroku login
heroku create your-app-name
git push heroku main
heroku config:set GOOGLE_CLIENT_ID=xxx
heroku config:set GOOGLE_CLIENT_SECRET=xxx
```

### Deploy on AWS

- Use **EC2** for compute
- Use **RDS** for PostgreSQL
- Use **ElastiCache** for Redis
- Use **S3** for file storage
- Use **CloudFront** for CDN

---

## 📸 Screenshots

### Dashboard
![Dashboard](https://via.placeholder.com/600x400?text=Dashboard)

### Voice Assistant
![Voice Assistant](https://via.placeholder.com/600x400?text=Voice+Assistant)

### Team Collaboration
![Team Collaboration](https://via.placeholder.com/600x400?text=Team+Collaboration)

### Chat Interface
![Chat Interface](https://via.placeholder.com/600x400?text=Chat+Interface)

---

## 🐛 Troubleshooting

### Issue: Gmail not connecting?
```
Solution: 
1. Check if Gmail API is enabled in Google Cloud Console
2. Verify GMAIL_API_KEY in .env file
3. Click "Request Access" button on dashboard
4. Re-authenticate with Google
```

### Issue: Voice commands not working?
```
Solution:
1. Check browser microphone permissions
2. Ensure you're using HTTPS (required for Web Speech API)
3. Try a different browser (Chrome/Edge recommended)
4. Check console for error messages
```

### Issue: Real-time chat not updating?
```
Solution:
1. Check WebSocket connection in browser DevTools
2. Verify Redis is running: docker ps
3. Restart the backend: docker-compose restart
4. Clear browser cache and refresh
```

---

## 🤝 Contributing

We love contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch** `git checkout -b feature/amazing-feature`
3. **Make your changes** and commit them `git commit -m 'Add amazing feature'`
4. **Push to the branch** `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 (Python) and ESLint (JavaScript) standards
- Write descriptive commit messages
- Add tests for new features
- Update documentation as needed
- Be respectful and constructive

### Areas We Need Help With

- [ ] Additional voice commands
- [ ] Mobile app (React Native)
- [ ] Advanced analytics
- [ ] Calendar integration
- [ ] Slack integration
- [ ] Microsoft Teams support

---

## 📚 Documentation

- [API Documentation](./docs/API.md)
- [Setup Guide](./docs/SETUP.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)
- [Contributing Guide](./docs/CONTRIBUTING.md)
- [Troubleshooting](./docs/TROUBLESHOOTING.md)

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙋 Support

Need help? We're here for you!

- **GitHub Issues** - Report bugs or request features
- **Email** - support@aiworkflow.com
- **Discord Community** - Join our community server
- **Twitter** - Follow us for updates @AIWorkflow

---

## 🎓 Roadmap

### Version 1.1 (Q4 2025)
- [ ] Mobile app (iOS & Android)
- [ ] Advanced task filtering and search
- [ ] Task templates and automation
- [ ] Email scheduling

### Version 1.2 (Q1 2026)
- [ ] Slack integration
- [ ] Calendar sync
- [ ] Analytics dashboard
- [ ] AI-powered task suggestions

### Version 1.3 (Q2 2026)
- [ ] Microsoft Teams integration
- [ ] Advanced automation workflows
- [ ] Team performance analytics
- [ ] Custom voice model training

---

## ❤️ Built With Love

Made with ❤️ by the AI Workflow Assistant team. We believe productivity should be effortless, intelligent, and collaborative.

**Enjoying the project? Give us a ⭐ on GitHub!**

---

## 🎉 Acknowledgments

- Google APIs for authentication and services
- The React and FastAPI communities
- All our amazing contributors
- You for using AI Workflow Assistant!

---

**Ready to revolutionize your workflow? [Get Started Now!](#quick-start)** 🚀