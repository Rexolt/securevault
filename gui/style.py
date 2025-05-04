style_sheet = """
/* Sötét téma, lekerekített ablakok és gombok */
QWidget {
    background-color: #121212;
    color: #e0e0e0;
    font-size: 14px;
}
QPushButton {
    border-radius: 8px;
    padding: 8px;
    background-color: #1f1f1f;
}
QPushButton:hover {
    background-color: #2a2a2a;
}
QLineEdit, QTableWidget {
    background-color: #1e1e1e;
    border: 1px solid #333;
    border-radius: 6px;
}
QHeaderView::section {
    background-color: #1f1f1f;
    padding: 4px;
}
"""