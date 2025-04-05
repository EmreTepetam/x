import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
import qtawesome as qta
from backend.settings import Settings
from gui.install_window import InstallWindow


class MainWindow(QMainWindow):
    def __init__(self, settings, parent=None):
        super(MainWindow, self).__init__(parent)

        self.settings = settings

        self.setWindowTitle(self.settings.translate("Driver Yükleyici"))
        self.setGeometry(100, 100, 400, 300)

        self.initUI()

    def initUI(self):
        # Logo
        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap("resources/logo.png"))
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        self.title = QLabel(self.settings.translate("Driver Yükleyici"), self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1D3557;")

        # Start Button
        self.startButton = QPushButton(self.settings.translate("Yüklemeye Başla"), self)
        self.startButton.setStyleSheet("""
            QPushButton {
                background-color: #457B9D;
                color: white;
                font-size: 18px;
                padding: 10px 20px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #1D3557;
            }
        """)
        self.startButton.clicked.connect(self.openInstallWindow)

        # Theme Toggle Button
        self.themeButton = QPushButton(self)
        self.themeButton.setIcon(qta.icon('fa5s.moon'))
        self.themeButton.setFixedSize(30, 30)
        self.themeButton.setStyleSheet("border: none;")
        self.themeButton.clicked.connect(self.changeTheme)

        # Language Toggle Button
        self.languageButton = QPushButton(self)
        self.languageButton.setIcon(QIcon("resources/tr_flag.png"))
        self.languageButton.setFixedSize(30, 30)
        self.languageButton.setStyleSheet("border: none;")
        self.languageButton.clicked.connect(self.changeLanguage)

        # Top Right Layout for Theme and Language Buttons
        topRightLayout = QHBoxLayout()
        topRightLayout.addStretch()
        topRightLayout.addWidget(self.themeButton)
        topRightLayout.addWidget(self.languageButton)

        # Main Layout
        layout = QVBoxLayout()
        layout.addLayout(topRightLayout)
        layout.addWidget(self.logo)
        layout.addWidget(self.title)
        layout.addWidget(self.startButton, alignment=Qt.AlignmentFlag.AlignCenter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.applyTheme(self.settings.current_theme)

    def openInstallWindow(self):
        self.installWindow = InstallWindow(self.settings)
        self.installWindow.show()
        self.close()  # Mevcut pencereyi kapat

    def changeTheme(self):
        if self.settings.current_theme == "light":
            self.settings.set_theme("dark")
            self.themeButton.setIcon(qta.icon('fa5s.sun'))
        else:
            self.settings.set_theme("light")
            self.themeButton.setIcon(qta.icon('fa5s.moon'))

        self.applyTheme(self.settings.current_theme)

    def applyTheme(self, theme):
        self.setStyleSheet(self.settings.get_theme())

    def changeLanguage(self):
        if self.settings.current_language == "tr":
            self.settings.set_language("en")
            self.languageButton.setIcon(QIcon("resources/en_flag.png"))
        else:
            self.settings.set_language("tr")
            self.languageButton.setIcon(QIcon("resources/tr_flag.png"))

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle(self.settings.translate("Driver Yükleyici"))
        self.title.setText(self.settings.translate("Driver Yükleyici"))
        self.startButton.setText(self.settings.translate("Yüklemeye Başla"))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    settings = Settings()
    window = MainWindow(settings)
    window.show()

    sys.exit(app.exec())