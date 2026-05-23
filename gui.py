import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import datetime

connection = sqlite3.connect("students.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    grade TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    date TEXT,
    status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject TEXT,
    marks REAL,
    total_marks REAL,
    exam_month TEXT
)
""")

connection.commit()

root = tk.Tk()
root.title("Bright Mind Attendance System")
root.geometry("1000x700")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

student_tab = tk.Frame(notebook)
attendance_tab = tk.Frame(notebook)
exam_tab = tk.Frame(notebook)
report_tab = tk.Frame(notebook)

notebook.add(student_tab, text="Students")
notebook.add(attendance_tab, text="Attendance")
notebook.add(exam_tab, text="Exams")
notebook.add(report_tab, text="Reports")

name_entry = tk.Entry(student_tab, width=40)
name_entry.pack(pady=5)
name_entry.insert(0, "Student Name")

grade_entry = tk.Entry(student_tab, width=40)
grade_entry.pack(pady=5)
grade_entry.insert(0, "Grade/Class")

student_tree = ttk.Treeview(student_tab, columns=("ID", "Name", "Grade"), show="headings")
student_tree.heading("ID", text="ID")
student_tree.heading("Name", text="Name")
student_tree.heading("Grade", text="Grade")
student_tree.pack(fill="both", expand=True)


def load_students():

    for item in student_tree.get_children():
        student_tree.delete(item)

    cursor.execute("SELECT * FROM students")

    rows = cursor.fetchall()

    for row in rows:
        student_tree.insert("", "end", values=row)


def add_student():

    name = name_entry.get()
    grade = grade_entry.get()

    cursor.execute(
        "INSERT INTO students (name, grade) VALUES (?, ?)",
        (name, grade)
    )

    connection.commit()

    messagebox.showinfo("Success", "Student Added")

    load_students()


add_button = tk.Button(student_tab, text="Add Student", command=add_student)
add_button.pack(pady=10)

attendance_tree = ttk.Treeview(attendance_tab, columns=("ID", "Name", "Grade"), show="headings")
attendance_tree.heading("ID", text="ID")
attendance_tree.heading("Name", text="Name")
attendance_tree.heading("Grade", text="Grade")
attendance_tree.pack(fill="both", expand=True)

attendance_date = tk.Entry(attendance_tab, width=30)
attendance_date.pack(pady=5)
attendance_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

status_var = tk.StringVar()
status_var.set("P")

status_menu = ttk.Combobox(attendance_tab, textvariable=status_var, values=["P", "A"])
status_menu.pack(pady=5)


def load_attendance_students():

    for item in attendance_tree.get_children():
        attendance_tree.delete(item)

    cursor.execute("SELECT * FROM students")

    rows = cursor.fetchall()

    for row in rows:
        attendance_tree.insert("", "end", values=row)


def mark_attendance():

    selected = attendance_tree.focus()

    if selected == "":
        messagebox.showerror("Error", "Select Student")
        return

    data = attendance_tree.item(selected)

    student_id = data["values"][0]

    date = attendance_date.get()

    status = status_var.get()

    cursor.execute(
        "INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
        (student_id, date, status)
    )

    connection.commit()

    messagebox.showinfo("Success", "Attendance Saved")


attendance_button = tk.Button(attendance_tab, text="Save Attendance", command=mark_attendance)
attendance_button.pack(pady=10)

student_id_entry = tk.Entry(exam_tab, width=40)
student_id_entry.pack(pady=5)
student_id_entry.insert(0, "Student ID")

subject_entry = tk.Entry(exam_tab, width=40)
subject_entry.pack(pady=5)
subject_entry.insert(0, "Subject")

marks_entry = tk.Entry(exam_tab, width=40)
marks_entry.pack(pady=5)
marks_entry.insert(0, "Obtained Marks")

total_entry = tk.Entry(exam_tab, width=40)
total_entry.pack(pady=5)
total_entry.insert(0, "Total Marks")

month_entry = tk.Entry(exam_tab, width=40)
month_entry.pack(pady=5)
month_entry.insert(0, datetime.now().strftime("%Y-%m"))


def add_exam_result():

    try:

        student_id = student_id_entry.get()
        subject = subject_entry.get()
        marks = float(marks_entry.get())
        total_marks = float(total_entry.get())
        month = month_entry.get()

        cursor.execute(
            """
            INSERT INTO exams
            (student_id, subject, marks, total_marks, exam_month)
            VALUES (?, ?, ?, ?, ?)
            """,
            (student_id, subject, marks, total_marks, month)
        )

        connection.commit()

        percentage = (marks / total_marks) * 100

        messagebox.showinfo(
            "Saved",
            f"Percentage: {round(percentage,2)}%"
        )

    except:

        messagebox.showerror("Error", "Invalid Input")


exam_button = tk.Button(exam_tab, text="Save Exam Result", command=add_exam_result)
exam_button.pack(pady=20)

report_text = tk.Text(report_tab, width=100, height=30)
report_text.pack(pady=20)


def generate_top_students():

    report_text.delete("1.0", tk.END)

    month = datetime.now().strftime("%Y-%m")

    cursor.execute("""
    SELECT students.name,
           students.grade,
           SUM(exams.marks),
           SUM(exams.total_marks)

    FROM exams

    JOIN students
    ON exams.student_id = students.id

    WHERE exams.exam_month = ?

    GROUP BY students.name

    ORDER BY SUM(exams.marks) DESC
    """, (month,))

    records = cursor.fetchall()

    report_text.insert(tk.END, "===== TOP STUDENTS =====\n\n")

    rank = 1

    for record in records:

        name = record[0]
        grade = record[1]
        obtained = record[2]
        total = record[3]

        percentage = (obtained / total) * 100

        report_text.insert(
            tk.END,
            f"{rank}. {name} | Grade: {grade} | {round(percentage,2)}%\n"
        )

        rank += 1


report_button = tk.Button(report_tab, text="Generate Top Student Report", command=generate_top_students)
report_button.pack(pady=10)

load_students()
load_attendance_students()

root.mainloop()

connection.close()
