
from PySide6.QtWidgets import *
import PySide6.QtCore as QtCore
from nucleo.library import Library
from services.anilist import searchForAnime, AniListError
from PySide6.QtGui import QPixmap
from services.covers import load_cover

# modelo da janela principal

class MainWindow(QMainWindow):
    ALL_ANIME = "All Anime"
    def __init__(self, lib):
        
        super().__init__() 
        # "A função super() em Python é usada para acessar métodos e atributos da classe pai (superclasse)
        #  a partir de uma classe filha (subclasse)."
        self.cover_pixmap = None
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
        lists_title = QLabel("Lists")
        lists_title.setObjectName("heading")
        left.addWidget(lists_title)
        left.addWidget(self.lists_widget)
        self.new_list_btn = QPushButton("New List")
        self.delete_list_btn = QPushButton("Delete List")
        left.addWidget(self.new_list_btn)
        left.addWidget(self.delete_list_btn)

        # painel do meio (tabela)

        self.table = QTableWidget(0, 3)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setHorizontalHeaderLabels(["Title", "My Rating", "User Rating"])
        self.table.verticalHeader().hide()
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        middle = QVBoxLayout()
        self.viewer_label = QLabel("List Viewer")
        self.viewer_label.setObjectName("heading")
        middle.addWidget(self.viewer_label)
        middle.addWidget(self.table)
        self.rate_btn = QPushButton("Rate")
        buttons = QHBoxLayout()
        buttons.addWidget(self.rate_btn)
        self.add_to_list_btn = QPushButton("Add to List")
        self.remove_from_list_btn = QPushButton("Remove from List")
        self.remove_anime_btn = QPushButton("Remove Anime")
        self.rank_box = QCheckBox("Rank by rating?")
        buttons.addWidget(self.add_to_list_btn)
        buttons.addWidget(self.remove_from_list_btn)
        buttons.addWidget(self.rank_box)
        buttons.addWidget(self.remove_anime_btn)

        middle.addLayout(buttons)

        # painel da direita (detalhes do anime selecionado)
        self.cover_label = QLabel()
        self.cover_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        self.cover_label.setAlignment(QtCore.Qt.AlignCenter)
        
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
        self.new_list_btn.clicked.connect(self.on_new_list)
        self.delete_list_btn.clicked.connect(self.on_delete_list)
        self.add_to_list_btn.clicked.connect(self.on_add_to_list)
        self.remove_from_list_btn.clicked.connect(self.on_remove_from_list)
        self.remove_anime_btn.clicked.connect(self.on_remove_anime)
        self.rank_box.toggled.connect(lambda checked: self.refresh_current())

        for btn in self.findChildren(QPushButton):
            btn.setCursor(QtCore.Qt.PointingHandCursor)

        self.refresh_lists()
        self.refresh_current()


    def refresh_table(self, animes):
        self.shown_animes = animes
        self.table.setRowCount(len(animes))
        for row, anime in enumerate(animes):
            self.table.setItem(row, 0, QTableWidgetItem(anime.title))
            self.table.setItem(row, 1, QTableWidgetItem(str(anime.rating) if anime.rating is not None else "-"))
            score = f"{anime.anilist_score / 10:.1f}" if anime.anilist_score is not None else "-"
            self.table.setItem(row, 2, QTableWidgetItem(score))
    def show_info(self, row, column):
        anime = self.shown_animes[row]
        info_text = f"Title: {anime.title}\n"
        info_text += f"Genres: {', '.join(anime.genres)}\n"
        info_text += f"Episodes: {anime.episodes if anime.episodes is not None else 'Unknown'}\n"
        info_text += f"My Rating: {anime.rating if anime.rating is not None else 'Not rated'}\n"
        info_text += f"User Rating: {anime.anilist_score / 10:.1f}" if anime.anilist_score is not None else "User Rating: Unknown"
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
        self.cover_pixmap = None
        self.cover_label.clear()
        data = load_cover(url)
        if data is None:
            return
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.cover_pixmap = pixmap
        self.update_cover_size()


    def update_cover_size(self):
        if self.cover_pixmap is None or self.cover_pixmap.isNull():
            return
        scaled = self.cover_pixmap.scaled(self.cover_label.width(), int(self.height() * 0.6), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.cover_label.setPixmap(scaled)
 
    def resizeEvent(self, event): # automaticamente chamado quando a janela muda d tamanho
        super().resizeEvent(event)
        self.update_cover_size()

    def refresh_current(self):
        self.viewer_label.setText(self.current_list or "All Anime")
        if self.rank_box.isChecked():
            self.refresh_table(self.lib.ranked(list_name=self.current_list))
        elif self.current_list is None:
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
    def on_list_clicked(self, item):
        if item.text() == self.ALL_ANIME:
            self.current_list = None
        else:
            self.current_list = item.text()
        self.refresh_current()

    def on_new_list(self):
        name, ok = QInputDialog.getText(self, "New List", "List name:")
        if not ok or not name.strip():
            return
        try:
            self.lib.create_list(name.strip())
        except ValueError as e:
            QMessageBox.warning(self, "Can't create list", str(e))
            return
        self.refresh_lists()

    def on_delete_list(self):
        if self.current_list is None:
            QMessageBox.information(self, "No list selected", "Select a list first.")
            return
        reply = QMessageBox.question(self, "Delete list", f"Are you sure you wan to delete the list {self.current_list}? The anime will stay in your library.")
        if reply != QMessageBox.Yes:
            return
        self.lib.removeList(self.current_list)
        self.current_list = None
        self.refresh_lists()
        self.refresh_current()

    def on_add_to_list(self):
        anime = self.selected_anime()
        if anime is None:
            return
        listnames = self.lib.listNames()
        if not listnames:
            QMessageBox.information(self, "No lists", "You have no lists. Create one first.")
            return
        listname, ok = QInputDialog.getItem(self, "Add to List", f"Choose a list to add {anime.title} to:", listnames, 0, False)
        if not ok:
            return
        self.lib.addToList(listname, anime.id)
        self.refresh_current()

    def on_remove_from_list(self):
        if self.current_list is None:
            QMessageBox.information(self, "No list selected", "Select a list first.")
            return
        anime = self.selected_anime()
        if anime is None:
            return
        self.lib.removeFromList(self.current_list, anime.id)
        self.refresh_current()

    def on_remove_anime(self):
        anime = self.selected_anime()
        if anime is None:
            return
        reply = QMessageBox.question(self, "Remove anime", f"Are you sure you want to remove {anime.title} from your library? This will also remove it from all lists.")
        if reply != QMessageBox.Yes:
            return
        self.lib.remove(anime.id)
        self.info_label.setText("Select an anime")
        self.cover_label.clear()
        self.refresh_current()
    
    