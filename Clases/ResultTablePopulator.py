# ResultTablePopulator.py

import glob
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton

def populate_result_table(clases_instance, date, data):
    """ Populate the result table with search results based on the given date and data. """
    label = data['label']
    week_number = data['week']
    video_files = glob.glob("Videos/*.mp4")
    
    for video in video_files:
        if video.split('_')[0][3:] == date:
            course_times = label.split('\n')
            for ct in course_times:
                course_name = ct.split(":")[0]
                topic_list = clases_instance.course_data_manager.course_data.get(course_name, [])
                topic = topic_list[week_number - 1] if week_number <= len(topic_list) else "Tema no encontrado"
                
                row_position = clases_instance.ui.result_table.rowCount()
                clases_instance.ui.result_table.insertRow(row_position)
                clases_instance.ui.result_table.setItem(row_position, 0, QTableWidgetItem(date))
                clases_instance.ui.result_table.setItem(row_position, 1, QTableWidgetItem(ct))
                clases_instance.ui.result_table.setItem(row_position, 2, QTableWidgetItem(topic))
                
                play_button = QPushButton("Reproducir")
                play_button.clicked.connect(lambda ch, path=video: clases_instance.play_video_with_potplayer(path))
                clases_instance.ui.result_table.setCellWidget(row_position, 3, play_button)
