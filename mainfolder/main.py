import sys
from PySide6.QtWidgets import QApplication
from database.db import get_connection, init_db
from nucleo.library import Library
from ui.main_window import MainWindow

def main():
    conn = get_connection()
    init_db(conn)
    lib = Library(conn)
    app = QApplication(sys.argv)
    janela = MainWindow(lib)
    janela.show()
    app.exec()

    conn.close()

if __name__ == "__main__":
        main()