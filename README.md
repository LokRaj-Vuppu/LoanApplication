# Loan Application Management System 💳

A full-stack **loan management web application** built with **Flask**. Users can register, log in, submit loan applications, and track their application status. Admins can review and approve/reject applications.

---

## Features

- **User Authentication** — Registration, login, logout via Flask-Security
- **Role-based Access Control** — Separate user and admin roles
- **Loan Application** — Users submit loan requests with personal and financial details
- **Application Status** — Users can view pending/approved/rejected status
- **Admin Dashboard** — Admins review applications and update status
- **Form Validation** — WTForms with server-side validation
- **Responsive UI** — Bootstrap + jQuery frontend

---

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Flask | Python web framework |
| SQLAlchemy | ORM for database operations |
| PostgreSQL | Relational database |
| Flask-Security | User authentication & authorization |
| Flask-Login | Session management |
| WTForms | Form handling and validation |
| Bootstrap 4 | Responsive CSS framework |
| jQuery | Frontend interactivity |
| Jinja2 | Template engine |

---

## Project Structure

```
LoanApplication/
├── loanapplication/
│   ├── __init__.py       # Flask app initialization
│   ├── models.py         # SQLAlchemy models (User, Loan)
│   ├── forms.py          # WTForms (RegistrationForm, LoanForm)
│   ├── routes.py         # Flask routes/views
│   ├── templates/        # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── apply_loan.html
│   │   ├── loan_status.html
│   │   └── admin_dashboard.html
│   └── static/           # CSS, JS, images
├── run.py                # Application entry point
└── README.md
```

---

## Database Schema

### Users Table
```
id (PK)
email (unique)
password (hashed)
first_name
last_name
role (user/admin)
```

### Loans Table
```
id (PK)
user_id (FK)
loan_amount
loan_purpose
monthly_income
employment_status
credit_score
status (pending/approved/rejected)
application_date
```

---

## Getting Started

### Prerequisites

- Python 3.7+
- PostgreSQL

### Installation

```bash
git clone https://github.com/LokRaj-Vuppu/LoanApplication.git
cd LoanApplication

# Create virtual environment
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

# Install dependencies
pip install Flask Flask-SQLAlchemy Flask-Security Flask-Login WTForms psycopg2-binary
```

### Database Setup

```bash
# Create PostgreSQL database
createdb loan_application

# Update database URI in loanapplication/__init__.py
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/loan_application'
```

### Run Migrations

```bash
python
>>> from loanapplication import db
>>> db.create_all()
>>> exit()
```

### Run the Application

```bash
python run.py
```

Visit: **http://localhost:5000**

---

## Usage

### For Users

1. **Register** — Create an account with email and password
2. **Login** — Access your dashboard
3. **Apply for Loan** — Fill out the loan application form
4. **Check Status** — View pending/approved/rejected applications

### For Admins

1. **Login** — Use admin credentials
2. **Dashboard** — View all pending loan applications
3. **Review** — Approve or reject applications
4. **Manage Users** — View registered users

---

## Security Features

- Password hashing with Flask-Security (bcrypt)
- Role-based access control (@roles_required decorator)
- CSRF protection with WTForms
- Session management with Flask-Login
- SQL injection prevention via SQLAlchemy ORM

---

## API Endpoints (Example Routes)

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page |
| `/register` | GET, POST | User registration |
| `/login` | GET, POST | User login |
| `/logout` | GET | Logout |
| `/apply` | GET, POST | Submit loan application |
| `/status` | GET | View application status |
| `/admin/dashboard` | GET | Admin dashboard (admin only) |
| `/admin/review/<id>` | POST | Approve/reject loan (admin only) |

---

## Future Enhancements

- Email notifications for application status changes
- File upload for income proof/ID documents
- Loan eligibility calculator
- Payment schedule tracker
- Export applications to PDF/Excel
- REST API for mobile app integration

---

## Author

**LokRaj Vuppu** — [GitHub](https://github.com/LokRaj-Vuppu)
