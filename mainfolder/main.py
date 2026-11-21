import sys
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore
from database.db import get_connection, init_db
from nucleo.library import Library
from ui.main_window import MainWindow
from ui.style import QSS

def main():
    conn = get_connection()
    init_db(conn)
    lib = Library(conn)
    app = QApplication(sys.argv)
    app.styleHints().setColorScheme(QtCore.Qt.ColorScheme.Dark)
    app.setStyleSheet(QSS)
    janela = MainWindow(lib)
    janela.show()
    app.exec()

    conn.close()

if __name__ == "__main__":
        main()