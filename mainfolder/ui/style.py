from pathlib import Path
from paths import BUNDLE_DIR
ARROW = (BUNDLE_DIR / "ui" / "arrow.svg").as_posix()

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

QTableWidget::item:hover {
background-color: #222222;}

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
font-weight: bold;
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



QComboBox {
    background-color: #2a2a2a;
    border: 1px solid #2a2a2a;
    border-radius: 16px;
    padding: 6px 12px;
    min-width: 120px;
    color: #FFFFFF;
    font-weight: bold;
    }

QComboBox:hover {
    background-color: #121212;
    }    

QComboBox::drop-down {
    border: none;
    width: 28px;
    }

QComboBox::down-arrow {
    image: url(ARROW_PATH);
    width: 12px;
    height: 8px;
    }

QComboBox QAbstractItemView {
    background-color: #181818;
    border: none;
    outline: none;
    padding: 4px;
    selection-background-color: #a43ae0;
    selection-color: #000000;
    }

"""

QSS = QSS.replace("ARROW_PATH", ARROW)