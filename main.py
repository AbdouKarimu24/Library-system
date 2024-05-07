import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.uic import loadUi
#import mysql.connector as connector # type: ignore
#the ignore is to be removed latter

class LoginApp(QDialog):
    def __init__(self):
        super(LoginApp, self).__init__()
        loadUi("login.ui", self)
        self.b1.clicked.connect(self.login)
        self.b2.clicked.connect(self.show_reg)

    def login(self):
        un = self.tb1.text()
        pw = self.tb2.text()
        db = con.connect(host = "localhost", usr="root",password="", db="") #database found here
        cursor = db.cursor()
        cursor.execute("select * from userlist where username'"+ un +"' password = '"+ pw +"'")#database on table userlist and column username
        result = cursor.fetchone()
        self.tb1.setText("")
        self.tb2.setText("")
        #too see if the user is register
        if result:
            QMessageBox.information(self,"login output", "congrats!! you have login sucessfuly!!")
        else:
            QMessageBox.information(self,"login output", "Invalid user.. Try again Or Register for new user")
    def show_reg(self):
        Widgets.setCurrentIndex(1)


class ReginApp(QDialog):
    def __init__(self):
        super(ReginApp, self).__init__()
        loadUi("registerform.ui", self)
        self.b3.clicked.connect(self.reg)
        self.b4.clicked.connect(self.show_login)

    
    def reg(self):
        un = self.tb3.text()
        pw = self.tb4.text()
        em = self.tb5.text()
        ph = self.tb6.text()

        #connect to databse 
        db = con.connect(host = "localhost", usr="root",password="", db="")
        cursor = db.cursor()
        cursor.execute("select * from userlist where username = '"+ un +"' and password = '"+ pw +"'")
        result = cursor.fetchone()

        if result:
            QMessageBox.information(self,"login form", "the user already registered, Try another oser name!!! ")
        else:
            cursor.execute("insert into userlist value('"+ un +"', '"+ pw +"', '"+ em +"', '"+ ph +"' )")#userlist is the table name for the database
            db.commit()
            QMessageBox.information(self,"login form", "th user registered successfully, Login now")
            self.tb3.setText("")
            self.tb4.setText("")
            self.tb5.setText("")
            self.tb6.setText("")

            
    def show_login(self):
        Widgets.setCurrentIndex(0)




app = QApplication(sys.argv)
Widgets = QtWidgets.QStackedWidget()
loginform = LoginApp()
Registrationform =ReginApp()
Widgets.addWidget(loginform)
Widgets.addWidget(Registrationform)
Widgets.setCurrentIndex(0)
Widgets.setFixedWidth(400)
Widgets.setFixedHeight(400)
Widgets.show()



app.exec_()