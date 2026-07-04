# MindPulse AI

MindPulse AI is an AI-powered student productivity and wellness prediction system that helps students analyze their academic habits, predict productivity, identify burnout risks, and receive personalized AI-driven guidance. The application combines Machine Learning, Artificial Intelligence, and Web Development to provide a complete student wellness platform.

---

## Features

- User Registration and Secure Login
- Student Productivity Prediction using Machine Learning
- Personalized Dashboard
- Wellness Score Calculation
- Burnout Risk Analysis
- Distraction Index Analysis
- Interactive What-If Simulator
- AI Coach (Powered by Ollama & Llama 3.2)/later changed to gemini due to deployment
- AI Insights (Powered by Google Gemini)
- AI Roadmap Generation
- Secure Password Hashing
- MySQL Database Integration
- Session-Based Authentication

---

## Technology Stack

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Jinja2
- Chart.js

### Backend
- Python
- Flask

### Database
- MySQL
- MySQL Connector for Python

### Machine Learning
- Scikit-learn
- Random Forest Regressor
- Joblib

### Artificial Intelligence
- Google Gemini API
- Ollama
- Llama 3.2
- Prompt Engineering

### Security
- Flask Sessions
- Werkzeug Security

---

## Project Structure

```text
MindPulseAI/
│
├── AI_CHAT/
├── model/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
├── app.py
├── db.py
├── gemini_helper.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

1. Clone the repository

```bash
git clone https://github.com/keerty318/MindPulse-AI.git
```

2. Navigate to the project folder

```bash
cd MindPulse-AI
```

3. Install the required packages

```bash
pip install -r requirements.txt
```

4. Configure your MySQL database.

5. Add your Google Gemini API Key.

6. Make sure Ollama is installed and the Llama 3.2 model is available.

7. Run the application

```bash
python app.py
```

---

## Future Enhancements

- Assessment History
- Progress Tracking
- Email Verification
- Password Reset
- Admin Dashboard
- PDF Report Generation
- Cloud Deployment

---

## Author

**Keertana Priya A**