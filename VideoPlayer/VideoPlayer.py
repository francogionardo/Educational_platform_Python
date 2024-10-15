import sys
import platform
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt
import vlc

from .topbar import TopBar
from .downbar import DownBar


class VideoPlayer(QMainWindow):
    def __init__(self, video_path):
        super().__init__()
        self.setWindowTitle('Video Player')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Main widget and layout
        self.main_widget = QWidget(self)
        self.main_widget.setStyleSheet("background-color: black; border-radius: 10px;")
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)

        # Video player instance
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        media = self.instance.media_new(video_path)
        self.media_player.set_media(media)

        # Top and bottom bars
        self.top_bar = TopBar(self)
        self.down_bar = DownBar(self)

        layout.addWidget(self.top_bar)
        layout.addStretch(1)  # Space for video display
        layout.addWidget(self.down_bar)

        # Playback speed control button
        self.speed_button = QPushButton("1.0x", self)
        self.speed_button.setStyleSheet("background-color: rgba(255, 255, 255, 0.5); color: black;")
        self.speed_button.clicked.connect(self.change_speed)
        layout.addWidget(self.speed_button)

        # Opacity slider
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(50, 100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")
        self.opacity_slider.valueChanged.connect(self.adjust_opacity)
        layout.addWidget(self.opacity_slider)

        # Adjust the size of the player
        self.setFixedSize(900, 500)

        # Set up the correct video output for Windows
        if platform.system() == "Windows":
            self.media_player.set_hwnd(int(self.winId()))
        else:
            self.media_player.set_xwindow(self.winId())

        # Connect the play/pause button to toggle play/pause
        self.down_bar.play_button.clicked.connect(self.toggle_play_pause)

        # Play video automatically on open
        self.media_player.play()

    def toggle_play_pause(self):
        if self.media_player.is_playing():
            self.media_player.pause()
        else:
            self.media_player.play()

    def change_speed(self):
        """Cycle through playback speeds."""
        current_speed = self.media_player.get_rate()
        new_speed = 1.0  # Default speed
        if current_speed == 1.0:
            new_speed = 1.5
        elif current_speed == 1.5:
            new_speed = 2.0
        elif current_speed == 2.0:
            new_speed = 0.5
        elif current_speed == 0.5:
            new_speed = 1.0

        self.media_player.set_rate(new_speed)
        self.speed_button.setText(f"{new_speed}x")

    def adjust_opacity(self):
        """Adjust video opacity based on slider."""
        opacity = self.opacity_slider.value() / 100
        self.setWindowOpacity(opacity)

    def closeEvent(self, event):
        self.media_player.stop()

# Esta parte se elimina ya que se usa desde Clases.py
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     player = VideoPlayer("../Videos/GMT20240823-122814_Recording_1920x1080.mp4")
#     player.show()
#     sys.exit(app.exec_())
