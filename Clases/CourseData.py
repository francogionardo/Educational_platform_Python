# CourseData.py

import csv
from PyQt5.QtWidgets import QMessageBox

class CourseData:
    def __init__(self):
        self.course_data = {}
        self.video_data = {}

    def load_course_data(self, filepath):
        # Load course data logic remains the same
        pass

    def load_calendar_data(self, filepath):
        """ Load calendar data from CSV file, handling multiple Label columns """
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    date = row['Date']
                    week = row['Week']
                    # Extract and clean each label
                    labels = [
                        row.get('Label_1', '').strip(),
                        row.get('Label_2', '').strip(),
                        row.get('Label_3', '').strip(),
                        row.get('Label_4', '').strip()
                    ]
                    # Remove any empty strings from the list
                    non_empty_labels = [label for label in labels if label]
                    
                    # Format the label information to include the week and each course label
                    if non_empty_labels:
                        formatted_labels = f"Semana {week}:\n" + "\n".join(non_empty_labels)
                    else:
                        formatted_labels = f"Semana {week}: No hay cursos registrados"
                    
                    # Store the concatenated labels
                    self.video_data[date] = {'labels': formatted_labels, 'week': int(week)}
        except FileNotFoundError:
            QMessageBox.critical(None, "Error", f"No se pudo encontrar el archivo: {filepath}")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al leer el archivo: {e}")
