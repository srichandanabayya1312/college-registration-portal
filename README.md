# 🎓 Smart College Portal

A full-stack web application built using Flask that simulates a real-world college management system. It provides separate dashboards and functionalities for Students, Faculty, and Admin with features like attendance tracking, digital library, announcements, and more.

---

## 🚀 Features

### 👨‍🎓 Student
  
* Register and login securely
* View personal dashboard
* 📊 View attendance (with name, roll number, branch, year)
* 📚 Access Digital Library (notes, PDFs)
* 📝 Submit assignments/notes (text + file upload)

---

### 👨‍🏫 Faculty

* Login to faculty dashboard
* 📅 Mark student attendance (Present/Absent)
* 📊 View attendance summary (Branch & Year wise)
* 📤 Upload notes (text + PDF/documents)
* 👀 Review student submissions

---

### 🛠️ Admin

* Login to admin dashboard
* 📢 Add announcements (visible to students)
* 📋 Manage student records
* 💰 Track fee details (extendable feature)
* 📄 Handle certificates (extendable)

---

## 🧠 Key Concepts Used

* Flask (Routing, Templates, Forms)
* SQLite Database
* SQL JOIN & Aggregations
* File Upload Handling
* Role-based Dashboards
* Responsive UI with CSS

---

## 🗄️ Database Design

### Students Table

* name
* email
* password
* course
* roll_no
* branch
* year

### Attendance Table

* name
* roll_no
* email
* date
* status

### Submissions Table

* title
* content
* file
* student_name
* email
* branch
* year
* roll_no

---

## 📊 Attendance System

* Faculty marks attendance using roll numbers
* Students can view their attendance
* Attendance summary grouped by:

  * Branch
  * Year
* Displays:

  * Total Present
  * Total Absent

---

## 📂 Project Structure

```
smart-college-portal/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── student_dashboard.html
│   ├── faculty_dashboard.html
│   ├── admin_dashboard.html
│   ├── mark_attendance.html
│   ├── view_attendance.html
│   ├── attendance_summary.html
│   ├── upload_notes.html
│   ├── notes.html
│   └── review_notes.html
│
├── static/
│   └── style.css
│
├── uploads/
│
├── database.db
├── app.py
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```
git clone https://github.com/srichandanabayya1312/college-registration-portal.git
```

### 2. Install dependencies

```
pip install flask
```

### 3. Run the application

```
python app.py
```

### 4. Open in browser

```
http://127.0.0.1:5000/
```

---

## 🎯 Future Enhancements

* 📊 Attendance percentage calculation
* 📈 Graphical analytics (charts)
* 🔐 Session-based authentication
* 📅 Date-wise attendance filtering
* 📥 Download reports (PDF/Excel)
* 🌐 Deployment (AWS / Render)

---

## 💡 Learning Outcomes

* Built a complete full-stack application
* Understood database design and relationships
* Implemented real-world features like file upload and analytics
* Improved debugging and problem-solving skills

---

## 👩‍💻 Author

**Sri Chandana Bayya**

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!

