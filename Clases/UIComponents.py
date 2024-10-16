# UIComponents.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QCalendarWidget, QCheckBox, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt

class UIComponents(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout and Widgets
        self.layout = QVBoxLayout()
        
        # Course Selection Section
        self.course_label = QLabel("Curso:")
        self.course_select = QComboBox()
        self.course_select.addItem("-- Seleccione Curso --")
        self.course_select.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Week Selection
        self.week_label = QLabel("Semana y tema del curso elegido:")
        self.week_select = QComboBox()
        self.week_select.addItem("-- Seleccione Semana --")
        self.week_select.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Search button for course and week
        self.search_course_week_button = QPushButton("Buscar por Curso y Semana")
        self.search_course_week_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Date Selection Section
        self.date_label = QLabel("Seleccione una fecha:")
        self.date_checkbox = QCheckBox("Filtrar por Fecha")
        self.date_select = QCalendarWidget()
        self.date_select.setGridVisible(True)
        self.date_select.setVisible(False)  # Hidden by default
        self.date_select.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Search button for date
        self.search_date_button = QPushButton("Buscar por Fecha")
        self.search_date_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Result Table
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["Fecha", "Horario del Curso", "Tema", "Video"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Arrange Widgets in Layout
        self.layout.addWidget(self.course_label)
        self.layout.addWidget(self.course_select)
        self.layout.addWidget(self.week_label)
        self.layout.addWidget(self.week_select)
        self.layout.addWidget(self.search_course_week_button)
        
        date_layout = QHBoxLayout()
        date_layout.addWidget(self.date_label)
        date_layout.addWidget(self.date_checkbox)
        self.layout.addLayout(date_layout)
        
        self.layout.addWidget(self.date_select)
        self.layout.addWidget(self.search_date_button)
        self.layout.addWidget(self.result_table)
        
        # Add margin and set layout
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)
