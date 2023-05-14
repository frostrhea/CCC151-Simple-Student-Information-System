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
        self.setComboBoxModel() 
        self.gui_ssis.addStudentButton.clicked.connect(self.add_student_button_clicked)
        self.gui_ssis.searchCourseButton.clicked.connect(self.search_course_button_clicked)
        self.gui_ssis.searchStudentButton.clicked.connect(self.search_student_button_clicked)
        
    def setSModel(self, pdCSV, model):
        for row in range(len(pdCSV)):
            for column in range(len(pdCSV.columns)):
                text = str(pdCSV.iloc[row, column])
                item = QtGui.QStandardItem(text)
                model.setItem(row, column, item)
                print(f"text: {text}")
                if column == 2:
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
        for i in range(header.count()):
            if table == self.gui_ssis.StudentTable:
                header.resizeSection(i, 240)
            elif table == self.gui_ssis.CourseTable:
                header.resizeSection(i, 360)

    def clearModel(self, model, rows=0, cols=0):
        model.clear()
        model.setRowCount(rows)
        model.setColumnCount(cols)

    def setStandardItemModel(self):
        self.studentModel = QtGui.QStandardItemModel()
        self.courseModel = QtGui.QStandardItemModel()
        self.studentModel = self.setSModel(self.studentObject.returnStudentCSV(), self.studentModel)
        self.courseModel = self.setSModel(self.courseObject.returnCourseCSV(), self.courseModel)
        #self.modelSetter()
        
    #def modelSetter(self):
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
        
        self.courseModel = self.setSModel(self.courseObject.returnCourseCSV(), self.courseModel)
        self.gui_ssis.CourseTable.setModel(self.courseModel)
        self.adjustTableColumns(self.gui_ssis.CourseTable)
        self.gui_ssis.CourseTable.model().layoutChanged.emit()
    
    def add_student_button_clicked(self):
        student_name = self.gui_ssis.enterSName.text()
        student_id = self.gui_ssis.enterID.text()
        student_course = self.gui_ssis.chooseCourse.currentText() 
        self.studentObject.addStudent(student_name, student_id, student_course)
        
        self.studentModel = self.setSModel(self.studentObject.returnStudentCSV(), self.studentModel)
        self.gui_ssis.StudentTable.setModel(self.studentModel)
        self.adjustTableColumns(self.gui_ssis.StudentTable)
        self.gui_ssis.StudentTable.model().layoutChanged.emit()
    
    #clear combo box and populate items based on course_list df
    def setComboBoxModel(self):
        self.gui_ssis.chooseCourse.clear() 
        self.gui_ssis.chooseCourse.addItems(csvObject.course_list) 
        
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

    
    
    
    
    
    def uiReturner(self):
            return self.gui_ssis

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    window = MainWindow(ui)
    ui = window.uiReturner()
    # ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())

