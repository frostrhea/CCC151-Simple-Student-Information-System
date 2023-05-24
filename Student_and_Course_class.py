import csv
import pandas as pd



class Course:
    def __init__(self):
        self.columns = ['courseCode', 'courseName']
        self.courses_df = pd.read_csv(
            "courses.csv", header=0, names=self.columns)
        #self.course_list = self.courses_df['courseCode'].tolist()
        #self.course_names = self.courses_df['courseName'].tolist()

    def returnCourseCSV(self):
        return self.courses_df

    # function to add a course to the list
    # Checks if input is in the list, then adds it to the list by appending it to csv
    def addCourse(self, value, code):
        if code in self.courses_df['courseCode'].values:    
            print(f"Course code already exists.")       
            return
        else:
            new_course = {'courseName': value, 'courseCode': code}
            self.courses_df = self.courses_df.append(
                new_course, ignore_index=True)
            self.courses_df.to_csv('courses.csv', index=False, header=True)
            print(f"Course '{value}' added.\n")

    #           
    # function to delete a course from the list
    # Looks for the possible index of the input, then drop it from the list if it exists
    #   then update the csv.

    def deleteCourse(self, code):
        index = self.courses_df.index[self.courses_df['courseCode'] == code].tolist()
        if not index:
            print(f"Course code '{code}' does not exist.\n")
        else:
            self.courses_df.drop(index, inplace=True)
            self.courses_df.to_csv('courses.csv', index=False)
            print(f"Course '{code}' has been deleted.\n")
            studentObject.deleteStudentUnderCourse(code)
            

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
        value = str(course).lower()
        CResults_df = pd.DataFrame(columns=self.courses_df.columns)
        for index in range(len(self.courses_df)):
            course_name = self.courses_df.loc[index, 'courseName'].lower()
            course_code = self.courses_df.loc[index, 'courseCode'].lower()
            if value in course_name or value in course_code:
                CResults_df = CResults_df.append(self.courses_df.loc[index])
        if len(CResults_df) == 0:
            print("No matching courses found.")
        else:
            print(CResults_df)
        return CResults_df



    # function to update the course name field
    # Checks the indexes, then if found, check the new name if it exists already in csv
    #    if not, updates the name field and saves the new name in csv.

    def updateCourse(self, value, row, columnIndex, newValue):
        if columnIndex == 0:  # Course code column
            self.courses_df.at[row, 'courseCode'] = newValue
            self.courses_df.at[row, 'courseCode'] = newValue
            # Update the student_info.csv file
            studentObject.updateStudentCourse(value, newValue)
        elif columnIndex == 1:  # Course name column
            self.courses_df.at[row, 'courseName'] = newValue
        self.courses_df.to_csv('courses.csv', index=False)
        print(f"Course '{value}' updated to '{newValue}' successfully.")


    def courseCodeExists(self, courseCode):
        if courseCode in self.courses_df['courseCode'].values:
            return True

    
    def courseCodeNotinList(self, course):
        if course not in self.courses_df['courseCode'].values:
            return True
        
    # Retrieve the course code based on the course name    
    def getCourseCode(self, course_name):
        row = self.courses_df.loc[self.courses_df['courseName'] == course_name]
        course_code = row['courseCode'].values[0]
        return course_code
    
    def getCourseNames(self):
        return self.courses_df['courseName'].astype(str).tolist()
    
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

class StudentInfo:
    def __init__(self):
        self.columns = ['name', 'id', 'course']
        self.student_df = pd.read_csv(
            "student_info.csv", header=0, names=self.columns)
 

    def returnStudentCSV(self):
        return self.student_df

    # function to add a student
    def addStudent(self, name, id, course):
        if any(self.student_df['id'] == id):
            print(f"Student with ID '{id}' already exists.")
            return
        else:
            new_student = {'name': name, 'id': id, 'course': course}
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
        value = str(value).lower()
        SResults_df = pd.DataFrame(columns=self.student_df.columns)
        for index in range(len(self.student_df)):
            student_name = self.student_df.loc[index, 'name'].lower()
            student_id = self.student_df.loc[index, 'id'].lower()
            student_course = self.student_df.loc[index, 'course'].lower()
            if value in student_name or value in student_id or value in student_course:
                SResults_df = SResults_df.append(self.student_df.loc[index])
        if len(SResults_df) == 0:
            print("No matching courses found.")
        else:
            print(SResults_df)
        return SResults_df

  # function to edit/update student information

    def updateStudent(self, value, row, columnIndex, newValue):
        found = False
        if columnIndex == 2:  # Student course column
            if courseObject.courseCodeExists(newValue) == True:
                found = True
                self.student_df.at[row, 'course'] = newValue
                self.student_df.to_csv('student_info.csv', index=False)
                print(f"Student's course updated successfully.\n")
            else:
                print(f"Course code '{newValue}' not found.")
                return

        if columnIndex == 0:  # Student name column
            found = True
            self.student_df.at[row, 'name'] = newValue
            self.student_df.to_csv('student_info.csv', index=False)
            print(f"Student '{value}' updated to '{newValue}' successfully.\n")
        elif columnIndex == 1:  # Student id column
            found = True
            self.student_df.at[row, 'id'] = newValue
            self.student_df.to_csv('student_info.csv', index=False)
            print(f"Student ID '{value}' updated to '{newValue}' successfully.\n")
        
        if not found:
            print(f"Student '{value}' not found.")

    def deleteStudentUnderCourse(self, code):
        self.student_df = self.student_df[self.student_df['course'] != code]
        self.student_df.to_csv('student_info.csv', index=False)
        print(f"All students under course code '{code}' have been removed.\n")

    def updateStudentCourse(self, old_course_code, new_course_code):
        self.student_df.loc[self.student_df['course'] == old_course_code, 'course'] = new_course_code
        self.student_df.to_csv('student_info.csv', index=False)
        print(f"Updated course for students with course code '{old_course_code}' to '{new_course_code}'.")

                
    def studentIDExists(self, studentID):
        student_df = self.returnStudentCSV()
        if studentID in student_df['id'].values:
            return True
    



#
courseObject = Course()
studentObject = StudentInfo()
