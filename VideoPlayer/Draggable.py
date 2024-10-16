# Draggable.py

from PyQt5.QtCore import Qt, QPoint

class Draggable:
    def __init__(self):
        self.dragging = False
        self.drag_position = QPoint()
        self.resizing = False  # Flag to indicate resizing status

    def mousePressEvent(self, event):
        # Only start dragging if not resizing
        if event.button() == Qt.LeftButton and not self.resizing:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        # Move window only if dragging and not resizing
        if self.dragging and not self.resizing:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False
