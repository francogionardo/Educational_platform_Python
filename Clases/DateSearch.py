# DateSearch.py

import glob
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QMessageBox

def search_by_date(clases_instance):
    """ Search for videos by date and update both the result table and the duplicate section with expanded label information. """
    date_selected = clases_instance.ui.date_select.selectedDate().toString("yyyyMMdd")
    clases_instance.ui.result_table.setRowCount(0)
    video_files = glob.glob("Videos/*.mp4")
    matched_videos = [video for video in video_files if date_selected in video]

    if matched_videos:
        duplicate_content = f"Resultados para la fecha {date_selected}:\n"  # Preparar contenido para la duplicación

        for video in matched_videos:
            # Obtener la información de los labels concatenados para la fecha seleccionada
            label_info = clases_instance.course_data_manager.video_data.get(date_selected, {}).get('labels', "Horario no disponible")

            # Crear fila en la tabla de resultados
            row_position = clases_instance.ui.result_table.rowCount()
            clases_instance.ui.result_table.insertRow(row_position)
            clases_instance.ui.result_table.setItem(row_position, 0, QTableWidgetItem(date_selected))
            clases_instance.ui.result_table.setItem(row_position, 1, QTableWidgetItem(label_info))  # Asignar labels concatenados a "Horario"
            clases_instance.ui.result_table.setItem(row_position, 2, QTableWidgetItem("Tema no especificado"))

            # Botón de reproducción
            play_button = QPushButton("Reproducir")
            play_button.clicked.connect(lambda ch, path=video: clases_instance.play_video_with_potplayer(path))
            clases_instance.ui.result_table.setCellWidget(row_position, 3, play_button)

            # Agregar el contenido a la duplicación
            duplicate_content += f"{label_info}\n"

        # Actualizar la sección duplicada con el contenido generado
        clases_instance.duplicate_section.update_content(duplicate_content)

    else:
        QMessageBox.information(clases_instance, "Resultado", f"No se encontraron videos para la fecha {date_selected}.")
