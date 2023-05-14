#import csv
import pandas as pd

from Student_and_Course_class import StudentInfo, Course

student_df = pd.read_csv('student_info.csv')
course_df = pd.read_csv('courses.csv')


def main():

    course = Course()
    student = StudentInfo()

    course.addCourse('BS in Info System', 'BSIS')
    course.addCourse('BS in Info Tech', 'BSIT')
    course.addCourse('BS in Computer Application', 'BSCA')
    course.addCourse('BS in Computer Application', 'BSCA')
    course.deleteCourse('BSCA')

    student.addStudent("John", "126", "BSIT")  # works
    student.addStudent("John", "126", "BSIT")
    student.updateStudent("R", "Rhea", 'BSCS')  # id issue same SOLVED
    student.addStudent("R", "2021-2362", "BSCS")
    student.searchStudent('I')
    student.searchStudent("12445")  # not found  SOLVED
    student.updateStudent("R", "Rhea", 'BSCS')
    course.addCourse('BS in Computer Science', 'BSCS')
    student.addStudent("R", "2021-2362", "BSCS")
    course.displayList()

    course.updateCourse('BSIT', 'BS in Information Technology')
    course.searchCourse('BSIT')
    course.searchCourse('BS in Information Technology')
    course.searchCourse('BS in Info Tech')
    course.searchCourse('BSME')
    course.displayList()


'''
course = Course()
student = StudentInfo()
print("  Simple Student Information System  \n")
print("--------------------------------------")
print("Choose a selection: ")
print("1. Student Information")
print("2. Course Information")

choice = input("Enter your choice: ")
if choice == '1':
    print("You selected Student Information.\nChoose a selection: ")
    print("1. Add a new student")
    print("2. Remove a student")
    print("3. Display list of students")
    print("4. Search for students")
    print("5. Update student information")

    choice1 = input("Enter your choice: ")
    if choice1 == '1':
        #add samting
        student.addStudent()
    elif choice1 == '2':
        student.deleteStudent()
    elif choice1 == '3':
        student.displayList()
    elif choice1 == '4':
        student.searchStudent()
    elif choice1 == '5':
        student.updateStudent()
    else:
        print("Invalid choice.")

elif choice == '2':
    print("You selected Course Information.\nChoose a selection: ")
    print("1. Add a new course")
    print("2. Remove a courset")
    print("3. Display list of courses")
    print("4. Search for courses")
    print("5. Update course information")

    choice2 = input("Enter your choice: ")
    if choice2 == '1':
        course.addCourse()
    elif choice2 == '2':
        course.deleteCourse()
    elif choice2 == '3':
        course.displayList()
    elif choice2 == '4':
        course.searchCourse()
    elif choice2 == '5':
        course.updateCourse()
    else:
        print("Invalid choice.")
'''
main()
