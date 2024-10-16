# CourseData.py
import csv
from PyQt5.QtWidgets import QMessageBox

class CourseData:
    def __init__(self):
        self.course_data = {}
        self.video_data = {}

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
            QMessageBox.critical(None, "Error", f"No se pudo encontrar el archivo: {filepath}")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al leer el archivo: {e}")

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
