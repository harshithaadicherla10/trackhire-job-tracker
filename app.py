from flask import Flask, render_template, request, redirect, session
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash
import os

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- DATABASE CONNECTION ----------
def get_db():
    return psycopg2.connect(os.environ.get("postgresql://trackhire_db_user:lQwGCiH0m0eMTAvsd4z9saz0Zlqlidko@dpg-d7e935a8qa3s73bqvru0-a/trackhire_db"))

# ---------- HOME ----------
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Get search inputs
    search = request.args.get('search', '')
    status = request.args.get('status', '')

    query = """
        SELECT jobs.*, users.username
        FROM jobs
        JOIN users ON jobs.user_id = users.id
        WHERE 1=1
    """

    params = []

    # User filter
    if session['role'] != 'admin':
        query += " AND jobs.user_id = %s"
        params.append(session['user_id'])

    # Search filter
    if search:
        query += " AND jobs.company LIKE %s"
        params.append(f"%{search}%")

    # Status filter
    if status:
        query += " AND jobs.status = %s"
        params.append(status)

    cursor.execute(query, tuple(params))
    jobs = cursor.fetchall()

    # 🔥 ---------- Stats ----------
    stats = {
        "Applied": 0,
        "Interview": 0,
        "Offer": 0,
        "Rejected": 0
    }

    for job in jobs:
        if job['status'] in stats:
            stats[job['status']] += 1

    conn.close()

    return render_template(
        'index.html',
        jobs=jobs,
        role=session['role'],
        stats=stats   
    )

# ---------- ABOUT ----------
@app.route('/about')
def about():
    return render_template('about.html')

# ---------- CONTACT ----------
@app.route('/contact')
def contact():
    return render_template('contact.html')

# ---------- ADD JOB ----------
@app.route('/add', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
    "INSERT INTO jobs (company, role, status, date_applied, user_id) VALUES (%s, %s, %s, %s, %s)",
    (
        request.form['company'],
        request.form['role'],
        request.form['status'],
        request.form['date'],
        session['user_id']
    )
)

        conn.commit()
        conn.close()

        flash("Job added successfully!", "success")

        return redirect('/')

    return render_template('add.html')

# ---------- EDIT JOB ----------

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_job(id):
    if 'user_id' not in session:
        return redirect('/login')
    
    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # ALWAYS fetch job first (for both GET & POST)
    cursor.execute("SELECT * FROM jobs WHERE id=%s", (id,))
    job = cursor.fetchone()

    # SECURITY CHECK (VERY IMPORTANT)
    if session['role'] != 'admin' and job['user_id'] != session['user_id']:
        return "Access Denied"

    # ---------- UPDATE ----------
    if request.method == 'POST':
        cursor.execute(
            "UPDATE jobs SET company=%s, role=%s, status=%s, date_applied=%s WHERE id=%s",
            (
                request.form['company'],
                request.form['role'],
                request.form['status'],
                request.form['date'],
                id
            )
        )
        conn.commit()
        conn.close()

        flash("Job updated successfully!", "warning")

        return redirect('/')

    # ---------- SHOW EDIT PAGE ----------
    conn.close()
    return render_template('edit.html', job=job)

# ---------- DELETE JOB ----------
@app.route('/delete/<int:id>')
def delete_job(id):
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db()
    cursor = conn.cursor()

    # Admin can delete ANY
    if session['role'] == 'admin':
        cursor.execute("DELETE FROM jobs WHERE id=%s", (id,))
    else:
        cursor.execute(
            "DELETE FROM jobs WHERE id=%s AND user_id=%s",
            (id, session['user_id'])
        )

    conn.commit()
    conn.close()

    flash("Job deleted successfully!", "danger")
    
    return redirect('/')

# ---------- REGISTER ----------

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()

        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        cursor.execute(
            "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
            (username, email, password, "user")
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

# ---------- LOGIN ----------

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['role'] = user['role']
            return redirect('/')

        return "Invalid Credentials"

    return render_template('login.html')

# ---------- LOGOUT ----------

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )