import sqlite3
from datetime import datetime
import time


def create_tables():
    con = sqlite3.connect('school.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS students (
                    student_id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    age INTEGER,
                    grade TEXT,
                    registration_date TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS lessons (
                    lesson_id INTEGER PRIMARY KEY,
                    lesson_name TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS enrollments (
                    enrollment_id INTEGER PRIMARY KEY,
                    student_id INTEGER,
                    lesson_id INTEGER,
                    enrollment_date DATE,
                    FOREIGN KEY (student_id) REFERENCES students(student_id),
                    FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id))''')
    con.commit()
    con.close()


def add_student():
    while True:
        try:
            student_id = int(input("Enter student ID: "))
            with sqlite3.connect('school.db') as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
                if cur.fetchone():
                    print('This ID already exists. Try adding a new ID')
                else:
                    break
        except ValueError:
            print('Please enter Student ID as a valid number only')

    while True:
        first_name = input("Enter first name: ")
        if first_name.isalpha():
            break
        else:
            print('Please enter the name in letters only')

    while True:
        last_name = input("Enter last name: ")
        if last_name.isalpha():
            break
        else:
            print('Please enter the last name in letters only')

    while True:
        try:
            age = int(input("Enter age: "))
            if 3 < age < 90:
                break
            else:
                print('Please enter a valid age')
        except ValueError:
            print('Please enter age in numbers only')

    grade = input("Enter grade: ")
    registration_date = input("Enter registration date (YYYY-MM-DD): ")

    with sqlite3.connect('school.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)",
                    (student_id, first_name.capitalize(), last_name.capitalize(), age, grade, registration_date))

    while True:
        print("Do you want to add lessons for the student?")
        ch = input('(y/n): ')
        if ch == 'y':
            while True:
                with sqlite3.connect('school.db') as con:
                    cur = con.cursor()
                    cur.execute("SELECT lesson_id, lesson_name FROM lessons")
                    lessons = cur.fetchall()
                    if lessons:
                        available_lessons = {str(lesson[0]): lesson[1] for lesson in lessons}
                        print('-' * 10)
                        print('Registered Lessons: ')
                        for lesson_id, lesson_name in available_lessons.items():
                            print(f'Lesson ID: {lesson_id}, Lesson Name: {lesson_name}')
                        print('-' * 10)

                        def get_valid_lessons():
                            while True:
                                selected_lessons = input("Enter the IDs of the lessons you want to add for the student (comma separated): ").split(',')
                                if all(lesson_id.strip() in available_lessons for lesson_id in selected_lessons):
                                    return selected_lessons
                                else:
                                    print("Invalid input. Please enter lesson IDs from the registered lessons only.")

                        valid_lessons = get_valid_lessons()
                        break
                    else:
                        print("No registered lessons found.")
                        while True:
                            ch = input("To add a new lesson now enter 'a', or to skip and save enter 's': ")
                            if ch == 'a':
                                add_lesson()
                                break
                            elif ch == 's':
                                print("Student added successfully")
                                return

            enrollment_date = datetime.now().strftime("%Y-%m-%d")

            with sqlite3.connect('school.db') as con:
                cur = con.cursor()
                for lesson_id in valid_lessons:
                    cur.execute("INSERT INTO enrollments (student_id, lesson_id, enrollment_date) VALUES (?, ?, ?)",
                                (student_id, lesson_id.strip(), enrollment_date))
                con.commit()
                print("Student added successfully")
                return

        elif ch == 'n':
            print("Student added successfully")
            return


def delete_student():
    while True:
        student_id = input("Enter student ID to delete: ")
        if student_id == 'q':
            return
        try:
            student_id = int(student_id)
            break
        except ValueError:
            print("Please enter Student ID as a valid number only, or enter 'q' to cancel")

    con = sqlite3.connect('school.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    if cur.fetchone():
        while True:
            ch = input('Are you sure you want to delete student information? (y/n): ')
            if ch == 'y':
                cur.execute("DELETE FROM enrollments WHERE student_id = ?", (student_id,))
                cur.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
                con.commit()
                con.close()
                print("The student has been successfully deleted")
                break
            elif ch == 'n':
                con.close()
                print('The operation has been cancelled')
                break
    else:
        print("Student ID not found")
        con.close()


def update_student():
    while True:
        print("To update the student's personal information enter 'p'")
        print("To update a student's registered lessons information, enter 'l'")
        ch = input('Enter: ')
        if ch == 'p':
            while True:
                try:
                    student_id = int(input("Enter student ID to update: "))
                    break
                except ValueError:
                    print('Please enter Student ID as a valid number only')
            con = sqlite3.connect('school.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
            if cur.fetchone():
                while True:
                    first_name = input("Enter new first name: ")
                    if first_name.isalpha():
                        break
                    else:
                        print('Please enter the name in letters only')
                while True:
                    last_name = input("Enter new last name: ")
                    if last_name.isalpha():
                        break
                    else:
                        print('Please enter the last name in letters only')
                while True:
                    try:
                        age = int(input("Enter new age: "))
                        if 3 < age < 100:
                            break
                        else:
                            print('Please enter a valid age')
                    except ValueError:
                        print('Please enter a number only..')
                grade = input("Enter new grade: ")
                registration_date = input("Enter new registration date (YYYY-MM-DD): ")
                cur.execute("UPDATE students SET first_name = ?, last_name = ?, age = ?, grade = ?, registration_date = ? WHERE student_id = ?",
                            (first_name.capitalize(), last_name.capitalize(), age, grade, registration_date, student_id))
                con.commit()
                con.close()
                print("Student information has been updated successfully")
                return
            else:
                print("Student ID not found")
                con.close()
                return
        elif ch == 'l':
            while True:
                try:
                    student_id = int(input("Enter student ID to update: "))
                    break
                except ValueError:
                    print('Please enter Student ID as a valid number only')
            con = sqlite3.connect('school.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
            if cur.fetchone():
                while True:
                    cur.execute("SELECT lesson_id, lesson_name FROM lessons")
                    lessons = cur.fetchall()
                    if lessons:
                        available_lessons = {str(lesson[0]): lesson[1] for lesson in lessons}
                        print('-' * 10)
                        print('Registered Lessons: ')
                        for lesson_id, lesson_name in available_lessons.items():
                            print(f'lesson ID: {lesson_id}, lesson name: {lesson_name}')
                        print('-' * 10)

                        def get_valid_lessons():
                            while True:
                                selected_lessons = input("Enter the IDs of the lessons you want to add for the student (comma separated): ").split(',')
                                if all(lesson_id.strip() in available_lessons for lesson_id in selected_lessons):
                                    return selected_lessons
                                else:
                                    print("Invalid input. Please enter lesson IDs from the registered lessons only.")
                        valid_lessons = get_valid_lessons()
                        break
                    else:
                        print("No registered lessons found.")
                        while True:
                            ch = input(" To add a new lesson now enter 'a', or To cancel enter 'q': ")
                            if ch == 'a':
                                add_lesson()
                                break
                            elif ch == 'q':
                                con.close()
                                print("The operation has been cancelled")
                                return
                cur.execute("DELETE FROM enrollments WHERE student_id = ?", (student_id,))
                enrollment_date = datetime.now().strftime("%Y-%m-%d")
                for lesson_id in valid_lessons:
                    cur.execute("INSERT INTO enrollments (student_id, lesson_id, enrollment_date) VALUES (?, ?, ?)",
                                (student_id, lesson_id.strip(), enrollment_date))
                print("The student's lessons information has been successfully updated")
                con.commit()
                con.close()
                return
            else:
                print("Student ID not found")
                con.close()
                return
        elif ch == 'q':
            return


def show_student():
    while True:
        try:
            student_id = int(input("Enter student ID to show: "))
            break
        except ValueError:
            print('Please enter a valid ID number..')
    con = sqlite3.connect('school.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    student = cur.fetchone()
    if student:
        print(f"ID: {student[0]}, Name: {student[1]} {student[2]}, Age: {student[3]}, Grade: {student[4]}, Registration Date: {student[5]}")
        cur.execute("""SELECT lessons.lesson_name 
                            FROM lessons 
                            JOIN enrollments ON lessons.lesson_id = enrollments.lesson_id 
                            WHERE enrollments.student_id = ? """, (student_id,))
        lessons = cur.fetchall()
        if lessons:
            print("Lessons:", ", ".join([lesson[0] for lesson in lessons]))
        else:
            print("No lessons found for this student.")
    else:
        print("Student not found")
    con.close()


def add_lesson():
    lessons = input("Enter new lesson(s) (comma separated if multiple): ").split(',')
    try:
        with sqlite3.connect('school.db') as con:
            cur = con.cursor()
            for lesson in lessons:
                cur.execute("INSERT INTO lessons (lesson_name) VALUES (?)", (lesson.strip().upper(),))
            con.commit()
            print('The lesson(s) have been added successfully.')
    except sqlite3.OperationalError as e:
        if 'database is locked' in str(e):
            print('Database is locked. Retrying in a moment...')
            time.sleep(1)
            add_lesson()
        else:
            raise e


def delete_lesson():
    con = sqlite3.connect('school.db')
    cur = con.cursor()

    while True:
        cur.execute("SELECT lesson_id, lesson_name FROM lessons")
        lessons = cur.fetchall()
        available_lessons = {str(lesson[0]): lesson[1] for lesson in lessons}

        if available_lessons:
            print('-' * 10)
            print('Registered Lessons:')
            for lesson_id, lesson_name in available_lessons.items():
                print(f'Lesson ID: {lesson_id}, Lesson Name: {lesson_name}')
            print('-' * 10)

            lesson_id = input('Enter the lesson ID you want to delete: ')
            if lesson_id == 'q':
                con.close()
                return

            try:
                lesson_id = int(lesson_id)
            except ValueError:
                print("Please enter a valid lesson ID number, or enter 'q' to cancel")
                continue

            if str(lesson_id) in available_lessons:
                while True:
                    ch = input('Are you sure you want to delete this lesson? (y/n): ')
                    if ch.lower() == 'y':
                        cur.execute("DELETE FROM enrollments WHERE lesson_id = ?", (lesson_id,))
                        cur.execute("DELETE FROM lessons WHERE lesson_id = ?", (lesson_id,))
                        con.commit()
                        con.close()
                        print("The lesson has been successfully deleted")
                        return
                    elif ch.lower() == 'n':
                        con.close()
                        print('The operation has been cancelled')
                        return
            else:
                print("The entered lesson ID does not exist in the registered lessons list.")
                print("you can cancel operation by entering 'q'")
                continue
        else:
            print("No registered lessons found.")
            con.close()
            return


def update_lesson():
    con = sqlite3.connect('school.db')
    cur = con.cursor()
    cur.execute("SELECT lesson_id, lesson_name FROM lessons")
    lessons = cur.fetchall()

    if lessons:
        print('-' * 10)
        print('Registered Lessons:')
        for lesson in lessons:
            print(f'Lesson ID: {lesson[0]}, Lesson Name: {lesson[1]}')
        print('-' * 10)

        while True:
            lesson_id = input("Enter lesson ID to update: ")
            if lesson_id == 'q':
                con.close()
                return
            try:
                lesson_id = int(lesson_id)
                break
            except ValueError:
                print("Enter a valid lesson ID.. or press 'q' to cancel")

        cur.execute("SELECT * FROM lessons WHERE lesson_id = ?", (lesson_id,))
        if cur.fetchone():
            lesson_name = input("Enter the name of the new lesson: ")
            cur.execute("UPDATE lessons SET lesson_name = ? WHERE lesson_id = ?",
                        (lesson_name.strip().upper(), lesson_id))
            con.commit()
            con.close()
            print('Lesson updated successfully')
        else:
            con.close()
            print('The lesson is not found')
    else:
        con.close()
        print('No registered lessons found.')


def show_lesson():
    while True:
        print("To view the list of lessons, enter 'l'")
        print("To view students enrolled in a specific lesson, enter 's'")
        ch = input('Enter: ')
        if ch == 'l':
            con = sqlite3.connect('school.db')
            cur = con.cursor()
            cur.execute("SELECT lesson_id, lesson_name FROM lessons")
            lessons = cur.fetchall()
            con.close()
            if lessons:
                print('-' * 10)
                for index, lesson in enumerate(lessons):
                    print(f'{index + 1} - {lesson[1]}')
                print('-' * 10)
                return
            else:
                print('No registered lessons found.')
                return
        elif ch == 's':
            con = sqlite3.connect('school.db')
            cur = con.cursor()
            cur.execute("SELECT lesson_id, lesson_name FROM lessons")
            lessons = cur.fetchall()
            if lessons:
                available_lessons = {str(lesson[0]): lesson[1] for lesson in lessons}
                print('-' * 10)
                print('Registered Lessons: ')
                for lesson_id, lesson_name in available_lessons.items():
                    print(f'Lesson ID: {lesson_id}, Lesson Name: {lesson_name}')
                print('-' * 10)
                while True:
                    lesson_id = input("Enter lesson ID: ")
                    if lesson_id.strip() in available_lessons:
                        cur.execute("""
                        SELECT lessons.lesson_name, students.student_id, students.first_name, students.last_name, students.age, students.grade, enrollments.enrollment_date
                        FROM lessons
                        JOIN enrollments ON lessons.lesson_id = enrollments.lesson_id
                        JOIN students ON enrollments.student_id = students.student_id
                        WHERE lessons.lesson_id = ?
                        """, (lesson_id,))
                        students = cur.fetchall()
                        if students:
                            print('-' * 10)
                            print(f'Lesson Name: {students[0][0]}')
                            print('Enrolled Students:')
                            for student in students:
                                print(f'ID: {student[1]}, Name: {student[2]} {student[3]}, Age: {student[4]}, Grade: {student[5]}, Enrollment Date: {student[6]}')
                            print('-' * 10)
                        else:
                            print('No students enrolled in this lesson.')
                        break
                    else:
                        print("Invalid input. Please choose from the registered lessons only.")
            else:
                print('No registered lessons found.')
            con.close()
            return
