# VideoPlayer.py

import sys
import platform
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint, QRect, QSize  # Agregar QSize aquí
import vlc

from .Topbar import TopBar
from .Downbar import DownBar

class VideoPlayer(QMainWindow):
    def __init__(self, video_path):
        super().__init__()
        self.setWindowTitle('Video Player')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Tamaño de pantalla y ajuste inicial
        screen_geometry = QApplication.desktop().screenGeometry()
        initial_width = screen_geometry.width() // 2
        initial_height = screen_geometry.height() // 2
        self.setGeometry(
            (screen_geometry.width() - initial_width) // 2,
            (screen_geometry.height() - initial_height) // 2,
            initial_width,
            initial_height
        )

        # Variables para el arrastre y redimensionamiento
        self.dragging = False
        self.resizing = False
        self.drag_position = QPoint()
        self.resize_start_position = QPoint()
        self.initial_geometry = QRect()
        self.resize_edge_margin = 10  # Tamaño de área sensible para redimensionar
        self.aspect_ratio = 16 / 9  # Suponiendo una relación de aspecto 16:9, se puede calcular según el video
        
        # Configuración del reproductor
        self.main_widget = QWidget(self)
        self.main_widget.setStyleSheet("background-color: black; border-radius: 10px;")
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)

        # Instancia del reproductor de video
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        media = self.instance.media_new(video_path)
        self.media_player.set_media(media)

        # Barras superior e inferior
        self.top_bar = TopBar(self)
        self.down_bar = DownBar(self)

        layout.addWidget(self.top_bar)
        layout.addStretch(1)  # Espacio para el video
        layout.addWidget(self.down_bar)

        # Configurar la salida de video según el sistema operativo
        if platform.system() == "Windows":
            self.media_player.set_hwnd(int(self.winId()))
        else:
            self.media_player.set_xwindow(self.winId())

        # Conectar botones y eventos
        self.down_bar.play_button.clicked.connect(self.toggle_play_pause)
        self.show()

    def toggle_play_pause(self):
        if self.media_player.is_playing():
            self.media_player.pause()
        else:
            self.media_player.play()

    def closeEvent(self, event):
        self.media_player.stop()

    # Eventos para arrastrar y redimensionar
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.is_in_resize_zone(event.pos()):
                self.resizing = True
                self.resize_start_position = event.globalPos()
                self.initial_geometry = self.geometry()
            else:
                self.dragging = True
                self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
        elif self.resizing:
            delta = event.globalPos() - self.resize_start_position
            new_width = max(self.initial_geometry.width() + delta.x(), 100)
            new_height = int(new_width / self.aspect_ratio)
            new_geometry = QRect(self.initial_geometry.topLeft(), QSize(new_width, new_height))
            self.setGeometry(new_geometry)
            event.accept()
        else:
            self.update_cursor(event.pos())

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.resizing = False

    def is_in_resize_zone(self, pos):
        # Verificar si el cursor está en cualquier esquina o borde para cambiar el tamaño
        return (
            pos.x() >= self.width() - self.resize_edge_margin or
            pos.y() >= self.height() - self.resize_edge_margin or
            pos.x() <= self.resize_edge_margin or
            pos.y() <= self.resize_edge_margin
        )

    def update_cursor(self, pos):
        if self.is_in_resize_zone(pos):
            self.setCursor(Qt.SizeFDiagCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer("path/to/video.mp4")
    player.show()
    sys.exit(app.exec_())
