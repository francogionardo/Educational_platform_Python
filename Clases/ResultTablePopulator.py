# ResultTablePopulator.py

import glob
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont

def populate_result_table(clases_instance, date, data):
    """ Populate the result table with search results and update the duplicate section """
    label = data['label']
    week_number = data['week']
    video_files = glob.glob("Videos/*.mp4")
    
    # Prepare the content to duplicate (Horario del Curso)
    duplicate_content = f"Semana {week_number}:\n"  # Preparar el contenido duplicado
    
    for video in video_files:
        if video.split('_')[0][3:] == date:
            course_times = label.split('\n')
            
            # Create a new widget to hold the week and label information with styles
            result_widget = QWidget()
            result_layout = QVBoxLayout()

            # Create a styled QLabel for "Semana X"
            week_label = QLabel(f"Semana {week_number}")
            week_label.setFont(QFont("Arial", 16, QFont.Bold))  # Title 1 style
            week_label.setStyleSheet("color: black;")
            result_layout.addWidget(week_label)

            # Add each course label with a smaller font (Title 2 style)
            for ct in course_times:
                label_item = QLabel(ct)
                label_item.setFont(QFont("Arial", 14))  # Title 2 style
                label_item.setStyleSheet("color: gray;")
                result_layout.addWidget(label_item)
                
                # Add the course time to the duplicate content
                duplicate_content += f"{ct}\n"

            result_widget.setLayout(result_layout)

            # Insert the formatted widget into the result table
            row_position = clases_instance.ui.result_table.rowCount()
            clases_instance.ui.result_table.insertRow(row_position)
            clases_instance.ui.result_table.setCellWidget(row_position, 1, result_widget)  # Add the widget to the "Horario del Curso" column

            # Add other standard columns (date and video)
            clases_instance.ui.result_table.setItem(row_position, 0, QTableWidgetItem(date))
            clases_instance.ui.result_table.setItem(row_position, 2, QTableWidgetItem("Tema no especificado"))

            # Add play button
            play_button = QPushButton("Reproducir")
            play_button.clicked.connect(lambda ch, path=video: clases_instance.play_video_with_potplayer(path))
            clases_instance.ui.result_table.setCellWidget(row_position, 3, play_button)
    
    # Update the duplicated section with the new content
    clases_instance.duplicate_section.update_content(duplicate_content)
