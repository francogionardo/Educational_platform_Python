# Clases.py

import subprocess
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMessageBox
from .UIComponents import UIComponents
from .CourseData import CourseData
from .DateSearch import search_by_date
from .ResultTablePopulator import populate_result_table
from .ResultDuplicate import ResultDuplicate  # Nueva importación para la sección de duplicación
import os

class Clases(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize Course Data, UI Components, and Duplicate Results Section
        self.course_data_manager = CourseData()
        self.ui = UIComponents(self)
        self.duplicate_section = ResultDuplicate(self)  # Sección nueva para la duplicación de resultados

        # Load Data
        self.course_data_manager.load_course_data("course_content.txt")
        self.course_data_manager.load_calendar_data("Sources/Calendario.csv")
        self.populate_courses()

        # Main Layout: Contiene tanto los filtros como los resultados y la sección de duplicación
        main_layout = QVBoxLayout()  # Cambiado a QVBoxLayout para que todo se organice de arriba hacia abajo
        
        # Filtros de búsqueda y selección (sección superior)
        filter_layout = QVBoxLayout()  # Layout para la parte superior con filtros
        
        # Agregar los componentes de la interfaz de filtros (esto ya está en UIComponents)
        filter_layout.addWidget(self.ui.course_select)
        filter_layout.addWidget(self.ui.week_select)
        filter_layout.addWidget(self.ui.search_course_week_button)
        filter_layout.addWidget(self.ui.date_checkbox)
        filter_layout.addWidget(self.ui.date_select)
        filter_layout.addWidget(self.ui.search_date_button)
        
        # Resultado de búsqueda y duplicación (sección inferior)
        result_layout = QVBoxLayout()  # Layout para la parte inferior con la tabla de resultados y duplicación
        result_layout.addWidget(self.ui.result_table)
        result_layout.addWidget(self.duplicate_section)  # Sección duplicada debajo de la tabla de resultados
        
        # Agregar ambos layouts (filtros y resultados) al layout principal
        main_layout.addLayout(filter_layout)  # Filtros en la parte superior
        main_layout.addLayout(result_layout)  # Resultados y duplicación en la parte inferior
        
        self.setLayout(main_layout)

        # Connect Signals: Aquí conectamos los eventos a los componentes de UI
        self.ui.course_select.currentIndexChanged.connect(self.populate_weeks)
        self.ui.search_course_week_button.clicked.connect(self.search_by_course_and_week)
        self.ui.date_checkbox.stateChanged.connect(self.toggle_calendar)
        self.ui.search_date_button.clicked.connect(lambda: search_by_date(self))

    def populate_courses(self):
        """ Populate the course combo box with available courses. """
        for course in self.course_data_manager.course_data.keys():
            self.ui.course_select.addItem(course)

    def populate_weeks(self):
        """ Populate the week combo box based on the selected course. """
        course = self.ui.course_select.currentText()
        self.ui.week_select.clear()
        self.ui.week_select.addItem("-- Seleccione Semana --")
        weeks = self.course_data_manager.course_data.get(course, [])
        for week in weeks:
            self.ui.week_select.addItem(week)

    def toggle_calendar(self, state):
        """ Show or hide the calendar based on checkbox state """
        self.ui.date_select.setVisible(state == 2)

    def search_by_course_and_week(self):
        course = self.ui.course_select.currentText()
        week = self.ui.week_select.currentText()
        if course == "-- Seleccione Curso --" and week == "-- Seleccione Semana --":
            QMessageBox.warning(self, "Error", "Seleccione un curso y/o una semana.")
            return

        self.ui.result_table.setRowCount(0)
        for date, data in self.course_data_manager.video_data.items():
            if data['week'] == int(week.split()[1]) and course in data['label']:
                populate_result_table(self, date, data)  # Usar populate_result_table function

    def play_video_with_potplayer(self, video_path):
        potplayer_path = r"E:\Programs\PotPlayer\PotPlayerMini64.exe"
        try:
            subprocess.Popen([potplayer_path, video_path])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al abrir el video con PotPlayer: {e}")
