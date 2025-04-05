from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from backend.settings import Settings


class CompleteWindow(QMainWindow):
    def __init__(self, settings, parent=None):
        super(CompleteWindow, self).__init__(parent)

        self.settings = settings

        self.setWindowTitle(self.settings.translate("Driver Yükleyici - Tamamlandı"))
        self.setGeometry(100, 100, 400, 300)

        self.initUI()

    def initUI(self):
        # Title
        self.title = QLabel(self.settings.translate("Driver Yükleyici - Tamamlandı"), self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1D3557;")

        # Main Layout
        layout = QVBoxLayout()
        layout.addWidget(self.title)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.applyTheme(self.settings.current_theme)

    def applyTheme(self, theme):
        self.setStyleSheet(self.settings.get_theme())

    def retranslateUi(self):
        self.setWindowTitle(self.settings.translate("Driver Yükleyici - Tamamlandı"))
        self.title.setText(self.settings.translate("Driver Yükleyici - Tamamlandı"))