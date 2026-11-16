import requests
from PySide6.QtWidgets import *
import PySide6.QtCore as QtCore
from nucleo.library import Library
from services.anilist import searchForAnime, AniListError
from PySide6.QtGui import QPixmap

ALL_ANIME = "All Anime"
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
        self.rate_btn = QPushButton("Rate")
        buttons = QHBoxLayout()
        buttons.addWidget(self.rate_btn)
        middle.addLayout(buttons)

        # painel da direita (detalhes do anime selecionado)
        self.cover_label = QLabel()
        
        self.info_label = QLabel("Select an anime")
        self.info_label.setWordWrap(True)
        right = QVBoxLayout()
        right.addWidget(QLabel("Anime Info"))
        right.addWidget(self.info_label)
        right.addWidget(self.cover_label)
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


        self.table.cellClicked.connect(self.show_info)
        self.search_btn.clicked.connect(self.on_search)
        self.search_box.returnPressed.connect(self.on_search)

        self.rate_btn.clicked.connect(self.on_rate)
        self.lists_widget.itemClicked.connect(self.on_list_clicked)

        self.current_list = None
        self.refresh_lists()
        self.refresh_current()


    def refresh_table(self, animes):
        self.shown_animes = animes
        self.table.setRowCount(len(animes))
        for row, anime in enumerate(animes):
            self.table.setItem(row, 0, QTableWidgetItem(anime.title))
            self.table.setItem(row, 1, QTableWidgetItem(str(anime.rating) if anime.rating is not None else "-"))
    def show_info(self, row, column):
        anime = self.shown_animes[row]
        info_text = f"Title: {anime.title}\n"
        info_text += f"Genres: {', '.join(anime.genres)}\n"
        info_text += f"Episodes: {anime.episodes if anime.episodes is not None else 'Unknown'}\n"
        info_text += f"Rating: {anime.rating if anime.rating is not None else 'Not rated'}\n"
        self.info_label.setText(info_text)
        self.show_cover(anime.cover_url)

    def on_search(self):
        text = self.search_box.text()
        try:
            results = searchForAnime(text, limit = 12)
        except AniListError as e:
            QMessageBox.warning(self, "Search Error", str(e))
            return
        if not results:
            QMessageBox.information(self, "Search", "No results")
            return
        titles = [f'{a.title} ({a.episodes or '?'} episodes)' for a in results]
        choice, check = QInputDialog.getItem(self, "Search Results", "Choose an anime to add", titles, 0, False)
        if not check:
            return
        anime = results[titles.index(choice)]
        try:
            self.lib.add(anime)
        except ValueError as e:
            QMessageBox.warning(self, "Can't add", str(e))
            return
        self.refresh_current()
        self.search_box.clear()

    def show_cover(self, url):
        self.cover_label.clear()
        if not url:
            return
        try:
            data = requests.get(url, timeout=10).content
        except requests.exceptions.RequestException:
            return
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.cover_label.setPixmap(pixmap.scaledToWidth(230, QtCore.Qt.SmoothTransformation))

    def refresh_current(self):
        if self.current_list is None:
            self.refresh_table(self.lib.all())
        else:
            self.refresh_table(self.lib.getList(self.current_list))

    def refresh_lists(self):
        self.lists_widget.clear()
        self.lists_widget.addItem(self.ALL_ANIME)
        self.lists_widget.addItems(self.lib.listNames())

    def selected_anime(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "No anime selected", "Click an anime in the table first")
            return None
        return self.shown_animes[row]
    def on_rate(self):
        anime = self.selected_anime()
        if anime is None:
            return
        rating, ok = QInputDialog.getInt(self, "Rate", f"Rating for {anime.title} (1-10):", anime.rating or 5, 1, 10)
        if not ok:
            return
        self.lib.rate(anime.id, rating)
        self.refresh_current()
    