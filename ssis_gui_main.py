import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import pandas as pd
from gui_ssis2 import Ui_MainWindow
import Student_and_Course_class as csvObject


class MainWindow(QtWidgets.QMainWindow):
    studentModel = QtGui.QStandardItemModel()
    courseModel = QtGui.QStandardItemModel()

    def __init__(self, ui):
        super().__init__()
        self.courseObject = csvObject.courseObject
        self.studentObject = csvObject.studentObject
        self.gui_ssis = ui
        self.gui_ssis.setupUi(self)
        self.setStandardItemModel()
        #print("CONSTRUCTOR IS CALLED")
        self.gui_ssis.addCourseButton.clicked.connect(self.add_course_button_clicked)
        self.gui_ssis.enterCode.returnPressed.connect(self.add_course_button_clicked)
        self.setComboBoxModel() 
        
        self.gui_ssis.addStudentButton.clicked.connect(self.add_student_button_clicked)
        #self.gui_ssis.enterID.returnPressed.connect(self.add_student_button_clicked)
        #self.gui_ssis.chooseCourse.returnPressed.connect(self.add_student_button_clicked)
        # still need to fix this such that it will add when enter is pressed
        
        self.gui_ssis.searchCourseButton.clicked.connect(self.search_course_button_clicked)
        self.gui_ssis.searchInputCourse.returnPressed.connect(self.search_course_button_clicked)
        
        self.gui_ssis.searchStudentButton.clicked.connect(self.search_student_button_clicked)
        self.gui_ssis.searchInputStudent.returnPressed.connect(self.search_student_button_clicked)
        
        self.gui_ssis.CourseTable.doubleClicked.connect(self.course_table_cell_edit)
        self.gui_ssis.StudentTable.doubleClicked.connect(self.student_table_cell_edit)
        
        self.gui_ssis.deleteCourseButton.clicked.connect(self.delete_course_row)
        self.gui_ssis.deleteStudentButton.clicked.connect(self.delete_student_row)
        
    def setSModel(self, pdCSV, model):
        for row in range(len(pdCSV)):
            for column in range(len(pdCSV.columns)):
                text = str(pdCSV.iloc[row, column])
                item = QtGui.QStandardItem(text)
                model.setItem(row, column, item)
                #print(f"text: {text}")
                if column in [0, 1, 2]:
                    item.setEditable(False)
                if column in [0, 1, 2]:
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                else:
                    item.setTextAlignment(QtCore.Qt.AlignLeft)
                model.setItem(row, column, item)
        return model
    
    def adjustTableColumns(self, table):
        header = table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        if table == self.gui_ssis.StudentTable:
                header.resizeSection(0, 348)  
                header.resizeSection(1, 151)  
                header.resizeSection(2, 200)  
        elif table == self.gui_ssis.CourseTable:
                header.resizeSection(0, 240)  
                header.resizeSection(1, 459)  

    def clearModel(self, model, rows=0, cols=0):
        model.clear()
        model.setRowCount(rows)
        model.setColumnCount(cols)

    def setStandardItemModel(self):
        self.studentModel = QtGui.QStandardItemModel()
        self.courseModel = QtGui.QStandardItemModel()
        self.studentModel = self.setSModel(self.studentObject.returnStudentCSV(), self.studentModel)
        self.courseModel = self.setSModel(self.courseObject.returnCourseCSV(), self.courseModel)
        
        self.studentModel.setHorizontalHeaderLabels(self.studentObject.columns)
        self.gui_ssis.StudentTable.setModel(self.studentModel)
        self.courseModel.setHorizontalHeaderLabels(self.courseObject.columns)
        self.gui_ssis.CourseTable.setModel(self.courseModel)
        
        self.adjustTableColumns(self.gui_ssis.StudentTable)
        self.adjustTableColumns(self.gui_ssis.CourseTable)
    
    
    def add_course_button_clicked(self):
        course_name = self.gui_ssis.enterCourse.text()
        course_code = self.gui_ssis.enterCode.text()
        self.courseObject.addCourse(course_name, course_code)
        
        self.setStandardItemModel()
        self.gui_ssis.CourseTable.model().layoutChanged.emit()
        self.setComboBoxModel()
        self.gui_ssis.enterCourse.clear()
        self.gui_ssis.enterCode.clear()
        
    #------------------------------------------------------------ 
    def add_student_button_clicked(self):
        student_name = self.gui_ssis.enterSName.text()
        student_id = self.gui_ssis.enterID.text()
        student_course = self.gui_ssis.chooseCourse.currentText()

        student_course_code = self.courseObject.getCourseCode(student_course)

        self.studentObject.addStudent(student_name, student_id, student_course_code)
        self.setStandardItemModel()
        self.gui_ssis.StudentTable.model().layoutChanged.emit()
        self.gui_ssis.enterSName.clear()
        self.gui_ssis.enterID.clear()

    def delete_course_row(self):
        selected_rows = self.gui_ssis.CourseTable.currentIndex().row()
        column_index = 0
        course = self.gui_ssis.CourseTable.model().index(selected_rows, column_index).data()
        reply = QtWidgets.QMessageBox.question(self, "Delete Confirmation", "Are you sure you want to delete this course?",
                                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.courseObject.deleteCourse(course)

        self.courseModel = self.setSModel(self.courseObject.returnCourseCSV(), self.courseModel)
        self.setStandardItemModel()
        self.gui_ssis.CourseTable.model().layoutChanged.emit()
        self.setComboBoxModel()

    
    #------
    def delete_student_row(self):
        #selection_model= self.gui_ssis.StudentTable.selectionModel()
        selected_rows = self.gui_ssis.StudentTable.currentIndex().row()
        column_index = 1
        student = self.gui_ssis.StudentTable.model().index(selected_rows, column_index).data()
        reply = QtWidgets.QMessageBox.question(self, "Delete Confirmation", "Are you sure you want to delete this student?",
                                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.studentObject.deleteStudent(student)

        self.studentModel = self.setSModel(self.studentObject.returnStudentCSV(), self.studentModel)
        self.setStandardItemModel()
        self.gui_ssis.StudentTable.model().layoutChanged.emit()

    
    #clear combo box and populate items based on course_names df
    def setComboBoxModel(self):
        self.gui_ssis.chooseCourse.clear() 
        self.gui_ssis.chooseCourse.addItems(self.courseObject.getCourseNames()) 
     
        
    def search_course_button_clicked(self): 
        search_coursetxt = self.gui_ssis.searchInputCourse.text()
        CResults_df = self.courseObject.searchCourse(search_coursetxt)
        print("Results:", CResults_df) 
        if not CResults_df.empty:
            self.clearModel(self.courseModel)
            self.courseModel = self.setSModel(CResults_df, self.courseModel)
            self.courseModel.setHorizontalHeaderLabels(self.courseObject.columns)
            self.gui_ssis.CourseTable.setModel(self.courseModel)
            self.adjustTableColumns(self.gui_ssis.CourseTable)
            self.gui_ssis.CourseTable.model().layoutChanged.emit()
        else:
            QtWidgets.QMessageBox.information(self, "No Results", f"No results found for course '{search_coursetxt}'.")
            
            
    def search_student_button_clicked(self): 
        search_studenttxt = self.gui_ssis.searchInputStudent.text()
        SResults_df = self.studentObject.searchStudent(search_studenttxt)
        print("Results:", SResults_df) 
        if not SResults_df.empty:
            self.clearModel(self.studentModel)
            self.studentModel = self.setSModel(SResults_df, self.studentModel)
            self.studentModel.setHorizontalHeaderLabels(self.studentObject.columns)
            self.gui_ssis.StudentTable.setModel(self.studentModel)
            self.adjustTableColumns(self.gui_ssis.StudentTable)
            self.gui_ssis.StudentTable.model().layoutChanged.emit()
        else:
            QtWidgets.QMessageBox.information(self, "No Results", f"No results found for course '{search_studenttxt}'.")

  #--FIXED--- 
    def course_table_cell_edit(self, index):
        row = index.row()
        column = index.column()
        item = self.gui_ssis.CourseTable.model().item(row, column)
        current_value = item.text()
        new_value, ok = QtWidgets.QInputDialog.getText(self, "Update Course", "Enter new text:", text=current_value)
        if ok and new_value:
            if new_value != current_value:
                reply = QtWidgets.QMessageBox.question(self, "Save Changes", "Do you want to save the changes?", 
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    if column == 0:
                        if self.courseObject.courseCodeExists(new_value) == True:
                            QtWidgets.QMessageBox.warning(self, "Course Code Exists", "Course code already exists.")
                        else:
                            self.courseObject.updateCourse(current_value, row, column, new_value)
                            self.setStandardItemModel()
                            self.gui_ssis.CourseTable.model().layoutChanged.emit()
                            #self.setComboBoxModel()
                    if column == 1:
                            self.courseObject.updateCourse(current_value, row, column, new_value)
                            self.setStandardItemModel()
                            self.gui_ssis.CourseTable.model().layoutChanged.emit()
                            self.setComboBoxModel()
                else:
                    pass

    def student_table_cell_edit(self, index):
        column = index.column()
        row = index.row()
        item = self.gui_ssis.StudentTable.model().item(row, column)
        current_value = item.text()
        new_value, ok = QtWidgets.QInputDialog.getText(self, "Update Student", "Enter new text:", text=current_value)
        if ok and new_value and new_value != current_value:
            reply = QtWidgets.QMessageBox.question(self, "Save Changes", "Do you want to save the changes?",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                if column == 0:  
                    self.studentObject.updateStudent(current_value, row, column, new_value)
                    self.setStandardItemModel()
                    self.gui_ssis.StudentTable.model().layoutChanged.emit()
                elif column == 1:  
                    if self.studentObject.studentIDExists(new_value) == True:
                        QtWidgets.QMessageBox.warning(self, "Student ID Exists", "Student ID already exists.")
                    else:
                        self.studentObject.updateStudent(current_value, row, column, new_value)
                        self.setStandardItemModel()
                        self.gui_ssis.StudentTable.model().layoutChanged.emit()
                elif column == 2:  # Course column
                    if self.courseObject.courseCodeNotinList(new_value) == True:
                        QtWidgets.QMessageBox.warning(self, "Course Unavailable", "Course does not exist.")
                    else:
                        self.studentObject.updateStudent(current_value, row, column, new_value)
                        self.setStandardItemModel()
                        self.gui_ssis.StudentTable.model().layoutChanged.emit()
                else:
                    pass

    # ----------------------------------------------------------------


    
    def uiReturner(self):
            return self.gui_ssis

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    window = MainWindow(ui)
    #ui = window.uiReturner()
    # ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())

