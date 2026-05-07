import time
import json
from main import add_student, search_student, load_students, save_students

TEST_FILE = "students.json"


def reset_data():
    with open(TEST_FILE, "w") as f:
        json.dump([], f)


def populate_test_data(n):
    students = []
    for i in range(n):
        students.append({
            "student_number": str(i),
            "name": f"Student {i}",
            "contact": "email@example.com",
            "grades": []
        })
    save_students(students)


def test_add_and_search():
    print("Running basic functionality test...")

    reset_data()

    add_student_manual("123", "Alice", "a@example.com")

    result = search_student_manual("123")

    if result and result["name"] == "Alice":
        print("PASS: Student added and found")
    else:
        print("FAIL: Student not found correctly")


def test_search_performance():
    print("\nRunning performance test...")

    reset_data()
    populate_test_data(1000)

    start = time.perf_counter()
    search_student_manual("999")
    end = time.perf_counter()

    print(f"Search time: {end - start:.6f} seconds")


# Helper versions without input() for testing
def add_student_manual(student_number, name, contact):
    students = load_students()

    students.append({
        "student_number": student_number,
        "name": name,
        "contact": contact,
        "grades": []
    })

    save_students(students)


def search_student_manual(student_number):
    students = load_students()

    for student in students:
        if student["student_number"] == student_number:
            return student

    return None


if __name__ == "__main__":
    test_add_and_search()
    test_search_performance()
       
