from inputs import *


if __name__ == "__main__":

    create_tables()
    while True:
        print("Please choose an operation:")
        print("* To add a student, press 'a'")
        print("* To delete a student, press 'd'")
        print("* To update a student's information, press 'u'")
        print("* To show a student's information, press 's'")
        print("* To add a lesson, press 'al'")
        print("* To delete a lesson, press 'dl'")
        print("* To update a lesson, press 'ul'")
        print("* To show a lessons, press 'sl'")
        print("* To Exit the program, press 'q'")
        choice = input("Enter your choice: ").lower()
        if choice == 'a':
            add_student()
        elif choice == 'd':
            delete_student()
        elif choice == 'u':
            update_student()
        elif choice == 's':
            show_student()
        elif choice == 'al':
            add_lesson()
        elif choice == 'dl':
            delete_lesson()
        elif choice == 'ul':
            update_lesson()
        elif choice == 'sl':
            show_lesson()
        elif choice == 'q':
            break
        else:
            print("Invalid choice. Please try again.")
