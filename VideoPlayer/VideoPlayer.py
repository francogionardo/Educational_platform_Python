import sys
import platform
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
import vlc

from VideoPlayer.topbar import TopBar
from VideoPlayer.downbar import DownBar


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

        # Set up the correct video output for Windows
        if platform.system() == "Windows":
            self.media_player.set_hwnd(int(self.winId()))
        else:
            self.media_player.set_xwindow(self.winId())

        # Connect the play/pause button to toggle play/pause
        self.down_bar.play_button.clicked.connect(self.toggle_play_pause)

        # Timer for mouse movement detection to hide/show bars
        self.timer = QTimer()
        self.timer.setInterval(2000)  # 2 seconds
        self.timer.timeout.connect(self.hide_controls)
        self.setMouseTracking(True)

        # Show controls when the mouse enters the window
        self.main_widget.setMouseTracking(True)
        self.main_widget.installEventFilter(self)

        # Window resize and move functionalities
        self.setMinimumSize(200, 150)
        self.setMouseTracking(True)

    def eventFilter(self, obj, event):
        if event.type() == event.Enter:
            self.show_controls()
        elif event.type() == event.Leave:
            self.hide_controls()
        return super().eventFilter(obj, event)

    def toggle_play_pause(self):
        if self.media_player.is_playing():
            self.media_player.pause()
        else:
            self.media_player.play()

    # En la función show_controls:
    def show_controls(self):
        self.top_bar.show()
        self.down_bar.show()
        self.timer.start()

    # En la función hide_controls:
    def hide_controls(self):
        self.top_bar.hide()
        self.down_bar.hide()
        self.timer.stop()

    def closeEvent(self, event):
        self.media_player.stop()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.RightButton:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    video_path = "Videos/GMT20240823-122814_Recording_1920x1080.mp4"  # Cambia esto por el video que desees probar
    player = VideoPlayer(video_path)
    player.show()
    sys.exit(app.exec_())
