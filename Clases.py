# Clases.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
import os

class Clases(QWidget):
    def __init__(self):
        super().__init__()

        # Layout for the widget
        layout = QVBoxLayout()

        # Course Selection
        course_label = QLabel("Curso:")
        self.course_select = QComboBox()
        self.course_select.addItem("-- Seleccione Curso --")
        
        # Initialize course_data and populate courses
        self.course_data = {}
        self.load_course_data("course_content.txt")
        self.populate_courses()
        
        # Connect to populate weeks when course changes
        self.course_select.currentIndexChanged.connect(self.populate_weeks)

        # Week Selection (this will update dynamically)
        week_label = QLabel("Semana y tema del curso elegido:")
        self.week_select = QComboBox()

        # Search button
        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.search_course_content)

        # Adding widgets to layout
        layout.addWidget(course_label)
        layout.addWidget(self.course_select)
        layout.addWidget(week_label)
        layout.addWidget(self.week_select)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def load_course_data(self, filepath):
        """ Load course data from an external text file, excluding 'Inglés' and 'Psicología'. """
        current_course = None

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith("# Course:"):
                        current_course = line.split(":", 1)[1].strip()
                        if current_course not in ["Inglés", "Psicología"]:
                            self.course_data[current_course] = []
                    elif current_course and line.startswith("SEMANA"):
                        # Add week content only if the course is valid and not 'Inglés' or 'Psicología'
                        if current_course in self.course_data:
                            self.course_data[current_course].append(line)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"No se pudo encontrar el archivo: {filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al leer el archivo: {e}")

    def populate_courses(self):
        """ Populate the course combo box with available courses from the data file. """
        for course in self.course_data.keys():
            self.course_select.addItem(course)

    def populate_weeks(self):
        """ Populate the week combo box based on the selected course. """
        course = self.course_select.currentText()

        # Clear existing weeks
        self.week_select.clear()

        # Add weeks depending on the course
        weeks = self.course_data.get(course, [])
        for week in weeks:
            self.week_select.addItem(week)

    def search_course_content(self):
        """ Action to search for the course content """
        course = self.course_select.currentText()
        week = self.week_select.currentText()

        if course == "-- Seleccione Curso --" or not week:
            QMessageBox.warning(self, "Error", "Seleccione un curso y una semana válida.")
            return

        # Simulate the search functionality (you can implement file searching here)
        QMessageBox.information(self, "Buscar", f"Buscando contenido para {course}, {week}.")

        # Here you can implement actual file searching logic in a local folder
        # For example:
        # course_folder = f"./content/{course}"
        # week_file = f"week_{week_number}.txt"
        # Check if file exists, etc.
