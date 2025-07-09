# TodoApp 📝

**TodoApp** is a simple and powerful task management API built with **FastAPI** and **Python**.  
It includes user authentication via **JWT tokens**, role-based access control, and admin endpoints for managing users and tasks.

---

## 🚀 Features

- ✅ CRUD operations for managing to-do tasks.
- 👤 User registration and login using JWT.
- 🔐 Role-based authorization (e.g., `user`, `admin`).
- ⚙️ Admin endpoints to manage users and all tasks.
- 📄 FastAPI auto-generated interactive docs.

---

## 🛠 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [Python 3.10+](https://www.python.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/) or Tortoise ORM
- [PostgreSQL](https://www.postgresql.org/) or SQLite
- [PyJWT](https://pyjwt.readthedocs.io/)

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/todoapp.git
cd todoapp

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
⚙️ Environment Configuration
Create a .env file in the root directory:

env
Copy
Edit
DATABASE_URL=sqlite:///./todoapp.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
▶️ Running the App
bash
Copy
Edit
uvicorn app.main:app --reload
Visit the interactive docs at http://localhost:8000/docs

🧪 API Overview
🔐 Auth
Method	Endpoint	Description
POST	/auth/register	Register a new user
POST	/auth/login	Obtain JWT token

📋 Tasks (Protected)
Method	Endpoint	Description
GET	/tasks	List user tasks
POST	/tasks	Create new task
PUT	/tasks/{task_id}	Update a task
DELETE	/tasks/{task_id}	Delete a task

⚙️ Admin (Admin Only)
Method	Endpoint	Description
GET	/admin/users	List all users
GET	/admin/tasks	View all tasks
DELETE	/admin/users/{id}	Delete a user

🧰 Project Structure
pgsql
Copy
Edit
todoapp/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   └── admin.py
│   ├── core/
│   │   ├── security.py
│   │   └── config.py
│   └── database.py
├── .env
├── requirements.txt
└── README.md
🛡️ License
This project is licensed under the MIT License.

🙌 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

👨‍💻 Author
Made with ❤️ by [Your Name or GitHub Handle]