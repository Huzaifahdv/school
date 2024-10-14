import sqlite3


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
                    lesson_name TEXT,
                    student_id INTEGER,
                    FOREIGN KEY (student_id) REFERENCES students(student_id))''')
    con.commit()
    con.close()


def add_student():
    while True:
        try:
            student_id = int(input("Enter student ID: "))
            con = sqlite3.connect('school.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
            if cur.fetchone():
                print('This ID already exists. Try adding a new ID')
                con.close()
            else:
                con.close()
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

    con = sqlite3.connect('school.db')
    cur = con.cursor()
    while True:
        cur.execute("SELECT lesson_id, lesson_name FROM lessons WHERE student_id IS NULL")
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
                    selected_lessons = input("Enter lesson IDs (comma separated): ").split(',')
                    if all(lesson_id.strip() in available_lessons for lesson_id in selected_lessons):
                        return selected_lessons
                    else:
                        print("Invalid input. Please choose from the registered lessons only.")
            valid_lessons = get_valid_lessons()
            break
        else:
            print('No registered lessons found. Please add a new lesson first.')
            add_lesson()

    cur.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)",
                (student_id, first_name.capitalize(), last_name.capitalize(), age, grade, registration_date))
    for lesson_id in valid_lessons:
        lesson_name = available_lessons[lesson_id.strip()]
        cur.execute("INSERT INTO lessons (student_id, lesson_name) VALUES (?, ?)", (student_id, lesson_name.strip().upper()))
    con.commit()
    con.close()
    print("Student added successfully")


def delete_student():
    while True:
        student_id = input("Enter student ID to delete: ")
        if student_id == 'q':
            return
        try:
            student_id = int(student_id)
            break
        except ValueError:
            print('Please enter Student ID as a valid number only')
    con = sqlite3.connect('school.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    if cur.fetchone():
        while True:
            ch = input('Are you sure you want to delete student information? (y/n)')
            if ch == 'y':
                cur.execute("DELETE FROM lessons WHERE student_id = ?", (student_id,))
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


def update_student():
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
        print("Student updated successfully")
    else:
        print("Student ID not found")
    con.close()


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
        cur.execute("SELECT lesson_name FROM lessons WHERE student_id = ?", (student_id,))
        lessons = cur.fetchall()
        print("Lessons:", ", ".join([lesson[0] for lesson in lessons]))
    else:
        print("Student not found")
    con.close()


def add_lesson():
    lessons = input("Enter new lesson(s) (comma separated if multiple): ").split(',')
    con = sqlite3.connect('school.db')
    cur = con.cursor()
    for lesson in lessons:
        cur.execute("INSERT INTO lessons (lesson_name) VALUES (?)", (lesson.upper(),))
    con.commit()
    con.close()
    print('The lesson(s) have been added successfully.')


def delete_lesson():
    con = sqlite3.connect('school.db')
    cur = con.cursor()
    while True:
        cur.execute("SELECT lesson_id, lesson_name FROM lessons WHERE student_id IS NULL")
        lessons = cur.fetchall()
        available_lessons = {str(lesson[0]): lesson[1] for lesson in lessons}

        print('-' * 10)
        print('Registered Lessons: ')
        for lesson_id, lesson_name in available_lessons.items():
            print(f'lesson ID: {lesson_id}, lesson name: {lesson_name}')
        print('-' * 10)

        lesson_id = input('Enter the lesson ID you want to delete: ')
        if lesson_id == 'q':
            return

        try:
            lesson_id = int(lesson_id)
        except ValueError:
            print("Please enter a valid lesson ID number, or press 'q' to Exit")
            continue

        if str(lesson_id) in available_lessons:
            while True:
                ch = input('Are you sure you want to delete lesson ? (y/n)')
                if ch.lower() == 'y':
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
            return


def update_lesson():
    con = sqlite3.connect('school.db')
    cur = con.cursor()
    cur.execute("SELECT lesson_id, lesson_name FROM lessons WHERE student_id IS NULL")
    lessons = cur.fetchall()
    print('-' * 10)
    print('Registered Lessons: ')
    for lesson in lessons:
        print(f'lesson ID: {lesson[0]}, lesson name: {lesson[1]}')
    print('-' * 10)
    while True:
        lesson_id = input("Enter lesson ID to update: ")
        if lesson_id == 'q':
            return
        try:
            lesson_id = int(lesson_id)
            break
        except ValueError:
            print("Enter a valid lesson ID.. or press 'q' to exit")
    cur.execute("SELECT * FROM lessons WHERE lesson_id = ?", (lesson_id,))
    if cur.fetchone():
        lesson_name = input("Enter the name of the new lesson: ")
        cur.execute("UPDATE lessons SET lesson_name = ? WHERE lesson_id = ?", (lesson_name.upper(), lesson_id))
        con.commit()
        con.close()
        print('lesson updated successfully')
    else:
        con.close()
        print('the lesson is not found')


def show_lesson():
    con = sqlite3.connect('school.db')
    cur = con.cursor()
    cur.execute("SELECT lesson_id, lesson_name FROM lessons WHERE student_id IS NULL")
    lessons = cur.fetchall()
    con.close()
    print('-' * 10)
    for index, lesson in enumerate(lessons):
        print(f'{index + 1} - {lesson[1]}')
    print('-' * 10)
