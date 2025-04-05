import os
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QTreeWidget, QTreeWidgetItem, QPushButton, \
    QHBoxLayout, QScrollArea, QProgressBar
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
from backend.settings import Settings
from backend.driver_installer import DriverInstaller


class InstallWindow(QMainWindow):
    def __init__(self, settings, parent=None):
        super(InstallWindow, self).__init__(parent)

        self.settings = settings
        self.driver_installer = DriverInstaller("drivers")  # DriverInstaller instance

        self.setWindowTitle(self.settings.translate("Driver Yükleyici - Kurulum"))
        self.setGeometry(100, 100, 600, 400)

        self.initUI()
        self.scanDrivers()

    def initUI(self):
        # Main Container
        container = QWidget()
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)

        # Title Layout
        titleLayout = QHBoxLayout()
        self.title = QLabel(self.settings.translate("Driver Yükleyici - Kurulum"), self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #1E3A5F;
            margin-bottom: 20px;
        """)

        # Logo
        logo = QLabel(self)
        pixmap = QPixmap("resources/themes/logo.png")
        logo.setPixmap(pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio))
        titleLayout.addWidget(logo)
        titleLayout.addWidget(self.title)
        titleLayout.addStretch()
        layout.addLayout(titleLayout)

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
        layout.addWidget(scrollArea)

        # Select All Button
        self.selectAllButton = QPushButton(self.settings.translate("Hepsini Seç"), self)
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

        # Progress Bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)

        # Bottom Button Layout
        bottomButtonLayout = QHBoxLayout()
        bottomButtonLayout.addWidget(self.selectAllButton)
        bottomButtonLayout.addWidget(self.deselectAllButton)

        layout.addLayout(bottomButtonLayout)
        layout.addWidget(self.installButton, alignment=Qt.AlignmentFlag.AlignCenter)

        self.applyTheme(self.settings.current_theme)

    def applyTheme(self, theme):
        self.setStyleSheet(self.settings.get_theme())

    def scanDrivers(self):
        categorized_drivers = self.driver_installer.scan_and_categorize_drivers()
        self.displayDrivers(categorized_drivers)

    def displayDrivers(self, categorized_drivers):
        self.driverList.clear()
        for category, files in categorized_drivers.items():
            category_item = QTreeWidgetItem([category])
            category_item.setFlags(category_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            category_item.setCheckState(0, Qt.CheckState.Unchecked)
            self.driverList.addTopLevelItem(category_item)
            category_item.setExpanded(False)  # Kategoriler varsayılan olarak kapalı

            for file in files:
                file_item = QTreeWidgetItem(category_item)
                file_item.setFlags(file_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                file_item.setCheckState(0, Qt.CheckState.Unchecked)

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

    def deselectAllDrivers(self):
        self.driverList.blockSignals(True)
        for index in range(self.driverList.topLevelItemCount()):
            category_item = self.driverList.topLevelItem(index)
            category_item.setCheckState(0, Qt.CheckState.Unchecked)
            for child_index in range(category_item.childCount()):
                item = category_item.child(child_index)
                item.setCheckState(0, Qt.CheckState.Unchecked)
        self.driverList.blockSignals(False)

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
        self.thread.start()

    def updateProgressBar(self, value):
        self.progressBar.setValue(value)


class DriverInstallThread(QThread):
    progress = pyqtSignal(int)

    def __init__(self, driver_installer, driver_files):
        QThread.__init__(self)
        self.driver_installer = driver_installer
        self.driver_files = driver_files

    def run(self):
        total_files = len(self.driver_files)
        for i, file in enumerate(self.driver_files):
            self.driver_installer.installDriver(file)
            self.progress.emit(int((i + 1) / total_files * 100))


if __name__ == "__main__":
    from backend.settings import Settings
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    settings = Settings()
    window = InstallWindow(settings)
    window.show()

    sys.exit(app.exec())