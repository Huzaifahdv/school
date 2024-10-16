from inputs import *

if __name__ == "__main__":
    create_tables()
    while True:
        print("\n" + "=" * 50)
        print("Please choose an operation:")
        print("=" * 50)
        print("* To add a student, enter 'a'")
        print("* To delete a student, enter 'd'")
        print("* To update a student's information, enter 'u'")
        print("* To show a student's information, enter 's'")
        print("* To add a lesson, enter 'al'")
        print("* To delete a lesson, enter 'dl'")
        print("* To update a lesson, enter 'ul'")
        print("* To show lessons information, enter 'sl'")
        print("* To Exit the program, enter 'q'")
        print("=" * 50)
        choice = input("Enter your choice: ").lower().strip()

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
            print("Exiting the program... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
