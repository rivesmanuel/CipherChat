# AI Chat Agent API

A conversational AI agent built with Flask and PostgreSQL that handles multi-turn conversations through RESTful endpoints, featuring conversation management, message persistence, and modular architecture.

## Features

- REST API endpoint for chat interactions
- Persistent conversation storage in PostgreSQL
- Multi-turn conversation support with context awareness
- OpenAI GPT integration for intelligent responses
- Modular Flask Blueprint architecture

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **AI**: OpenAI API
- **ORM**: SQLAlchemy
- **Migrations**: Flask-Migrate

## Prerequisites

- Python 3.8+
- PostgreSQL
- OpenAI API key

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ItzRayoo23/agente_ia.git
   cd agente_ia
2. **Create virtual environment**

   ```bash
   python -m venv env
   source env/bin/activate  # Windows: env\Scripts\activate
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables**

   Create a .env file in the project root:
   
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   FLASK_APP=run.py
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=postgresql://username:password@localhost:5432/dbname
   ```
5. **Run the application**

   ```bash
   python run.py
   ```
   Server runs at http://localhost:5000

### Project Structure
```bash
agente_ia/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── api/
│   │   └── chat.py
│   └── services/
│       └── openai_service.py
├── migrations/
├── .env
├── .gitignore
├── requirements.txt
└── run.py
```
### Author
ItzRayoo23
