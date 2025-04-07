from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices, QPixmap, QIcon
import qtawesome as qta
from backend.settings import Settings

class CompleteWindow(QMainWindow):
    def __init__(self, settings, parent=None):
        super(CompleteWindow, self).__init__(parent)

        self.settings = settings

        self.setWindowTitle(self.settings.translate("Driver Yükleyici - Tamamlandı"))
        self.setGeometry(100, 100, 600, 400)

        self.initUI()

    def initUI(self):
        # Main Container
        container = QWidget()
        self.setCentralWidget(container)
        mainLayout = QVBoxLayout(container)

        # Top Right Layout for Theme and Language Buttons
        topRightLayout = QHBoxLayout()
        topRightLayout.addStretch()

        # Theme Toggle Button
        self.themeButton = QPushButton(self)
        self.themeButton.setIcon(qta.icon('fa5s.moon'))
        self.themeButton.setFixedSize(24, 24)
        self.themeButton.setStyleSheet("border: none;")
        self.themeButton.clicked.connect(self.changeTheme)
        topRightLayout.addWidget(self.themeButton)

        # Language Toggle Button
        self.languageButton = QPushButton(self)
        self.languageButton.setIcon(QIcon("resources/tr_flag.png"))
        self.languageButton.setFixedSize(24, 24)
        self.languageButton.setStyleSheet("border: none;")
        self.languageButton.clicked.connect(self.changeLanguage)
        topRightLayout.addWidget(self.languageButton)

        mainLayout.addLayout(topRightLayout)

        # Logo
        self.logo = QLabel(self)
        pixmap = QPixmap("resources/logo.png")
        self.logo.setPixmap(pixmap.scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio))
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(self.logo)

        # Success Message
        self.successMessage = QLabel(self.settings.translate("KURULUM TAMAMLANDI!\nDriverlar başarılı bir şekilde yüklendi."), self)
        self.successMessage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.successMessage.setStyleSheet("font-size: 18px; color: #2E8B57; margin-top: 20px;")
        mainLayout.addWidget(self.successMessage)

        # Website Button
        self.websiteButton = QPushButton(self.settings.translate("Web Sitemizi Ziyaret Edin"), self)
        self.websiteButton.setStyleSheet("""
            QPushButton {
                background-color: #457B9D;
                color: white;
                font-size: 14px;
                padding: 5px 10px;
                border-radius: 10px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #1D3557;
            }
        """)
        self.websiteButton.clicked.connect(self.openWebsite)
        mainLayout.addWidget(self.websiteButton, alignment=Qt.AlignmentFlag.AlignCenter)

        # Bottom Container
        bottomLayout = QHBoxLayout()

        # About Section
        self.aboutTitle = QLabel(self.settings.translate("Hakkında"), self)
        self.aboutTitle.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.aboutTitle.setStyleSheet("font-size: 16px; font-weight: bold; color: #1D3557; margin-bottom: 10px;")

        self.aboutText = QLabel(self.settings.translate("Bu uygulama, tüm driver'larınızı kolay ve hızlı bir şekilde yüklemenize yardımcı olur."), self)
        self.aboutText.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.aboutText.setWordWrap(True)
        self.aboutText.setStyleSheet("font-size: 14px; color: #000000; margin-bottom: 20px;")

        aboutLayout = QVBoxLayout()
        aboutLayout.addWidget(self.aboutTitle)
        aboutLayout.addWidget(self.aboutText)
        aboutLayout.addStretch()  # Push content to bottom
        bottomLayout.addLayout(aboutLayout)

        # Empty Space in the Middle
        bottomLayout.addStretch()

        # Contact Information
        self.contactTitle = QLabel(self.settings.translate("Teknik Servis"), self)
        self.contactTitle.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.contactTitle.setStyleSheet("font-size: 16px; font-weight: bold; color: #1D3557; margin-bottom: 10px;")

        self.contactInfo = QLabel(self.settings.translate(
            "Teknik Servis: +90 123 456 78 90\n"
            "Çalışma Saatleri: 09:00 - 18:00\n"
            "E-posta: destek@driverinstaller.com"
        ), self)
        self.contactInfo.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.contactInfo.setStyleSheet("font-size: 14px; color: #000000; margin-bottom: 20px;")

        contactLayout = QVBoxLayout()
        contactLayout.addWidget(self.contactTitle)
        contactLayout.addWidget(self.contactInfo)
        contactLayout.addStretch()  # Push content to bottom
        bottomLayout.addLayout(contactLayout)

        mainLayout.addLayout(bottomLayout)

        self.applyTheme(self.settings.current_theme)

    def applyTheme(self, theme):
        self.setStyleSheet(self.settings.get_theme())

    def retranslateUi(self):
        self.setWindowTitle(self.settings.translate("Driver Yükleyici - Tamamlandı"))
        self.successMessage.setText(self.settings.translate("KURULUM TAMAMLANDI!\nDriverlar başarılı bir şekilde yüklendi."))
        self.aboutTitle.setText(self.settings.translate("Hakkında"))
        self.aboutText.setText(self.settings.translate("Bu uygulama, tüm driver'larınızı kolay ve hızlı bir şekilde yüklemenize yardımcı olur."))
        self.contactTitle.setText(self.settings.translate("Teknik Servis"))
        self.contactInfo.setText(self.settings.translate(
            "Teknik Servis: +90 123 456 78 90\n"
            "Çalışma Saatleri: 09:00 - 18:00\n"
            "E-posta: destek@driverinstaller.com"
        ))
        self.websiteButton.setText(self.settings.translate("Web Sitemizi Ziyaret Edin"))

    def openWebsite(self):
        QDesktopServices.openUrl(QUrl("https://www.driverinstaller.com"))

    def changeTheme(self):
        if self.settings.current_theme == "light":
            self.settings.set_theme("dark")
            self.themeButton.setIcon(qta.icon('fa5s.sun'))
        else:
            self.settings.set_theme("light")
            self.themeButton.setIcon(qta.icon('fa5s.moon'))

        self.applyTheme(self.settings.current_theme)

    def changeLanguage(self):
        if self.settings.current_language == "tr":
            self.settings.set_language("en")
            self.languageButton.setIcon(QIcon("resources/en_flag.png"))
        else:
            self.settings.set_language("tr")
            self.languageButton.setIcon(QIcon("resources/tr_flag.png"))

        self.retranslateUi()


if __name__ == "__main__":
    from backend.settings import Settings
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    settings = Settings()
    window = CompleteWindow(settings)
    window.show()

    sys.exit(app.exec())