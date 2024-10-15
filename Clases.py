# Clases.py

import csv
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QCalendarWidget, QCheckBox, QHBoxLayout
from PyQt5.QtCore import QDate
import os
import glob
from VideoPlayer.VideoPlayer import VideoPlayer


class Clases(QWidget):
    def __init__(self):
        super().__init__()

        # Main Layout
        layout = QVBoxLayout()

        # Course Selection Section
        course_label = QLabel("Curso:")
        self.course_select = QComboBox()
        self.course_select.addItem("-- Seleccione Curso --")

        # Initialize course_data and populate courses
        self.course_data = {}
        self.video_data = {}
        self.load_course_data("course_content.txt")
        self.load_calendar_data("Sources/Calendario.csv")  # Ruta corregida
        self.populate_courses()
        
        # Connect to populate weeks when course changes
        self.course_select.currentIndexChanged.connect(self.populate_weeks)

        # Week Selection
        week_label = QLabel("Semana y tema del curso elegido:")
        self.week_select = QComboBox()
        self.week_select.addItem("-- Seleccione Semana --")

        # Search button for course and week
        search_course_week_button = QPushButton("Buscar por Curso y Semana")
        search_course_week_button.clicked.connect(self.search_by_course_and_week)

        # Date Selection Section
        date_label = QLabel("Seleccione una fecha:")
        self.date_checkbox = QCheckBox("Filtrar por Fecha")
        self.date_select = QCalendarWidget()
        self.date_select.setGridVisible(True)
        self.date_select.setVisible(False)  # Hidden by default
        self.date_checkbox.stateChanged.connect(self.toggle_calendar)

        # Search button for date
        search_date_button = QPushButton("Buscar por Fecha")
        search_date_button.clicked.connect(self.search_by_date)

        # Result Table
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["Fecha", "Horario del Curso", "Tema", "Video"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Adding Widgets to Layout
        layout.addWidget(course_label)
        layout.addWidget(self.course_select)
        layout.addWidget(week_label)
        layout.addWidget(self.week_select)
        layout.addWidget(search_course_week_button)

        date_layout = QHBoxLayout()
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_checkbox)
        layout.addLayout(date_layout)
        layout.addWidget(self.date_select)
        layout.addWidget(search_date_button)
        layout.addWidget(self.result_table)

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
                        if current_course in self.course_data:
                            self.course_data[current_course].append(line)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"No se pudo encontrar el archivo: {filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al leer el archivo: {e}")

    def load_calendar_data(self, filepath):
        """ Load calendar data from CSV file for video labeling """
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    date = row['Date']
                    label = row['Label']
                    week = row['Week']
                    self.video_data[date] = {'label': label, 'week': int(week)}
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
        self.week_select.clear()
        self.week_select.addItem("-- Seleccione Semana --")  # Add default item
        weeks = self.course_data.get(course, [])
        for week in weeks:
            self.week_select.addItem(week)

    def toggle_calendar(self, state):
        """ Show or hide the calendar based on checkbox state """
        self.date_select.setVisible(state == 2)  # 2 means Checked

    def search_by_course_and_week(self):
        """ Search by course and week number """
        course = self.course_select.currentText()
        week = self.week_select.currentText()
        if course == "-- Seleccione Curso --" and week == "-- Seleccione Semana --":
            QMessageBox.warning(self, "Error", "Seleccione un curso y/o una semana.")
            return

        self.result_table.setRowCount(0)
        for date, data in self.video_data.items():
            if data['week'] == int(week.split()[1]) and course in data['label']:
                self.populate_result_table(date, data)

    def search_by_date(self):
        """ Search for videos by date """
        date_selected = self.date_select.selectedDate().toString("yyyyMMdd")
        self.result_table.setRowCount(0)

        # Obtener la lista de videos que contengan la fecha seleccionada en su nombre
        video_files = glob.glob("Videos/*.mp4")
        matched_videos = [video for video in video_files if date_selected in video]

        if matched_videos:
            # Para cada video coincidente, mostrar los resultados en la tabla
            for video in matched_videos:
                video_name = os.path.basename(video)
                
                # Crear una fila para el video encontrado
                row_position = self.result_table.rowCount()
                self.result_table.insertRow(row_position)
                self.result_table.setItem(row_position, 0, QTableWidgetItem(date_selected))
                
                # Aquí estamos colocando datos genéricos en las columnas restantes, podrías personalizarlos.
                # Ejemplo para un curso y horario de prueba
                self.result_table.setItem(row_position, 1, QTableWidgetItem("Información no especificada"))
                self.result_table.setItem(row_position, 2, QTableWidgetItem("Tema no especificado"))

                # Botón de reproducción
                play_button = QPushButton("Reproducir")
                play_button.clicked.connect(lambda ch, path=video: self.play_video(path))
                self.result_table.setCellWidget(row_position, 3, play_button)
        else:
            QMessageBox.information(self, "Resultado", f"No se encontraron videos para la fecha {date_selected}.")


    def populate_result_table(self, date, data):
        """ Populate result table with search results """
        label = data['label']
        week_number = data['week']

        video_files = glob.glob("Videos/*.mp4")
        for video in video_files:
            video_name = os.path.basename(video)
            video_date = video_name.split('_')[0][3:]

            if video_date == date:
                course_times = label.split('\n')
                for ct in course_times:
                    course_name = ct.split(":")[0]
                    topic_list = self.course_data.get(course_name, [])
                    topic = topic_list[week_number - 1] if week_number <= len(topic_list) else "Tema no encontrado"

                    row_position = self.result_table.rowCount()
                    self.result_table.insertRow(row_position)
                    self.result_table.setItem(row_position, 0, QTableWidgetItem(date))
                    self.result_table.setItem(row_position, 1, QTableWidgetItem(ct))
                    self.result_table.setItem(row_position, 2, QTableWidgetItem(topic))

                    play_button = QPushButton("Reproducir")
                    play_button.clicked.connect(lambda ch, path=video: self.play_video(path))
                    self.result_table.setCellWidget(row_position, 3, play_button)

    def play_video(self, video_path):
        """Inicia la reproducción del video en una ventana emergente"""
        self.player = VideoPlayer(video_path)  # Crea una instancia de VideoPlayer con el video
        self.player.show()  # Muestra la ventana del reproductor

