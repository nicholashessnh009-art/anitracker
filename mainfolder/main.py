import requests
import PySide6.QtWidgets as QtWidgets
import PySide6.QtCore as QtCore
from nucleo.library import Library

API_URL = "https://graphql.anilist.co"

## pyside6 test, delete later

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Test app')

        container = QtWidgets.QWidget()
        self.setCentralWidget(container)

        layout = QtWidgets.QHBoxLayout(container)



        label1 = QtWidgets.QLabel('Hello World1')
        label1.setAlignment(QtCore.Qt.AlignCenter)

        label2 = QtWidgets.QLabel('Hello World2')
        label2.setAlignment(QtCore.Qt.AlignCenter)

        label3 = QtWidgets.QLabel('Hello World3')
        label3.setAlignment(QtCore.Qt.AlignCenter)

        label4 = QtWidgets.QLabel('Hello World4')
        label4.setAlignment(QtCore.Qt.AlignCenter)

        button = QtWidgets.QPushButton('Click me!')
        dropdown = QtWidgets.QComboBox()
        dropdown.addItems(['First option', 'Second option'])
        layout.addWidget(button)
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)
        layout.addWidget(label4)
        layout.addWidget(dropdown)

app = QtWidgets.QApplication()
window = MainWindow()
window.show()

app.exec()


# PROGRESSSSS
