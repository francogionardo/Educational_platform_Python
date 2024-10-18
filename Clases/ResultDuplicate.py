import csv
import unidecode  # Para eliminar tildes de los nombres
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt

class ResultDuplicate(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        # Crear una etiqueta donde se mostrará el contenido duplicado
        self.label = QLabel("Resultados duplicados aparecerán aquí.")
        self.label.setAlignment(Qt.AlignTop)
        self.label.setWordWrap(True)

        # Lista para mostrar los "Paths" de Temario.csv
        self.path_list = QListWidget()

        # Agregar widgets al diseño
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.path_list)  # Añadimos la lista debajo de la etiqueta
        self.setLayout(self.layout)

    def update_content(self, content):
        """ Actualiza la sección duplicada con nuevo contenido y busca en Temario.csv. """
        self.label.setText(content)

        # Extraer la semana y los cursos del contenido
        cursos = self.extract_courses_from_content(content)
        week = self.extract_week_from_content(content)

        # Imprimir los cursos y la semana extraídos para depuración
        print(f"Cursos extraídos: {cursos}")
        print(f"Semana extraída: {week}")

        if cursos and week:
            self.search_in_temario(cursos, week)

    def extract_courses_from_content(self, content):
        """ Extrae los nombres de los cursos del contenido duplicado. """
        lines = content.splitlines()
        cursos = []
        
        # Recorremos las líneas para encontrar las que tengan un horario (y por lo tanto un curso)
        for line in lines:
            if ' De ' in line:  # Esta línea contiene un curso seguido de un horario
                curso = line.split(':')[0].strip()  # Extraemos el curso antes de los ":"
                cursos.append(curso)
        
        return cursos

    def extract_week_from_content(self, content):
        """ Extrae la semana del contenido duplicado. """
        # Buscar la línea que contiene "Semana X:"
        lines = content.splitlines()
        for line in lines:
            if 'Semana' in line:
                # Separa por espacios y elimina cualquier carácter no numérico como los ":".
                week_str = line.split()[1].rstrip(':')
                return int(week_str)  # Extrae el número de la semana correctamente
        return None

    def search_in_temario(self, cursos, week):
        """ Busca los cursos y la semana en Temario.csv y actualiza la lista de Path. """
        self.path_list.clear()  # Limpiar la lista antes de actualizarla
        found_paths = []

        # Leer el archivo Temario.csv
        with open("Sources/Temario.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            # Iterar sobre los cursos extraídos y buscar en el CSV
            for curso in cursos:
                curso_normalizado = unidecode.unidecode(curso)  # Normalizamos el nombre del curso quitando tildes

                print(f"Buscando curso: {curso_normalizado}, Semana: {week}")  # Para depuración

                for row in reader:
                    curso_csv = unidecode.unidecode(row["Curso"])
                    if curso_csv == curso_normalizado and int(row["Week"]) == week:
                        found_paths.append(row["Path"])

        # Mostrar los resultados en la lista de Path
        if found_paths:
            for path in found_paths:
                item = QListWidgetItem(path)
                self.path_list.addItem(item)
        else:
            self.path_list.addItem("No se encontraron resultados en Temario.csv.")
