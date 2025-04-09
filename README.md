# SimpleQuora

A simplified version of Quora built with Django allowing users to ask questions, provide answers. This project was created as an assignment for TransportSimple.

## Features

- **User Authentication**
  - User registration and login
  - Secure logout

- **Questions**
  - Post new questions
  - View questions posted by other users
  - Browse through question feed

- **Answers**
  - Answer questions posted by others
  - View answers from other users
  - Like/unlike answers

## Technology Stack

### Backend
- Python
- Django
- SQLite3

### Frontend
- HTML
- CSS
- JavaScript


## Setup Instructions

1. Clone the repository
```bash
git clone <repository-url>
cd SimpleQuora
```

2. Create a virtual environment
```bash
python -m venv workspace
source workspace/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run database migrations
```bash
python manage.py migrate
```

5. Start the development server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

