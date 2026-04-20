# 🚀 TrackHire – Job Application Tracker

A full-stack web application to track, manage, and analyze job applications efficiently. Built with Flask and PostgreSQL, and deployed on Render.

---

## 🌐 Live Demo

🔗 https://trackhire-feru.onrender.com/

---

## 📌 Features

* 👤 User Authentication (Register / Login)
* 🔐 Secure password hashing
* 🧑‍💼 Role-based access (Admin & User)
* 📊 Dashboard with application insights (Pie Chart)
* 🗂️ Track job applications (Applied, Interview, Offer, Rejected)
* 🔍 Search & filter jobs
* ✏️ Edit and delete job entries
* 📱 Responsive UI (Mobile + Desktop)
* ☁️ Deployed on cloud (Render)

---

## 🛠️ Tech Stack

### 💻 Backend

* Python
* Flask
* Gunicorn

### 🗄️ Database

* PostgreSQL (Render Hosted)

### 🎨 Frontend

* HTML
* CSS
* Bootstrap
* JavaScript
* Chart.js

### 🚀 Deployment

* Render (Web Service + PostgreSQL)

---

## 🧠 Key Highlights

* Integrated Flask with PostgreSQL using `psycopg2`
* Implemented environment variables for secure configuration
* Production deployment using Gunicorn
* Role-based system with dynamic UI rendering
* Real-time analytics using charts

---

## 📂 Project Structure

```bash
trackhire-job-tracker/
│
├── app.py
├── requirements.txt
├── templates/
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions (Local)

### 1. Clone the repository

```bash
git clone https://github.com/harshithaadicherla10/trackhire-job-tracker.git
cd trackhire-job-tracker
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

```bash
DATABASE_URL=your_postgresql_url
SECRET_KEY=your_secret_key
```

### 5. Run the app

```bash
python app.py
```

---

## 🗄️ Database Schema

### Users Table

* id (Primary Key)
* username
* email
* password
* role (admin/user)

### Jobs Table

* id (Primary Key)
* company
* role
* status
* date_applied
* user_id

---

## 🚀 Deployment (Render)

* Connected GitHub repository
* Configured environment variables
* Used Gunicorn for production server
* Integrated PostgreSQL database

---

## 📈 Future Enhancements

* 📅 Job reminders & notifications
* 📊 Advanced analytics dashboard
* 🔔 Email alerts
* 📎 Resume upload & tracking
* 🌙 Dark mode

---

## 👩‍💻 Author

Harshitha Adicherla

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
