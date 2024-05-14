from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QTextBrowser, QLineEdit
from PyQt5.QtGui import QPixmap
import requests

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(717, 466)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, -20, 631, 451))
        self.label.setText("")
        self.label.setObjectName("label")
        self.cover_label = QtWidgets.QLabel(Form)
        self.cover_label.setGeometry(QtCore.QRect(130, 50, 291, 61))
        self.cover_label.setObjectName("cover_label")
        self.describtion_labels = QtWidgets.QLabel(Form)
        self.describtion_labels.setGeometry(QtCore.QRect(130, 119, 201, 21))
        self.describtion_labels.setObjectName("describtion_labels")
        self.comments_browser = QtWidgets.QTextBrowser(Form)
        self.comments_browser.setGeometry(QtCore.QRect(390, 30, 256, 192))
        self.comments_browser.setObjectName("comments_browser")
        self.download_button = QtWidgets.QPushButton(Form)
        self.download_button.setGeometry(QtCore.QRect(110, 210, 89, 25))
        self.download_button.setObjectName("download_button")
        self.read_button = QtWidgets.QPushButton(Form)
        self.read_button.setGeometry(QtCore.QRect(120, 300, 89, 25))
        self.read_button.setObjectName("read_button")
        self.comment_input = QtWidgets.QLineEdit(Form)
        self.comment_input.setGeometry(QtCore.QRect(390, 230, 256, 25))
        self.comment_input.setObjectName("comment_input")
        self.post_comment_button = QtWidgets.QPushButton(Form)
        self.post_comment_button.setGeometry(QtCore.QRect(520, 270, 89, 25))
        self.post_comment_button.setObjectName("post_comment_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Book Details"))
        self.cover_label.setText(_translate("Form", "Book Covers"))
        self.describtion_labels.setText(_translate("Form", "Description"))
        self.download_button.setText(_translate("Form", "Download"))
        self.read_button.setText(_translate("Form", "Read"))
        self.post_comment_button.setText(_translate("Form", "Post Comment"))

class BookDetailsPage(QMainWindow):
    def __init__(self, book):
        super().__init__()
        self.book = book

        self.setWindowTitle("Book Details")
        self.resize(800, 600)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.read_button.clicked.connect(self.read_book)
        self.ui.download_button.clicked.connect(self.download_book)
        self.ui.post_comment_button.clicked.connect(self.post_comment)

        self.populate_details()

    def populate_details(self):
        self.ui.cover_label.setPixmap(QPixmap(self.book['cover_url']).scaled(200, 300))
        self.ui.describtion_labels.setText(self.book['description'])

        # Fetch comments from API and populate the comments_browser widget
        comments = self.fetch_comments()
        self.ui.comments_browser.setText("\n".join(comments))

    def fetch_comments(self):
        # Use appropriate API endpoint to fetch comments for the book
        response = requests.get("http://api.example.com/book/{}/comments".format(self.book['id']))
        if response.status_code == 200:
            return response.json().get("comments", [])
        return []

    def post_comment(self):
        # Get the comment text from the input field
        comment = self.ui.comment_input.text()

        # Make sure the comment is not empty
        if comment:
            # Use appropriate API endpoint to post a comment for the book
            payload = {"book_id": self.book['id'], "comment": comment}
            response = requests.post("http://api.example.com/book/comment", json=payload)
            if response.status_code == 201:
                # Comment posted successfully
                self.ui.comments_browser.append(comment)
                self.ui.comment_input.clear()
                
    def read_book(self):
        # Implement the logic to open and read the book
        url = self.book['read_url']
        webbrowser.open(url)

    def download_book(self):
        # Implement the logic to download the book
        url = self.book['download_url']
        response = requests.get(url)

        if response.status_code == 200:
            file_path = "path/to/save/book.pdf"  # Specify the path where you want to save the downloaded book
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print("Book downloaded successfully!")
        else:
            print("Failed to download the book.")

if __name__ == "__main__":
    app = QApplication([])
    book = {
        "id": 1,
        "cover_url": "path/to/book_cover.jpg",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    }
    window = BookDetailsPage(book)
    window.show()
    app.exec_()