# CourseData.py
import csv
from PyQt5.QtWidgets import QMessageBox

class CourseData:
    def __init__(self):
        self.course_data = {}
        self.video_data = {}

    def load_course_data(self, filepath):
        # Load course data logic
        pass

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
            QMessageBox.critical(None, "Error", f"No se pudo encontrar el archivo: {filepath}")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al leer el archivo: {e}")
