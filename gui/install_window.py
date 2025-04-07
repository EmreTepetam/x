import os
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QTreeWidget, QTreeWidgetItem, QPushButton, \
    QHBoxLayout, QScrollArea, QProgressBar, QTextEdit
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QPropertyAnimation, QRect, QEasingCurve, QTimer
from PyQt6.QtGui import QPixmap, QIcon
import qtawesome as qta
from backend.settings import Settings
from backend.driver_installer import DriverInstaller
from gui.complete_window import CompleteWindow  # Import CompleteWindow


class InstallWindow(QMainWindow):
    def __init__(self, settings, parent=None):
        super(InstallWindow, self).__init__(parent)

        self.settings = settings
        self.driver_installer = DriverInstaller("drivers")  # DriverInstaller instance

        self.setWindowTitle(self.settings.translate("Driver Yükleyici - Kurulum"))
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumSize(QSize(600, 400))

        self.initUI()
        self.scanDrivers()

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

        # Title Layout
        titleLayout = QHBoxLayout()

        # Logo
        logo = QLabel(self)
        pixmap = QPixmap("resources/logo1.webp")
        logo.setPixmap(pixmap.scaled(170, 100, Qt.AspectRatioMode.KeepAspectRatio))
        titleLayout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignLeft)

        # Title
        self.title = QLabel(self.settings.translate("Kurulum Yöneticisi"), self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin-left: auto;
        """)
        titleLayout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignRight)

        mainLayout.addLayout(titleLayout)

        # Main Content Layout
        contentLayout = QHBoxLayout()

        # Left Layout
        leftLayout = QVBoxLayout()

        # Driver List
        self.driverList = QTreeWidget(self)
        self.driverList.setHeaderHidden(True)
        self.driverList.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)
        self.driverList.setStyleSheet("""
            QTreeWidget {
                border: 1px solid #1E3A5F;
                border-radius: 5px;
                background-color: #FFFFFF;
            }
            QTreeWidget::item {
                padding: 5px;
                color: #1A2B3C; /* Daha koyu renk */
            }
            QTreeWidget::item:selected {
                background-color: #87CEEB;
                color: white;
            }
            QScrollBar:vertical {
                background: #F1FAEE;
                width: 16px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #A2C2E6;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                border: none;
            }
        """)

        scrollArea = QScrollArea()
        scrollArea.setWidget(self.driverList)
        scrollArea.setWidgetResizable(True)
        leftLayout.addWidget(scrollArea)

        contentLayout.addLayout(leftLayout)

        # Right Layout
        rightLayout = QVBoxLayout()

        # Message Box
        self.messageBox = QTextEdit(self)
        self.messageBox.setReadOnly(True)
        self.messageBox.setStyleSheet("""
            QTextEdit {
                border: 1px solid #1E3A5F;
                border-radius: 5px;
                font-size: 14px;
                height: 100px;
                padding: 10px;
                background-color: #F0F0F0;
                color: #333333;
            }
        """)
        rightLayout.addWidget(self.messageBox)

        # Progress Bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setValue(0)
        self.progressBar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #1E3A5F;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #87CEEB;
                width: 20px;
            }
        """)
        rightLayout.addWidget(self.progressBar)

        # Buttons Layout
        buttonsLayout = QVBoxLayout()

        # Select All Button
        self.selectAllButton = QPushButton(self.settings.translate("Tümünü Seç"), self)
        self.selectAllButton.setStyleSheet("""
            QPushButton {
                background-color: #5D8A99;
                color: white;
                font-size: 14px;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2C3E50;
            }
        """)
        self.selectAllButton.clicked.connect(self.selectAllDrivers)
        buttonsLayout.addWidget(self.selectAllButton)

        # Deselect All Button
        self.deselectAllButton = QPushButton(self.settings.translate("Seçimleri İptal Et"), self)
        self.deselectAllButton.setStyleSheet("""
            QPushButton {
                background-color: #5D8A99;
                color: white;
                font-size: 14px;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2C3E50;
            }
        """)
        self.deselectAllButton.clicked.connect(self.deselectAllDrivers)
        buttonsLayout.addWidget(self.deselectAllButton)

        # Install Button
        self.installButton = QPushButton(self.settings.translate("Yükle"), self)
        self.installButton.setStyleSheet("""
            QPushButton {
                background-color: #E63946;
                color: white;
                font-size: 16px;
                padding: 10px 20px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #D62828;
            }
        """)
        self.installButton.clicked.connect(self.installSelectedDrivers)
        buttonsLayout.addWidget(self.installButton)

        rightLayout.addLayout(buttonsLayout)

        contentLayout.addLayout(rightLayout)
        mainLayout.addLayout(contentLayout)

        self.applyTheme(self.settings.current_theme)

    def applyTheme(self, theme):
        theme_path = os.path.join('resources', 'themes', f'{theme}.qss')
        if os.path.exists(theme_path):
            with open(theme_path, 'r') as file:
                self.setStyleSheet(file.read())
        else:
            self.updateMessageBox(f"Theme file {theme_path} not found")

    def scanDrivers(self):
        categorized_drivers = self.driver_installer.scan_and_categorize_drivers()
        self.displayDrivers(categorized_drivers)
        self.updateMessageBox("- Driver taraması tamamlandı. Sol ekranda bulunan driverlar arasında seçim yapabilir ve yüklemeye başlayabilirsiniz.")

    def displayDrivers(self, categorized_drivers):
        self.driverList.clear()
        for category, files in categorized_drivers.items():
            category_item = QTreeWidgetItem([category])
            category_item.setFlags(category_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            category_item.setCheckState(0, Qt.CheckState.Unchecked)
            self.driverList.addTopLevelItem(category_item)
            category_item.setExpanded(False)  # Kategoriler varsayılan olarak açık

            for file in files:
                file_item = QTreeWidgetItem([os.path.basename(file)])
                file_item.setFlags(file_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                file_item.setCheckState(0, Qt.CheckState.Unchecked)
                category_item.addChild(file_item)

        self.driverList.itemChanged.connect(self.handleItemChanged)

    def handleItemChanged(self, item, column):
        self.driverList.blockSignals(True)
        if item.childCount() > 0:  # Kategori öğesi
            for child_index in range(item.childCount()):
                child = item.child(child_index)
                child.setCheckState(0, item.checkState(0))
        else:  # Alt öğe
            parent = item.parent()
            if parent is not None:
                all_checked = all(parent.child(child_index).checkState(0) == Qt.CheckState.Checked
                                  for child_index in range(parent.childCount()))
                if all_checked:
                    parent.setCheckState(0, Qt.CheckState.Checked)
                else:
                    parent.setCheckState(0, Qt.CheckState.Unchecked)
        self.driverList.blockSignals(False)

    def selectAllDrivers(self):
        self.driverList.blockSignals(True)
        for index in range(self.driverList.topLevelItemCount()):
            category_item = self.driverList.topLevelItem(index)
            category_item.setCheckState(0, Qt.CheckState.Checked)
            for child_index in range(category_item.childCount()):
                item = category_item.child(child_index)
                item.setCheckState(0, Qt.CheckState.Checked)
        self.driverList.blockSignals(False)
        # Mesaj kutusuna seçim bilgisi yazılmayacak.

    def deselectAllDrivers(self):
        self.driverList.blockSignals(True)
        for index in range(self.driverList.topLevelItemCount()):
            category_item = self.driverList.topLevelItem(index)
            category_item.setCheckState(0, Qt.CheckState.Unchecked)
            for child_index in range(category_item.childCount()):
                item = category_item.child(child_index)
                item.setCheckState(0, Qt.CheckState.Unchecked)
        self.driverList.blockSignals(False)
        # Mesaj kutusuna seçim bilgisi yazılmayacak.

    def installSelectedDrivers(self):
        selected_drivers = []
        for index in range(self.driverList.topLevelItemCount()):
            category_item = self.driverList.topLevelItem(index)
            for child_index in range(category_item.childCount()):
                item = category_item.child(child_index)
                if item.checkState(0) == Qt.CheckState.Checked:
                    selected_drivers.append(self.driver_installer.getFullPath(category_item, item.text(0)))

        self.thread = DriverInstallThread(self.driver_installer, selected_drivers)
        self.thread.progress.connect(self.updateProgressBar)
        self.thread.status.connect(self.showStatusMessage)
        self.thread.finished.connect(self.onInstallFinished)  # Connect to onInstallFinished
        self.thread.start()
        self.updateMessageBox("Driver yükleme işlemi başlatıldı.")

    def updateProgressBar(self, value):
        self.progressBar.setValue(value)

    def showStatusMessage(self, message):
        self.updateMessageBox(message)

    def updateMessageBox(self, message):
        current_text = self.messageBox.toPlainText()
        new_text = f"{current_text}\n{message}"
        self.messageBox.setPlainText(new_text)
        self.messageBox.verticalScrollBar().setValue(self.messageBox.verticalScrollBar().maximum())  # Scroll to bottom

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

    def retranslateUi(self):
        self.setWindowTitle(self.settings.translate("Driver Yükleyici - Kurulum"))
        self.title.setText(self.settings.translate("Kurulum Yöneticisi"))
        self.selectAllButton.setText(self.settings.translate("Tümünü Seç"))
        self.deselectAllButton.setText(self.settings.translate("Seçimleri İptal Et"))
        self.installButton.setText(self.settings.translate("Yükle"))

    def onInstallFinished(self):
        QTimer.singleShot(2000, self.showCompleteWindow)  # Wait for 2 seconds before transitioning

    def showCompleteWindow(self):
        self.completeWindow = CompleteWindow(self.settings)
        self.completeWindow.setGeometry(self.geometry())
        self.completeWindow.show()

        # Büyütme animasyonu
        self.animation = QPropertyAnimation(self.completeWindow, b"geometry")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.setStartValue(QRect(self.geometry().x() + self.width() // 2, self.geometry().y() + self.height() // 2, 0, 0))
        self.animation.setEndValue(self.geometry())
        self.animation.start()

        self.hide()


class DriverInstallThread(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)

    def __init__(self, driver_installer, driver_files):
        QThread.__init__(self)
        self.driver_installer = driver_installer
        self.driver_files = driver_files

    def run(self):
        total_files = len(self.driver_files)
        for i, file in enumerate(self.driver_files):
            try:
                self.driver_installer.installDriver(file)
                self.status.emit(f"{os.path.basename(file)} yükleniyor...")
                self.progress.emit(int((i + 1) / total_files * 100))
            except Exception as e:
                self.status.emit(f"Hata: {os.path.basename(file)} yüklenemedi. Hata: {str(e)}")
        self.status.emit("Yükleme tamamlandı!")
        self.progress.emit(100)  # Ensure progress is shown as 100% when done


if __name__ == "__main__":
    from backend.settings import Settings
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    settings = Settings()
    window = InstallWindow(settings)
    window.show()

    sys.exit(app.exec())