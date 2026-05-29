# Student Management System

import json

FILE_NAME = "students.json"


class Student:
    def __init__(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade

    def to_dict(self):
        return {
            "id": self.student_id,
            "name": self.name,
            "grade": self.grade
        }


class SchoolSystem:
    def __init__(self):
        self.students = self.load_students()

    def load_students(self):
        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)
                return data
        except:
            return []

    def save_students(self):
        with open(FILE_NAME, "w") as file:
            json.dump(self.students, file, indent=4)

    def add_student(self):
        student_id = input("Student ID: ")
        name = input("Student Name: ")
        grade = float(input("Student Grade: "))

        student = Student(student_id, name, grade)

        self.students.append(student.to_dict())

        self.save_students()

        print("Student Added Successfully!")

    def view_students(self):
        print("\n===== STUDENTS =====")

        for student in self.students:
            print(f"ID: {student['id']}")
            print(f"Name: {student['name']}")
            print(f"Grade: {student['grade']}")
            print("--------------------")

    def search_student(self):
        student_id = input("Enter Student ID: ")

        found = False

        for student in self.students:
            if student["id"] == student_id:
                print(student)
                found = True

        if not found:
            print("Student not found.")

    def delete_student(self):
        student_id = input("Enter Student ID to delete: ")

        for student in self.students:
            if student["id"] == student_id:
                self.students.remove(student)
                self.save_students()
                print("Student Deleted!")
                return

        print("Student not found.")


system = SchoolSystem()

while True:
    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Delete Student")
    print("5. Exit")

    choice = input("Choose: ")

    if choice == "1":
        system.add_student()

    elif choice == "2":
        system.view_students()

    elif choice == "3":
        system.search_student()

    elif choice == "4":
        system.delete_student()

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")