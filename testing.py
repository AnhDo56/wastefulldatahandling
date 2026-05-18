import json
import os
import time

DATA_FILE = "students.json"

==================MAARIT=========================
#toberemove
def create_data_file_if_missing(): # Why create a file every time the code is run?
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as file:
            json.dump([], file) #toberemove
            
def load_students():  
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_students(students): 
    with open(DATA_FILE, "w") as file:
        json.dump(students, file, indent=4)

OPTION2 - my suggestion:
def load_students():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError): #runsEvenIfBrokenOREmpty as above the first one does the same/MN
        return []

def save_students(students):
    with open(DATA_FILE, "w") as file:
        json.dump(students, file, indent=4)
======================MARIS===========================

 # Inefficiency: unbounded while True loop - no limit on login attempts
 # Fix: replace with for attempt in range(3) to cap at 3 tries > limits attempts and does not loop forever 
def login():
    username = "admin"
    password = "password"
    
    while True:
        given_username = input("Enter username: ")
        given_password = input("Enter password: ")

        if given_username == username and given_password == password:
            print("Login successful.")
            break
        else:
            print("Incorrect username or password. Please try again.")

#OPTION1 to fix the above code
    # range(3) runs the loop exactly 3 times, then exits automatically
    for attempt in range(3):
        given_username = input("Enter username: ")
        given_password = input("Enter password: ")
        if given_username == username and given_password == password:
            print("Login successful.")
            return
        else:
            print("Incorrect username or password. Please try again.")
    print("Too many failed attempts.")


def add_student():
    student_number = input("Enter student number: ")
    name = input("Enter student name: ")
    contact = input("Enter student contact information: ")
    students = load_students()
    
 # Inefficiency: loop always checks every student even after a duplicate is found
    # duplicate_found flag is also unnecessary extra code
    duplicate_found = False
    for student in students:
        if student["student_number"] == student_number:
            duplicate_found = True

    if duplicate_found:
        print("Student number already exists.")
        return

    new_student = {
        "student_number": student_number,
        "name": name,
        "contact": contact,
        "grades": []
    }

    students.append(new_student)
    save_students(students)

    print("Student added.")

# OPTION1
    # any() stops searching the moment it finds a match, instead of always checking everyone
    if any(s["student_number"] == student_number for s in students):
        print("Student number already exists.")
        return

    new_student = {
        "student_number": student_number,
        "name": name,
        "contact": contact,
        "grades": []
    }
    students.append(new_student)
    save_students(students)
    print("Student added.")


def add_grade():
    student_number = input("Enter student number: ")
    course = input("Enter course name: ")
    grade = input("Enter grade: ")

    students = load_students()
    
# Inefficiency 1: "for a student" is a syntax error, crashes the program
    # Inefficiency 2: loop continues after finding the student, even though there can only be one match
    student_found = False

    for a student in students:
        if student["student_number"] == student_number:
            student["grades"].append({
                "course": course,
                "grade": grade
            })
            student_found = True

    if student_found:
        save_students(students)
        print("Grade added.")
    else:
        print("Student not found.")

#OPTION1
    # Fixed syntax: "for student" instead of "for a student"
    # break stops the loop immediately after finding the student
    student_found = False
    for student in students:
        if student["student_number"] == student_number:
            student["grades"].append({
                "course": course,
                "grade": grade
            })
            student_found = True
            break  # no need to keep looping, student numbers are unique
    if student_found:
        save_students(students)
        print("Grade added.")
    else:
        print("Student not found.")
        
==========================ANH====================

def search_student():
    student_number = input("Enter student number to search for: ")

    start_time = time.perf_counter()

    students = load_students()

    found_student = None

    for student in students:
        if student["student_number"] == student_number:
            found_student = student

    end_time = time.perf_counter()

    if found_student:
        print("Student found:")
        print(f"Student Number: {found_student['student_number']}")
        print(f"Name: {found_student['name']}")
        print(f"Contact: {found_student['contact']}")
        print(f"Grades: {found_student['grades']}")
    else:
        print("Student not found.")

    print(f"Search took {end_time - start_time:.6f} seconds.")


def display_all_students():
    students = load_students()

    if not students:
        print("No students found.")
        return

    print("All students:")

    for i in range(len(students)):
        sorted_students = sorted(students, key=lambda student: student["name"])
        student = sorted_students[i]

        print(f"Student Number: {student['student_number']}")
        print(f"Name: {student['name']}")
        print(f"Contact: {student['contact']}")
        print(f"Grades: {student['grades']}")
        print()


def count_total_grades():
    students = load_students()

    total = 0

    copied_students = []

    for student in students:
        copied_students.append(student)

    for student in copied_students:
        for grade in student["grades"]:
            total += 1

    print(f"Total number of grades: {total}")

===========================KATA=============================

def display_course_summary():
    students = load_students()

    all_courses = []

    # Inefficient: builds a course list using repeated membership checks
    for student in students:
        for grade in student["grades"]:
            if grade["course"] not in all_courses:
                all_courses.append(grade["course"])

    print("Course summary:")

    # Inefficient: nested loops repeatedly scan all students and grades
    for course in all_courses:
        count = 0

        for student in students:
            for grade in student["grades"]:
                if grade["course"] == course:
                    count += 1

        print(f"{course}: {count} grade(s)")


def save_backup():    
    students = load_students()

    json_text = json.dumps(students) #this seems a bit unnecessary, data is already on python form. this changes the form to json text. WHY? :)
    copied_students = json.loads(json_text) #this seems a bit unnecessary, as JSON string → Python

    with open("students_backup.json", "w") as file:  #lets just leave this? 
        json.dump(copied_students, file, indent=4)

    print("Backup saved.")


def main():
    create_data_file_if_missing() #this to be removed to avoid unnecssary file-system checks every time when starting the program.
    login()

    while True:
        print("\nSelect an action:")
        print("1. Add a student")
        print("2. Add grade")
        print("3. Search for student")
        print("4. Display all students")
        print("5. Count total grades")
        print("6. Display course summary")
        print("7. Save backup")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            add_grade()
        elif choice == "3":
            search_student()
        elif choice == "4":
            display_all_students()
        elif choice == "5":
            count_total_grades()
        elif choice == "6":
            display_course_summary()
        elif choice == "7":
            save_backup()
        elif choice == "8":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")

# A dispatch dictionary instead of a long if/elif chain. Cleaner and easier to maintain. Reduces repetitiveness.    
    
    actions = {
        "1": add_student,
        "2": add_grade,
        "3": search_student,
        "4": display_all_students,
        "5": count_total_grades.
        "6": display_course_summary,
        "7": save_backup,
    }

    if choice == "8":
        print("Goodbye.")
        break

    # Execute selected action if valid
    action = actions.get(choice)

    if action:
        action()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
