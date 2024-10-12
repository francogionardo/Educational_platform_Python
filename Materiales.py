# Materiales.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class Materiales(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        material_label = QLabel("Mis Materiales Académicos:")
        subjects = ["Álgebra", "Aritmética", "Geometría", "Trigonometría", "Razonamiento Matemático"]
        
        layout.addWidget(material_label)
        for subject in subjects:
            layout.addWidget(QLabel(subject))
        
        self.setLayout(layout)
