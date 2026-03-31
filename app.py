from flask import Flask, render_template, request, redirect, send_from_directory
import sqlite3
import os

app = Flask(__name__)

# Upload folder config
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_db():
    return sqlite3.connect("database.db")


# ================= DATABASE SETUP =================

conn = sqlite3.connect("database.db")
cur = conn.cursor()



# Create submissions table
cur.execute("""
CREATE TABLE IF NOT EXISTS submissions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
content TEXT,
file TEXT,
student_name TEXT,
email TEXT,
branch TEXT,
year TEXT,
roll_no TEXT
)
""")

# Create attendance table (updated structure)
cur.execute("""
CREATE TABLE IF NOT EXISTS attendance(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
roll_no TEXT,
email TEXT,
date TEXT,
status TEXT
)
""")

conn.commit()
conn.close()

# =================================================


@app.route('/')
def home():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM announcements")
    announcements = cur.fetchall()

    conn.close()

    return render_template("index.html", announcements=announcements)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        course = request.form['course']
        roll_no = request.form['roll_no']
        branch = request.form['branch']
        year = request.form['year']

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO students(name,email,password,course,roll_no,branch,year)
        VALUES(?,?,?,?,?,?,?)
        """, (name,email,password,course,roll_no,branch,year))

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template("register.html")


@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM students WHERE email=? AND password=?",
            (email, password)
        )

        user = cur.fetchone()

        conn.close()

        if user:
            return redirect('/student-dashboard')
        else:
            return "Invalid credentials"

    return render_template("login.html")

@app.route('/student-dashboard')
def student_dashboard():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM announcements")
    announcements = cur.fetchall()

    conn.close()

    return render_template("student_dashboard.html", announcements=announcements)

@app.route('/faculty-login', methods=['GET','POST'])
def faculty_login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        # Simple hardcoded login (for now)
        if username == "faculty" and password == "123":
            return redirect('/faculty-dashboard')
        else:
            return "Invalid Faculty Login"

    return render_template("faculty_login.html")


@app.route('/faculty-dashboard')
def faculty_dashboard():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT name,email,course FROM students")
    students = cur.fetchall()

    conn.close()

    return render_template("faculty_dashboard.html")


@app.route('/admin-login', methods=['GET','POST'])
def admin_login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        print(username, password)

        # Simple admin login
        if username == "admin" and password == "123":
            return redirect('/admin-dashboard')
        else:
            return "Invalid Admin Login"

    return render_template("admin_login.html")


@app.route('/admin-dashboard')
def admin_dashboard():

    conn = get_db()
    cur = conn.cursor()

    search = request.form.get('search')

    if search:
        cur.execute("SELECT name,email,course FROM students WHERE name LIKE ?", ('%' + search + '%',))
    else:
        cur.execute("SELECT name,email,course FROM students")

    students = cur.fetchall()

    conn.close()

    return render_template("admin_dashboard.html")




@app.route('/dashboard')
def dashboard():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT name,email,course FROM students")
    students = cur.fetchall()

    conn.close()

    return render_template("dashboard.html", students=students)

@app.route('/faculty-profile')
def faculty_profile():
    return render_template("faculty_profile.html")

@app.route('/add-announcement', methods=['GET','POST'])
def add_announcement():

    if request.method == 'POST':
        msg = request.form['message']

        conn = get_db()
        cur = conn.cursor()

        cur.execute("INSERT INTO announcements(message) VALUES(?)", (msg,))
        conn.commit()
        conn.close()

        return redirect('/admin-dashboard')

    return render_template("add_announcement.html")

@app.route('/upload-notes', methods=['GET','POST'])
def upload_notes():

    if request.method == 'POST':

        title = request.form['title']
        content = request.form['content']

        file = request.files['file']
        filename = file.filename

        if filename != "":
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        else:
            filename = ""

        conn = get_db()
        cur = conn.cursor()

        cur.execute("INSERT INTO notes(title,content,file) VALUES(?,?,?)",
                    (title, content, filename))

        conn.commit()
        conn.close()

        return redirect('/faculty-dashboard')

    return render_template("upload_notes.html")

@app.route('/notes')
def view_notes():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM notes")
    notes = cur.fetchall()

    conn.close()

    return render_template("notes.html", notes=notes)


from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/submit-notes', methods=['GET','POST'])
def submit_notes():

    if request.method == 'POST':

        title = request.form['title']
        content = request.form['content']
        file = request.files['file']

        filename = file.filename

        if filename != "":
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # 👉 TEMP student details (later we can use session)
        student_name = request.form['name']
        email = request.form['email']
        branch = request.form['branch']
        year = request.form['year']
        roll_no = request.form['roll']

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO submissions(title,content,file,student_name,email,branch,year,roll_no)
        VALUES(?,?,?,?,?,?,?,?)
        """, (title,content,filename,student_name,email,branch,year,roll_no))

        conn.commit()
        conn.close()

        return redirect('/student-dashboard')

    return render_template("submit_notes.html")

@app.route('/review-notes')
def review_notes():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM submissions")
    data = cur.fetchall()

    conn.close()

    return render_template("review_notes.html", data=data)

@app.route('/mark-attendance', methods=['GET','POST'])
def mark_attendance():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT name, roll_no, email FROM students")
    students = cur.fetchall()

    if request.method == 'POST':

        from datetime import date
        today = str(date.today())

        for student in students:
            name = student[0]
            roll = student[1]
            email = student[2]

            status = request.form.get(roll)

            # DEBUG PRINT
            print("DEBUG:", name, roll, status)

            cur.execute("""
            INSERT INTO attendance(name, roll_no, email, date, status)
            VALUES(?,?,?,?,?)
            """, (name, roll, email, today, status))

        conn.commit()   # ✅ VERY IMPORTANT

    conn.close()

    return render_template("mark_attendance.html", students=students)

@app.route('/view-attendance')
def view_attendance():

    conn = get_db()
    cur = conn.cursor()

    roll_no = "101"   # must match student

    cur.execute("""
    SELECT attendance.name, attendance.roll_no,
       students.branch, students.year,
       attendance.date, attendance.status
    FROM attendance
    JOIN students ON attendance.roll_no = students.roll_no
    WHERE attendance.roll_no=?
    """, (roll_no,))

    data = cur.fetchall()

    print("VIEW DATA:", data)

    conn.close()

    return render_template("view_attendance.html", data=data)


@app.route('/attendance-summary')
def attendance_summary():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT students.branch, students.year,
           SUM(CASE WHEN attendance.status='Present' THEN 1 ELSE 0 END) as present_count,
           SUM(CASE WHEN attendance.status='Absent' THEN 1 ELSE 0 END) as absent_count
    FROM attendance
    JOIN students ON attendance.roll_no = students.roll_no
    GROUP BY students.branch, students.year
    """)

    data = cur.fetchall()

    conn.close()

    return render_template("attendance_summary.html", data=data)

app.run(debug=True)