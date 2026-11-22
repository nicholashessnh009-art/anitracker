import sys
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore
from database.db import get_connection, init_db
from nucleo.library import Library
from ui.main_window import MainWindow
from ui.style import QSS
from pathlib import Path
from PySide6.QtCore import QTranslator, QLocale, QLibraryInfo
from paths import BUNDLE_DIR

def main(language="Português"):
    conn = get_connection()
    init_db(conn)
    lib = Library(conn)
    app = QApplication(sys.argv)
    app.styleHints().setColorScheme(QtCore.Qt.ColorScheme.Dark) # nao funciona no meu sistema :/
    app.setStyleSheet(QSS)

    # carrega traduções ptBR
    if language == "Português":
        translations = BUNDLE_DIR / "translations"
        translator = QTranslator()
        translator.load(str(translations / "anitracker_pt_br.qm"))
        app.installTranslator(translator)
        # traduz botões padrões do Qt
        qt_translator = QTranslator()
        qt_translator.load(str(translations / "qtbase_pt_BR.qm"))
        app.installTranslator(qt_translator)

    janela = MainWindow(lib)
    janela.show()
    app.exec()

    conn.close()

if __name__ == "__main__":
        main("Português") 
 ## se quiser usar o app em inglês, é só mudar language para qualquer outra coisa