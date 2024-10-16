# Resizable.py

from PyQt5.QtCore import Qt, QPoint, QRect, QSize
from PyQt5.QtGui import QCursor

class Resizable:
    def __init__(self):
        self.resizing = False
        self.resize_start_position = QPoint()
        self.initial_geometry = None
        self.resize_edge_margin = 8  # Reduced margin for better detection

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_in_resize_zone(event.pos()):
            self.resizing = True
            self.resize_start_position = event.globalPos()
            self.initial_geometry = self.geometry()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.resizing:
            self.perform_resize(event)
        else:
            self.update_cursor(event.pos())

    def mouseReleaseEvent(self, event):
        self.resizing = False
        self.setCursor(Qt.ArrowCursor)  # Reset cursor after resizing

    def is_in_resize_zone(self, pos):
        return (
            pos.x() >= self.width() - self.resize_edge_margin or
            pos.y() >= self.height() - self.resize_edge_margin or
            pos.x() <= self.resize_edge_margin or
            pos.y() <= self.resize_edge_margin
        )

    def update_cursor(self, pos):
        if pos.x() >= self.width() - self.resize_edge_margin:
            if pos.y() >= self.height() - self.resize_edge_margin:
                self.setCursor(Qt.SizeFDiagCursor)  # Bottom-right corner
            elif pos.y() <= self.resize_edge_margin:
                self.setCursor(Qt.SizeBDiagCursor)  # Top-right corner
            else:
                self.setCursor(Qt.SizeHorCursor)  # Right edge
        elif pos.x() <= self.resize_edge_margin:
            if pos.y() >= self.height() - self.resize_edge_margin:
                self.setCursor(Qt.SizeBDiagCursor)  # Bottom-left corner
            elif pos.y() <= self.resize_edge_margin:
                self.setCursor(Qt.SizeFDiagCursor)  # Top-left corner
            else:
                self.setCursor(Qt.SizeHorCursor)  # Left edge
        elif pos.y() >= self.height() - self.resize_edge_margin:
            self.setCursor(Qt.SizeVerCursor)  # Bottom edge
        elif pos.y() <= self.resize_edge_margin:
            self.setCursor(Qt.SizeVerCursor)  # Top edge
        else:
            self.setCursor(Qt.ArrowCursor)  # Default cursor

    def perform_resize(self, event):
        delta = event.globalPos() - self.resize_start_position
        new_width = max(self.initial_geometry.width() + delta.x(), 100)
        new_height = int(new_width / (16 / 9))  # Maintain 16:9 aspect ratio
        self.setGeometry(QRect(self.initial_geometry.topLeft(), QSize(new_width, new_height)))
