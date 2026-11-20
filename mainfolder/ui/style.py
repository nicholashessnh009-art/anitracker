QSS = """

QWidget {
    background-color: #121212;
    color: #FFFFFF;
    font-family: "Segoe UI", arial;
    font-size: 13px;

       }
QLabel#heading {
font-size: 18px;
font-weight: bold;
}
QLineEdit, QListWidget, QTableWidget {
background-color: #181818;
border: none;
border-radius: 8px;
padding: 6px;
}

QListWidget::item, QTableWidget::item {
padding: 6px;
}

QListWidget::item:selected, QTableWidget::item:selected {
background-color: #2a2a2a;
color: #a43ae0;
font-weight: bold;
}

QHeaderView::section {
background-color: #181818;
color: #b3b3b3;
border: none;
padding: 6px;
}

QPushButton {
background-color: #a43ae0;
color: #000000;
border: none;
border-radius: 16px;
padding: 8px 16px;
/* cursor: pointer; */
font-weight: bold;
}

QPushButton:hover {
    background-color: #8a2be2;
}

QCheckBox {
    color: #b3b3b3;
    font-weight: bold;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #b3b3b3;
    border-radius: 4px;
    }

QCheckBox::indicator:checked {
    background-color: #a43ae0;
    border-color: #a43ae0;
    }


"""