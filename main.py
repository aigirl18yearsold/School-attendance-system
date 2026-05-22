import sqlite3

connection = sqlite3.connect("students.db")
cursor = connection.cursor()


# =========================
# ADD STUDENT
# =========================

def add_student():

    name = input("Enter Student Name: ")

    cursor.execute(
        "INSERT INTO students (name) VALUES (?)",
        (name,)
    )

    connection.commit()

    print("Student Added Successfully")


# =========================
# VIEW STUDENTS
# =========================

def view_students():

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    print("\n===== STUDENT LIST =====")

    for student in students:

        print(student)


# =========================
# MARK ATTENDANCE
# =========================

def mark_attendance():

    date = input("Enter Date (YYYY-MM-DD): ")

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()


    for student in students:

        student_id = student[0]
        student_name = student[1]

        print(f"\nStudent: {student_name}")

        status = input("Present or Absent (P/A): ")


        cursor.execute("""
        INSERT INTO attendance (student_id, date, status)
        VALUES (?, ?, ?)
        """, (student_id, date, status))


    connection.commit()

    print("\nAttendance Saved Successfully")


# =========================
# MONTHLY REPORT
# =========================

def monthly_report():

    student_id = input("Enter Student ID: ")

    month = input("Enter Month (Example 2026-05): ")


    cursor.execute("""
    SELECT status FROM attendance
    WHERE student_id = ?
    AND date LIKE ?
    """, (student_id, f"{month}%"))

    records = cursor.fetchall()

    present = 0
    absent = 0


    for record in records:

        if record[0] == "P":
            present += 1

        elif record[0] == "A":
            absent += 1


    total = present + absent


    if total > 0:

        percentage = (present / total) * 100

        print("\n===== MONTHLY REPORT =====")
        print("Present:", present)
        print("Absent:", absent)
        print("Percentage:", round(percentage, 2), "%")

    else:

        print("No Records Found")


# =========================
# YEARLY REPORT
# =========================

def yearly_report():

    student_id = input("Enter Student ID: ")

    year = input("Enter Year (2026): ")


    cursor.execute("""
    SELECT status FROM attendance
    WHERE student_id = ?
    AND date LIKE ?
    """, (student_id, f"{year}%"))

    records = cursor.fetchall()

    present = 0
    absent = 0


    for record in records:

        if record[0] == "P":
            present += 1

        elif record[0] == "A":
            absent += 1


    total = present + absent


    if total > 0:

        percentage = (present / total) * 100

        print("\n===== YEARLY REPORT =====")
        print("Present:", present)
        print("Absent:", absent)
        print("Percentage:", round(percentage, 2), "%")

    else:

        print("No Records Found")


# =========================
# MAIN MENU
# =========================

while True:

    print("\n========================")
    print("ATTENDANCE MANAGEMENT")
    print("========================")

    print("1. Add Student")
    print("2. View Students")
    print("3. Mark Attendance")
    print("4. Monthly Report")
    print("5. Yearly Report")
    print("6. Exit")

    choice = input("\nEnter Choice: ")


    if choice == "1":

        add_student()


    elif choice == "2":

        view_students()


    elif choice == "3":

        mark_attendance()


    elif choice == "4":

        monthly_report()


    elif choice == "5":

        yearly_report()


    elif choice == "6":

        print("Program Closed")

        break


    else:

        print("Invalid Choice")


connection.close()
