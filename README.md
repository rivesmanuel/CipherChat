# AI Chat Agent API
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success)](https://github.com/ItzRayoo23/agente_ia)

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
