from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class TopBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.8);")
        layout = QHBoxLayout()
        self.setLayout(layout)

        # Minimize button
        self.minimize_button = QPushButton("—")
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(self.minimize_button)

        # Settings button (for future use)
        self.settings_button = QPushButton("⚙")
        self.settings_button.setFixedSize(30, 30)
        self.settings_button.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(self.settings_button)

        # Close button
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(self.close_button)

        self.close_button.clicked.connect(parent.close)
