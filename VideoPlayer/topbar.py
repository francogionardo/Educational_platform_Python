from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QStyle
from PyQt5.QtCore import Qt


class TopBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Minimize Button (sin funcionalidad)
        self.minimize_button = QPushButton()
        self.minimize_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMinButton))
        self.minimize_button.setStyleSheet("background-color: transparent;")
        layout.addWidget(self.minimize_button)

        # Spacer
        layout.addStretch()

        # Settings Button (sin funcionalidad)
        self.settings_button = QPushButton()
        self.settings_button.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.settings_button.setStyleSheet("background-color: transparent;")
        layout.addWidget(self.settings_button)

        # Close Button (funcionalidad de cerrar)
        self.close_button = QPushButton()
        self.close_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarCloseButton))
        self.close_button.setStyleSheet("background-color: transparent;")
        layout.addWidget(self.close_button)

        # Conectar el botón de cerrar a la función close del parent
        self.close_button.clicked.connect(self.close_window)

    def close_window(self):
        self.parent().close()
