# Clases.py

import subprocess
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QMessageBox
from .UIComponents import UIComponents
from .CourseData import CourseData
from .DateSearch import search_by_date
from .ResultTablePopulator import populate_result_table
import os

class Clases(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize Course Data and UI Components
        self.course_data_manager = CourseData()
        self.ui = UIComponents(self)
        
        # Load Data
        self.course_data_manager.load_course_data("course_content.txt")
        self.course_data_manager.load_calendar_data("Sources/Calendario.csv")
        self.populate_courses()
        
        # Main Layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.ui)  # Make UIComponents fill the available space
        self.setLayout(main_layout)

        # Connect Signals
        self.ui.course_select.currentIndexChanged.connect(self.populate_weeks)
        self.ui.search_course_week_button.clicked.connect(self.search_by_course_and_week)
        self.ui.date_checkbox.stateChanged.connect(self.toggle_calendar)
        self.ui.search_date_button.clicked.connect(lambda: search_by_date(self))  # Use search_by_date function

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
                populate_result_table(self, date, data)  # Use populate_result_table function

    def play_video_with_potplayer(self, video_path):
        potplayer_path = r"E:\Programs\PotPlayer\PotPlayerMini64.exe"
        try:
            subprocess.Popen([potplayer_path, video_path])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al abrir el video con PotPlayer: {e}")
