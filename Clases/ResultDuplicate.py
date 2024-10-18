# ResultDuplicate.py

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class ResultDuplicate(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        # Crear una etiqueta donde se mostrará el contenido duplicado
        self.label = QLabel("Resultados duplicados aparecerán aquí.")
        self.label.setAlignment(Qt.AlignTop)  # Alinear el texto en la parte superior
        self.label.setWordWrap(True)  # Habilitar el ajuste de texto en varias líneas si es necesario
        
        # Agregar la etiqueta al diseño
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def update_content(self, content):
        """ Actualiza la sección duplicada con nuevo contenido. """
        self.label.setText(content)
