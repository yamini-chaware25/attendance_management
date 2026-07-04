from flask import Flask, render_template, request, redirect, flash, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = "attendance_secret"

# -------------------------------
# MySQL Connection
# -------------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="attendance_db"
)

cursor = db.cursor(dictionary=True)

# -------------------------------
# Dashboard
# -------------------------------
# -------------------------------
# Dashboard
# -------------------------------
@app.route("/")
def dashboard():

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM students")
    total_students = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM teachers")
    total_teachers = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM subjects")
    total_subjects = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM attendance")
    total_attendance = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM attendance WHERE status='Present'")
    total_present = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM attendance WHERE status='Absent'")
    total_absent = cursor.fetchone()["total"]

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_teachers=total_teachers,
        total_subjects=total_subjects,
        total_attendance=total_attendance,
        total_present=total_present,
        total_absent=total_absent
    )


# -------------------------------
# View Students
# -------------------------------
@app.route("/students")
def students():

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students ORDER BY id DESC")
    students = cursor.fetchall()

    return render_template("students.html", students=students)

# -------------------------------
# Add Student
# -------------------------------
@app.route("/add_student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        roll = request.form["roll_no"]
        name = request.form["name"]
        gender = request.form["gender"]
        email = request.form["email"]
        phone = request.form["phone"]
        branch = request.form["branch"]
        year = request.form["year"]

        sql = """
        INSERT INTO students
        (roll_no, name, gender, email, phone, branch, year)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """

        values = (roll, name, gender, email, phone, branch, year)

        cursor.execute(sql, values)
        db.commit()

        flash("Student Added Successfully!")

        return redirect("/students")

    return render_template("add_student.html")

# -------------------------------
# Add Student
# -------------------------------



# ==========================================
# ADD THESE TWO ROUTES HERE
# ==========================================

@app.route("/edit_student/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        roll_no = request.form["roll_no"]
        name = request.form["name"]
        gender = request.form["gender"]
        email = request.form["email"]
        phone = request.form["phone"]
        branch = request.form["branch"]
        year = request.form["year"]

        cursor.execute("""
            UPDATE students
            SET roll_no=%s,
                name=%s,
                gender=%s,
                email=%s,
                phone=%s,
                branch=%s,
                year=%s
            WHERE id=%s
        """, (roll_no, name, gender, email, phone, branch, year, id))

        db.commit()
        flash("Student Updated Successfully!")

        return redirect(url_for("students"))

    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cursor.fetchone()

    return render_template("edit_student.html", student=student)


@app.route("/delete_student/<int:id>")
def delete_student(id):

    cursor = db.cursor()

    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    db.commit()

    flash("Student Deleted Successfully!")

    return redirect(url_for("students"))

# ==========================================
# THEN YOUR ATTENDANCE ROUTE STARTS HERE
# ==========================================

# -------------------------------
# Attendance
# -------------------------------
@app.route("/attendance", methods=["GET", "POST"])
def attendance():

    cursor = db.cursor(dictionary=True)

    # Load all students
    cursor.execute("SELECT id, roll_no, name FROM students")
    students = cursor.fetchall()

    if request.method == "POST":

        student_id = request.form["student_id"]
        date = request.form["date"]
        status = request.form["status"]

        sql = """
        INSERT INTO attendance (student_id,Date, status)
        VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (student_id, date, status))
        db.commit()

        flash("Attendance Saved Successfully!")

        return redirect(url_for("attendance"))

    return render_template("attendance.html", students=students)

# -------------------------------
# Teachers
# -------------------------------
# -------------------------------
# Teachers
# -------------------------------
@app.route("/teachers", methods=["GET", "POST"])
def teachers():

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        name = request.form["teacher_name"]
        subject = request.form["subject"]
        phone = request.form["phone"]
        email = request.form["email"]

        cursor.execute("""
        INSERT INTO teachers(teacher_name, subject,phone,email)
        VALUES(%s,%s,%s,%s)
        """,(name,subject,phone,email))

        db.commit()
        flash("Teacher Added Successfully!")

        return redirect(url_for("teachers"))

    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()

    return render_template("teachers.html", teachers=teachers)




# -------------------------------
# Subjects
# -------------------------------
# -------------------------------
# Subjects
# -------------------------------
@app.route("/subjects", methods=["GET","POST"])
def subjects():

    cursor = db.cursor(dictionary=True)

    if request.method=="POST":

        subject_name=request.form["subject_name"]
        subject_code=request.form["subject_code"]

        cursor.execute("""
        INSERT INTO subjects(subject_name,subject_code)
        VALUES(%s,%s)
        """,(subject_name,subject_code))

        db.commit()
        flash("Subject Added Successfully!")

        return redirect(url_for("subjects"))

    cursor.execute("SELECT * FROM subjects")
    subjects=cursor.fetchall()

    return render_template("subjects.html",subjects=subjects)

# -------------------------------
# Reports
# -------------------------------
# -------------------------------
# Reports
# -------------------------------
# -------------------------------
# Reports
# -------------------------------
@app.route("/reports")
def reports():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            attendance.id,
            students.roll_no,
            students.name,
            attendance.date,
            attendance.status
        FROM attendance
        INNER JOIN students
        ON attendance.student_id = students.id
        ORDER BY attendance.date DESC
    """)

    reports = cursor.fetchall()

    return render_template("reports.html", reports=reports)


# ===============================
# DELETE ROUTES
# ===============================

@app.route("/delete_teacher/<int:id>")
def delete_teacher(id):

    cursor = db.cursor()

    cursor.execute("DELETE FROM teachers WHERE id=%s", (id,))
    db.commit()

    flash("Teacher Deleted Successfully!")

    return redirect(url_for("teachers"))


@app.route("/delete_subject/<int:id>")
def delete_subject(id):

    cursor = db.cursor()

    cursor.execute("DELETE FROM subjects WHERE id=%s", (id,))
    db.commit()

    flash("Subject Deleted Successfully!")

    return redirect(url_for("subjects"))


@app.route("/delete_report/<int:id>")
def delete_report(id):

    cursor = db.cursor()

    cursor.execute("DELETE FROM attendance WHERE id=%s", (id,))
    db.commit()

    flash("Attendance Record Deleted Successfully!")

    return redirect(url_for("reports"))


# -------------------------------
# Run
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)

