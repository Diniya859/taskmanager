## Features

- ✅ **User Authentication** (JWT tokens)
- 👥 **Role-based permissions** (SuperAdmin/Admin/User)
- 📋 **Task management** 
- 📊 **Completion reports**
- 🔒 **Admin dashboard** 
- 📱 **REST API** for integration

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: SQLite 
- **Authentication**: JWT (JSON Web Tokens)
- **Frontend**: Django Templates (Admin panel)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/taskmanager.git
   cd taskmanager
2.Create and activate virtual environment:

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

3.Install dependencies:

bash
pip install -r requirements.txt
4.python manage.py makemigrations and migrate
5.python manage.py createsuperuser
