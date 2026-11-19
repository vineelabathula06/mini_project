
import sqlite3

DB_NAME = "students.db"

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            roll_no TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            course TEXT,
            marks REAL,
            grade TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("Database connected successfully!")
def calculate_grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 75:
        return "A"
    elif marks >= 60:
        return "B"
    elif marks >= 40:
        return "C"
    else:
        return "Fail"
def get_marks():
    while True:
        try:
            marks = float(input("Enter Marks (0-100): "))
            if 0 <= marks <= 100:
                return marks
            print("Marks must be between 0 and 100.")
        except ValueError:
            print("Please enter valid marks!")
def add_student():
    roll_no = input("Enter Roll Number: ")
    name = input("Enter Student Name: ")
    age = input("Enter Age: ")
    course = input("Enter Course: ")
    marks = get_marks()

    grade = calculate_grade(marks)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO students
            VALUES (?, ?, ?, ?, ?, ?)
        """, (roll_no, name, age, course, marks, grade))

        conn.commit()
        print("Student added successfully!")
    except sqlite3.IntegrityError:
        print("Roll Number already exists!")

    finally:
        conn.close()
def view_students():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    print("\n========== Student Details ==========")

    if records:
        for row in records:
            print("Roll No:", row[0])
            print("Name:", row[1])
            print("Age:", row[2])
            print("Course:", row[3])
            print("Marks:", row[4])
            print("Grade:", row[5])
            print("--------------------------------")
    else:
        print("No student records found.")

    conn.close()
def search_student():
    roll_no = input("Enter Roll Number to search: ")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    row = cursor.fetchone()

    if row:
        print("\nStudent Found!")
        print("Roll No:", row[0])
        print("Name:", row[1])
        print("Age:", row[2])
        print("Course:", row[3])
        print("Marks:", row[4])
        print("Grade:", row[5])
    else:
        print("Student not found.")

    conn.close()
def update_student():
    roll_no = input("Enter Roll Number to update: ")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    row = cursor.fetchone()

    if row:
        print("Current Details:", row)

        name = input("Enter New Name: ")
        age = input("Enter New Age: ")
        course = input("Enter New Course: ")
        marks = get_marks()

        grade = calculate_grade(marks)

        cursor.execute("""
            UPDATE students
            SET name = ?, age = ?, course = ?,
                marks = ?, grade = ?
            WHERE roll_no = ?
        """, (name, age, course, marks, grade, roll_no))

        conn.commit()
        print("Student updated successfully!")

    else:
        print("Student not found.")

    conn.close()
def delete_student():
    roll_no = input("Enter Roll Number to delete: ")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    conn.commit()

    if cursor.rowcount > 0:
        print("Student deleted successfully!")
    else:
        print("Student not found.")

    conn.close()
def main():
    create_database()

    while True:
        print("""
========== STUDENT MANAGEMENT SYSTEM ==========

1. Add Student
2. View Students
3. Search Student
4. Update Student
5. Delete Student
6. Exit

===============================================
""")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            update_student()

        elif choice == "5":
            delete_student()

        elif choice == "6":
            print("Exiting program...")
            break

        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()
