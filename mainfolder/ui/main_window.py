import requests
from PySide6.QtWidgets import *
import PySide6.QtCore as QtCore
from nucleo.library import Library

# modelo da janela principal

class MainWindow(QMainWindow):
    def __init__(self, lib):
        super().__init__() 
        # "A função super() em Python é usada para acessar métodos e atributos da classe pai (superclasse)
        #  a partir de uma classe filha (subclasse)."
        self.lib = lib
        self.setWindowTitle("AniTracker")
        self.resize(1000, 600)

        # barra de pesquisa
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search for an anime...")
        self.search_btn = QPushButton("Search")
        top_bar = QHBoxLayout()
        top_bar.addWidget(self.search_box)
        top_bar.addWidget(self.search_btn)

        # painel de listas
        self.lists_widget = QListWidget()
        left = QVBoxLayout()
        left.addWidget(QLabel("Lists"))
        left.addWidget(self.lists_widget)

        # painel do meio (tabela)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Title", "Rating"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        middle = QVBoxLayout()
        middle.addWidget(QLabel("List Viewer ???"))
        middle.addWidget(self.table)

        # painel da direita (detalhes do anime selecionado)

        self.info_label = QLabel("Select an anime")
        self.info_label.setWordWrap(True)
        right = QVBoxLayout()
        right.addWidget(QLabel("Anime Info"))
        right.addWidget(self.info_label)
        right.addStretch()



        panels = QHBoxLayout()
        panels.addLayout(left, 1)
        panels.addLayout(middle, 3)
        panels.addLayout(right, 2)

        # layout principal

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_bar)
        main_layout.addLayout(panels)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # self.refresh_table(self.lib.all())
