import sys
from PyQt5.QtWidgets import QApplication
from interfaz import GestorCatalogoApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setStyle("Fusion")
    app.setStyleSheet("""
        QMainWindow {
            background-color: #F5F5F5;
        }
        QLabel {
            color: #333333;
        }
        QPushButton {
            background-color: #E0E0E0;
            border: 1px solid #BDBDBD;
            border-radius: 4px;
            padding: 5px 10px;
        }
        QPushButton:hover {
            background-color: #BDBDBD;
        }
        QLineEdit, QTextEdit {
            border: 1px solid #BDBDBD;
            border-radius: 4px;
            padding: 5px;
        }
        QListWidget {
            background-color: white;
            border: 1px solid #BDBDBD;
            border-radius: 4px;
        }
    """)
    
    ventana = GestorCatalogoApp()
    ventana.show()
    sys.exit(app.exec_())