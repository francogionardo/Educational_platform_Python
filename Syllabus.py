# Syllabus.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox

class Syllabus(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        ciclo_label = QLabel("Ciclo:")
        ciclo_select = QComboBox()
        ciclo_select.addItem("INTENSIVO UNI - MAÑANA")
        
        course_label = QLabel("Curso:")
        course_select = QComboBox()
        course_select.addItem("Álgebra")
        
        syllabus_content = QLabel("Semana 1: Números Complejos\nSemana 2: Ecuaciones Polinomiales")
        
        layout.addWidget(ciclo_label)
        layout.addWidget(ciclo_select)
        layout.addWidget(course_label)
        layout.addWidget(course_select)
        layout.addWidget(syllabus_content)
        
        self.setLayout(layout)
