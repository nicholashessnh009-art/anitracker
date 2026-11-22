
from PySide6.QtWidgets import *
import PySide6.QtCore as QtCore
from nucleo.library import Library
from services.anilist import searchForAnime, AniListError
from PySide6.QtGui import QPixmap
from services.covers import load_cover

# modelo da janela principal

class MainWindow(QMainWindow):
    
    def __init__(self, lib: Library):
        
        super().__init__() 
        # "A função super() em Python é usada para acessar métodos e atributos da classe pai (superclasse)
        #  a partir de uma classe filha (subclasse)."

        self.ALL_ANIME = self.tr("All Anime")
        self.SORT_DEFAULT = self.tr("Order added")
        self.SORT_TITLE = self.tr("title (A-Z)")
        self.SORT_MY_RATING = self.tr("my rating (high to low)")
        self.SORT_USER_RATING = self.tr("user rating (high to low)")

        self.cover_pixmap = None
        self.lib = lib
        self.setWindowTitle("AniTracker")
        self.resize(1000, 600)

        # barra de pesquisa
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(self.tr("Search for an anime..."))
        self.search_btn = QPushButton(self.tr("Search"))
        top_bar = QHBoxLayout()
        top_bar.addWidget(self.search_box)
        top_bar.addWidget(self.search_btn)

        # painel de listas
        self.lists_widget = QListWidget()
        left = QVBoxLayout()
        lists_title = QLabel(self.tr("Lists"))
        lists_title.setObjectName("heading")
        left.addWidget(lists_title)
        left.addWidget(self.lists_widget)
        self.new_list_btn = QPushButton(self.tr("New List"))
        self.delete_list_btn = QPushButton(self.tr("Delete List"))
        left.addWidget(self.new_list_btn)
        left.addWidget(self.delete_list_btn)

        # painel do meio (tabela)

        self.table = QTableWidget(0, 3)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setHorizontalHeaderLabels([self.tr("Title"), self.tr("My Rating"), self.tr("User Rating")])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setColumnWidth(1, 110)
        self.table.setColumnWidth(2, 110)
        self.table.verticalHeader().hide()
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setHighlightSections(False)
        self.table.horizontalHeader().setSectionsClickable(False)
        middle = QVBoxLayout()
        self.viewer_label = QLabel(self.tr("List Viewer"))
        self.viewer_label.setObjectName("heading")
        middle.addWidget(self.viewer_label)
        middle.addWidget(self.table)
        self.rate_btn = QPushButton(self.tr("Rate"))
        buttons = QHBoxLayout()
        buttons.addWidget(self.rate_btn)
        self.add_to_list_btn = QPushButton(self.tr("Add to List"))
        self.remove_from_list_btn = QPushButton(self.tr("Remove from List"))
        self.remove_anime_btn = QPushButton(self.tr("Remove Anime"))
        self.sort_box = QComboBox()
        self.sort_box.addItems([self.SORT_DEFAULT, self.SORT_TITLE, self.SORT_MY_RATING, self.SORT_USER_RATING])
        
        buttons.addWidget(self.add_to_list_btn)
        buttons.addWidget(self.remove_from_list_btn)
        buttons.addWidget(QLabel(self.tr("Sort by:")))
        buttons.addWidget(self.sort_box)
        buttons.addWidget(self.remove_anime_btn)

        middle.addLayout(buttons)

        # painel da direita (detalhes do anime selecionado)
        self.cover_label = QLabel()
        self.cover_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        self.cover_label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.info_label = QLabel(self.tr("Select an anime"))
        self.info_label.setWordWrap(True)
        right = QVBoxLayout()
        self.anime_info_title = QLabel(self.tr("Anime Info"))
        self.anime_info_title.setObjectName("heading")
        right.addWidget(self.anime_info_title)
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
        self.sort_box.currentIndexChanged.connect(lambda index: self.refresh_current())

        for btn in self.findChildren(QPushButton):
            btn.setCursor(QtCore.Qt.PointingHandCursor)
        for elem in self.findChildren(QComboBox):
            elem.setCursor(QtCore.Qt.PointingHandCursor)

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
        genres = ', '.join(anime.genres)
        episodes = anime.episodes if anime.episodes is not None else self.tr('Unknown')
        myrating = anime.rating if anime.rating is not None else self.tr('Not rated')
        user_rating = f"{anime.anilist_score / 10:.1f}" if anime.anilist_score is not None else self.tr("Unknown")
        
        info_text = self.tr("Title: {title}\n").format(title = anime.title) #### FALTA TRADUZIR, NICHJOLÇAS
        info_text += self.tr("Genres: {genres}\n").format(genres = genres)
        info_text += self.tr("Episodes: {episodes}\n").format(episodes = episodes)
        info_text += self.tr("My Rating: {myrating}\n").format(myrating = myrating)
        info_text += self.tr("User Rating: {user_rating}").format(user_rating = user_rating)
        self.info_label.setText(info_text)
        self.show_cover(anime.cover_url)

    def on_search(self):
        text = self.search_box.text()
        try:
            results = searchForAnime(text, limit = 12)
        except AniListError as e:
            QMessageBox.warning(self, self.tr("Search Error"), str(e))
            return
        if not results:
            QMessageBox.information(self, self.tr("Search"), self.tr("No results"))
            return
        titles = [self.tr("{title} ({episodes} episodes)").format(title=a.title, episodes=a.episodes or "?") for a in results]
        choice, check = QInputDialog.getItem(self, self.tr("Search Results"), self.tr("Choose an anime to add"), titles, 0, False)
        if not check:
            return
        anime = results[titles.index(choice)]
        try:
            self.lib.add(anime)
        except ValueError as e:
            QMessageBox.warning(self, self.tr("Can't add"), str(e))
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
        self.viewer_label.setText(self.current_list or self.tr("All Anime"))
        if self.current_list is None:
            animes = self.lib.all()
        else:
            animes = self.lib.getList(self.current_list)
        sort_method = self.sort_box.currentText()
        if sort_method == self.SORT_TITLE:
            animes = sorted(animes, key=lambda a: a.title.lower())
        elif sort_method == self.SORT_MY_RATING:
            animes = self.lib.ranked(list_name = self.current_list)
        elif sort_method == self.SORT_USER_RATING:
            animes = sorted(animes, key=lambda a: a.anilist_score or 0, reverse=True)
        self.refresh_table(animes)

    def refresh_lists(self):
        self.lists_widget.clear()
        self.lists_widget.addItem(self.ALL_ANIME)
        self.lists_widget.addItems(self.lib.listNames())

    def selected_anime(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, self.tr("No anime selected"), self.tr("Click an anime in the table first"))
            return None
        return self.shown_animes[row]
    def on_rate(self):
        anime = self.selected_anime()
        if anime is None:
            return
        rating, ok = QInputDialog.getInt(self, self.tr("Rate"), self.tr("Rating for {title} (1-10):").format(title=anime.title), anime.rating or 5, 1, 10)
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
        name, ok = QInputDialog.getText(self, self.tr("New List"), self.tr("List name:"))
        if not ok or not name.strip():
            return
        try:
            self.lib.create_list(name.strip())
        except ValueError as e:
            QMessageBox.warning(self, self.tr("Can't create list"), str(e))
            return
        self.refresh_lists()

    def on_delete_list(self):
        if self.current_list is None:
            QMessageBox.information(self, self.tr("No list selected"), self.tr("Select a list first."))
            return
        reply = QMessageBox.question(self, self.tr("Delete list"), self.tr("Are you sure you want to delete the list {current_list}? The anime will stay in your library.").format(current_list = self.current_list)) ## traduzir
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
            QMessageBox.information(self, self.tr("No lists"), self.tr("You have no lists. Create one first."))
            return
        listname, ok = QInputDialog.getItem(self, self.tr("Add to List"), self.tr("Choose a list to add {title} to:").format(title = anime.title), listnames, 0, False) ## traduzir
        if not ok:
            return
        self.lib.addToList(listname, anime.id)
        self.refresh_current()

    def on_remove_from_list(self):
        if self.current_list is None:
            QMessageBox.information(self, self.tr("No list selected"), self.tr("Select a list first."))
            return
        anime = self.selected_anime()
        if anime is None:
            return
        reply = QMessageBox.question(self, self.tr("Remove from list"), self.tr("Are you sure?"))
        if reply != QMessageBox.Yes:
            return
        self.lib.removeFromList(self.current_list, anime.id)
        self.refresh_current()

    def on_remove_anime(self):
        anime = self.selected_anime()
        if anime is None:
            return
        reply = QMessageBox.question(self, self.tr("Remove anime"), self.tr("Are you sure you want to remove {title} from your library? This will also remove it from all lists.").format(title = anime.title)) ## traduzir
        if reply != QMessageBox.Yes:
            return
        self.lib.remove(anime.id)
        self.info_label.setText(self.tr("Select an anime"))
        self.cover_label.clear()
        self.refresh_current()
    
    