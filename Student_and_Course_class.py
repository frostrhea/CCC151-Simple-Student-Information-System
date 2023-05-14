import csv
import pandas as pd

# global array for class Student to refer for existing courses
course_list = pd.read_csv("courses.csv")['courseCode'].tolist()


class Course:
    def __init__(self):
        self.columns = ['courseCode', 'courseName']
        self.courses_df = pd.read_csv(
            "courses.csv", header=0, names=self.columns)
        self.course_list = course_list

    # function to add a course to the list
    # Checks if input is in the list, then adds it to the list by appending it to csv

    def returnCourseCSV(self):
        return self.courses_df

    def addCourse(self, value, code):
        if code in self.course_list or value in self.course_list:
            print(f"Course {value} already exists.")
            return
        else:
            new_course = {'courseName': value, 'courseCode': code}
            self.courses_df = self.courses_df.append(
                new_course, ignore_index=True)
            self.courses_df.to_csv('courses.csv', index=False, header=True)
            self.course_list.append(value)
            print(f"Course '{value}' added.\n")
    #
    # function to delete a course from the list
    # Looks for the possible index of the input, then drop it from the list if it exists
    #   then update the csv.

    def deleteCourse(self, code):
        index = self.courses_df.index[self.courses_df['courseCode'] == code].tolist(
        )
        if not index:
            print(f"Course code '{code}' does not exist.\n")
        else:
            self.courses_df.drop(index, inplace=True)
            self.courses_df.to_csv('courses.csv', index=False)
            print(f"Course '{code}' has been deleted.\n")

    # function to display a course
    # Prints the course through its index

    def displayCourse(self, index):
        course = self.courses_df.iloc[index]
        print(f"Course: {course['courseName']}")
        print(f"Course Code: {course['courseCode']}\n")
        # print(f"Students: {course['students']}\n")

    # function to display the course list
    # Prints all of the course in csv.

    def displayList(self):
        print("Displaying list of courses...")
        for i in range(len(self.courses_df)):
            self.displayCourse(i)
        print("All courses displayed successfully.\n")

    # function to search for courses (by courseName and CouseCode)
    # Checks the indexes then invoke displayCourse method if found

    def searchCourse(self, course):
        value = str(course)
        found = False
        for index in range(len(self.courses_df)):
            if self.courses_df.loc[index, 'courseName'] == value or self.courses_df.loc[index, 'courseCode'] == value:
                found = True
                print("Search Results: ")
                self.displayCourse(index)
        if not found:
            print(f"Course '{course}' not found.\n")

    # function to update the course name field
    # Checks the indexes, then if found, check the new name if it exists already in csv
    #    if not, updates the name field and saves the new name in csv.

    def updateCourse(self, value, newCourseName):
        found = False
        for index in range(len(self.courses_df)):
            if self.courses_df.loc[index, 'courseName'] == value or self.courses_df.loc[index, 'courseCode'] == value:
                found = True
                if str(newCourseName) in str(self.courses_df['courseName'].values):
                    print("Course name already exists.")

                else:
                    self.courses_df.at[index, 'courseName'] = newCourseName
                    # self.courses_df.at[index, 'courseCode'] = newCourseCode
                    self.courses_df.to_csv('courses.csv', index=False)
                    print(
                        f"Course '{value}' name updated successfully. \n")
        if not found:
            print(f"Course '{value}' not found.")


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

class StudentInfo:
    def __init__(self):
        self.columns = ['name', 'id', 'course']
        self.student_df = pd.read_csv(
            "student_info.csv", header=0, names=self.columns)
        self.course_list = course_list

    def returnStudentCSV(self):
        return self.student_df

    # function to add a student
    def addStudent(self, name, id, course):
        if course not in self.course_list:
            print("Invalid course.")
            return
        else:
            if str(id) in str(self.student_df['id'].values):
                print(f"Student with ID '{id}' already exists.")
                return
            # name = input("Enter student name: ")
            # id= input("Enter ID number: ")
            # course = input("Enter course: ")
            # student = pd.DataFrame({'name': [name], 'course': [course], 'id': [id]})
            else:
                new_student = {'name': name, 'course': course, 'id': id}
                self.student_df = self.student_df.append(
                    new_student, ignore_index=True)
                self.student_df.to_csv('student_info.csv', index=False,
                                       header=True)
                print(f"Student '{name}' has been added.\n")

    # function to delete student

    def deleteStudent(self, id):
        index = self.student_df.index[self.student_df['id'] == id].tolist()
        if not index:
            print(f"Student with ID '{id}' does not exist.\n")
        else:
            self.student_df.drop(index, inplace=True)
            # write updated df to csv file
            self.student_df.to_csv('student_info.csv', index=False)
            print(f"Student with ID '{id}' has been deleted.\n")

    # function to display/read information of student

    def displayStudent(self, index):
        student = self.student_df.iloc[index]
        print(f"Name: {student['name']}")
        print(f"Course: {student['course']}")
        if '-' in str(student['id']):
            print(f"ID: '{student['id']}'\n")
        else:
            print(f"ID: {student['id']}\n")

    # function to display list of students

    def displayList(self):
        print("Displaying list of students...")
        for i in range(len(self.student_df)):
            self.displayStudent(i)
        print("All students displayed successfully.\n")

    # function to search student by name or id

    def searchStudent(self, value):
        value = str(value)
        found = False
        for index in range(len(self.student_df)):
            if self.student_df.loc[index, 'id'] == value or self.student_df.loc[index, 'name'] == value:
                found = True
                print("Search Results: ")
                self.displayStudent(index)
        if not found:
            print(f"Student '{value}' not found.\n")

  # function to edit/update student information

    def updateStudent(self, value, newName, newCourse):
        if newCourse not in self.course_list:
            print("Invalid course.")
            return
        else:
            found = False
            for index in range(len(self.student_df)):
                if self.student_df.loc[index, 'id'] == value or self.student_df.loc[index, 'name'] == value:
                    found = True
                    # if self.student_df['id'].isin([newID]).any():
                    # if str(newID) in str(self.student_df['id'].values):
                    #    print("Student ID already exists.")
                    # else:
                    self.student_df.at[index, 'name'] = newName
                    # self.student_df.at[index, 'id'] = newID
                    self.student_df.at[index, 'course'] = newCourse
                    self.student_df.to_csv('student_info.csv', index=False)
                    print(
                        f"Student '{value}' information updated successfully.\n")

                    #
            if not found:
                print(f"Student '{value}' not found.")

#
courseObject = Course()
studentObject = StudentInfo()
