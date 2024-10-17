# DateSearch.py

import glob
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QMessageBox

def search_by_date(clases_instance):
    """ Search for videos by date and update the result table with expanded label information. """
    date_selected = clases_instance.ui.date_select.selectedDate().toString("yyyyMMdd")
    clases_instance.ui.result_table.setRowCount(0)
    video_files = glob.glob("Videos/*.mp4")
    matched_videos = [video for video in video_files if date_selected in video]

    if matched_videos:
        for video in matched_videos:
            # Retrieve the concatenated labels for this date
            label_info = clases_instance.course_data_manager.video_data.get(date_selected, {}).get('labels', "Horario no disponible")

            row_position = clases_instance.ui.result_table.rowCount()
            clases_instance.ui.result_table.insertRow(row_position)
            clases_instance.ui.result_table.setItem(row_position, 0, QTableWidgetItem(date_selected))
            clases_instance.ui.result_table.setItem(row_position, 1, QTableWidgetItem(label_info))  # Assign concatenated labels to "Horario"
            clases_instance.ui.result_table.setItem(row_position, 2, QTableWidgetItem("Tema no especificado"))

            # Add play button
            play_button = QPushButton("Reproducir")
            play_button.clicked.connect(lambda ch, path=video: clases_instance.play_video_with_potplayer(path))
            clases_instance.ui.result_table.setCellWidget(row_position, 3, play_button)
    else:
        QMessageBox.information(clases_instance, "Resultado", f"No se encontraron videos para la fecha {date_selected}.")
