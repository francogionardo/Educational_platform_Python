from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSlider, QLabel
from PyQt5.QtCore import Qt

class DownBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.8);")
        layout = QHBoxLayout()
        self.setLayout(layout)

        # Play/Pause button
        self.play_button = QPushButton("▶")
        self.play_button.setFixedSize(30, 30)
        self.play_button.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(self.play_button)

        # Rewind 5 seconds button
        self.rewind_button = QPushButton("⏪")
        self.rewind_button.setFixedSize(30, 30)
        self.rewind_button.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(self.rewind_button)

        # Forward 5 seconds button
        self.forward_button = QPushButton("⏩")
        self.forward_button.setFixedSize(30, 30)
        self.forward_button.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(self.forward_button)

        # Volume control slider
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setStyleSheet("QSlider::handle { background: white; }")
        layout.addWidget(self.volume_slider)

        # Time label
        self.time_label = QLabel("0:00 / 0:00")
        self.time_label.setStyleSheet("color: white;")
        layout.addWidget(self.time_label)
