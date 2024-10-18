import csv
import os  # Para acceder a los archivos en los directorios
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
        # Eliminar contenido duplicado antes de mostrarlo
        filtered_content = self.remove_duplicate_content(content)
        self.label.setText(filtered_content)

        # Extraer la semana y los cursos del contenido filtrado
        cursos = self.extract_courses_from_content(filtered_content)
        week = self.extract_week_from_content(filtered_content)

        # Imprimir los cursos y la semana extraídos para depuración
        print(f"Cursos extraídos: {cursos}")
        print(f"Semana extraída: {week}")

        if cursos and week:
            self.search_in_temario(cursos, week)

    def remove_duplicate_content(self, content):
        """ Elimina cursos y semanas duplicados del contenido. """
        lines = content.splitlines()
        seen_courses = set()
        filtered_lines = []

        for line in lines:
            if 'Semana' in line or ('De' in line and ':' in line):
                # Identificar el curso en la línea que contiene el horario
                course = line.split(':')[0].strip()
                if course not in seen_courses:
                    seen_courses.add(course)
                    filtered_lines.append(line)  # Añadir curso único
            else:
                filtered_lines.append(line)  # Añadir otras líneas que no son duplicadas

        return '\n'.join(filtered_lines)

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
                # Separa por espacios y elimina cualquier carácter no numérico como los ":"
                week_str = line.split()[1].rstrip(':')
                return int(week_str)  # Extrae el número de la semana correctamente
        return None

    def search_in_temario(self, cursos, week):
        """ Busca cada curso y semana en Temario.csv y actualiza la lista de Path y contenido. """
        self.path_list.clear()  # Limpiar la lista antes de actualizarla
        found_paths = []  # Variable para almacenar los paths encontrados

        # Normalizamos los nombres de los cursos quitando tildes para la búsqueda
        cursos_normalizados = [unidecode.unidecode(curso) for curso in cursos]

        # Leer el archivo Temario.csv
        with open("Sources/Temario.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for curso in cursos:
                curso_encontrado = False  # Flag para verificar si encontramos el curso
                curso_normalizado = unidecode.unidecode(curso)
                for row in reader:
                    curso_csv = unidecode.unidecode(row["Curso"])
                    if curso_csv == curso_normalizado and int(row["Week"]) == week:
                        # Agregamos el curso con su path formateado
                        found_paths.append(f"Curso: {curso}:\n        Path: {row['Path']}")
                        
                        # Ahora mostramos el contenido del directorio asociado al path
                        folder_path = row['Path']
                        folder_contents = self.get_folder_contents(folder_path)
                        
                        # Agregamos los archivos dentro de la carpeta
                        if folder_contents:
                            for item in folder_contents:
                                found_paths.append(f"            {item}")
                        else:
                            found_paths.append("            (La carpeta está vacía o no se pudo acceder)")
                        
                        curso_encontrado = True
                        break  # Una vez encontrado, salimos del ciclo interno

                # Si no se encontró el curso, lo indicamos en la lista
                if not curso_encontrado:
                    found_paths.append(f"Curso: {curso} - Path: No encontrado")

        # Mostrar los resultados en la lista de Path
        if found_paths:
            for path in found_paths:
                item = QListWidgetItem(path)
                self.path_list.addItem(item)
        else:
            self.path_list.addItem("No se encontraron resultados en Temario.csv.")

    def get_folder_contents(self, folder_path):
        """ Retorna la lista de archivos en el directorio especificado. """
        try:
            # Obtener la lista de archivos en el directorio
            if os.path.exists(folder_path):
                return os.listdir(folder_path)
            else:
                return None
        except Exception as e:
            print(f"Error al acceder a {folder_path}: {e}")
            return None
