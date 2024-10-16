# app.py

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget,
    QStackedWidget, QLabel, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSettings
from Clases.Clases import Clases
from Syllabus import Syllabus
from Materiales import Materiales
import Styles
import qtawesome as qta  # Importing QtAwesome for icons

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Student Interface")
        self.settings = QSettings("MyCompany", "MyApp")
        self.restore_settings()

        # Apply default stylesheet
        self.current_style = "default"
        self.apply_stylesheet(self.current_style)

        # Main layout
        main_layout = QVBoxLayout()

        # Top bar layout
        top_bar_layout = QHBoxLayout()

        # Spacer on the left side of the top bar
        top_bar_layout.addStretch()

        # Label for Themes
        themes_label = QLabel("Themes")
        themes_label.setStyleSheet("color: white; font-size: 12px; margin-right: 10px;")
        top_bar_layout.addWidget(themes_label)

        # Green theme button
        green_button = QPushButton()
        green_button.setFixedSize(20, 20)
        green_button.setStyleSheet("border-radius: 10px; background-color: #28a745;")
        green_button.setIcon(qta.icon('fa.circle', color='white'))
        green_button.clicked.connect(lambda: self.apply_stylesheet("green"))
        top_bar_layout.addWidget(green_button)
        
        # Orange theme button
        orange_button = QPushButton()
        orange_button.setFixedSize(20, 20)
        orange_button.setStyleSheet("border-radius: 10px; background-color: #fd7e14;")
        orange_button.setIcon(qta.icon('fa.circle', color='white'))
        orange_button.clicked.connect(lambda: self.apply_stylesheet("orange"))
        top_bar_layout.addWidget(orange_button)
        
        # Blue theme button
        blue_button = QPushButton()
        blue_button.setFixedSize(20, 20)
        blue_button.setStyleSheet("border-radius: 10px; background-color: #007bff;")
        blue_button.setIcon(qta.icon('fa.circle', color='white'))
        blue_button.clicked.connect(lambda: self.apply_stylesheet("default"))
        top_bar_layout.addWidget(blue_button)

        # Align theme elements to the right of the top bar
        top_bar_layout.setContentsMargins(0, 5, 10, 0)

        # Main content layout
        content_layout = QHBoxLayout()

        # Sidebar layout with buttons
        sidebar_layout = QVBoxLayout()
        
        # Add Image at the top of the sidebar
        image_label = QLabel()
        pixmap = QPixmap("Sources/UNI.png")
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setScaledContents(True)
        image_label.setMaximumSize(340, 200)  # Set maximum size for responsiveness
        sidebar_layout.addWidget(image_label)

        # Spacer to move buttons to the middle of the sidebar
        sidebar_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Create buttons for navigation with icons
        clases_button = QPushButton("Clases Virtuales")
        clases_button.setIcon(qta.icon('fa.video-camera'))  # Icon for virtual classes
        clases_button.setStyleSheet("padding-left: 20px;")  # Adjust padding for icon
        clases_button.clicked.connect(self.show_clases)

        syllabus_button = QPushButton("Materiales - Silabus")
        syllabus_button.setIcon(qta.icon('fa.book'))  # Icon for syllabus
        syllabus_button.setStyleSheet("padding-left: 20px;")
        syllabus_button.clicked.connect(self.show_syllabus)

        materiales_button = QPushButton("Materiales - Académicos")
        materiales_button.setIcon(qta.icon('fa.folder-open'))  # Icon for materials
        materiales_button.setStyleSheet("padding-left: 20px;")
        materiales_button.clicked.connect(self.show_materiales)

        # Add buttons to the sidebar layout
        sidebar_layout.addWidget(clases_button)
        sidebar_layout.addWidget(syllabus_button)
        sidebar_layout.addWidget(materiales_button)

        # Spacer below the buttons
        sidebar_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Create a widget for the sidebar layout
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)

        # Stack widget to hold the different pages
        self.stack = QStackedWidget()
        
        # Add pages to the stack
        self.clases_page = Clases()
        self.syllabus_page = Syllabus()
        self.materiales_page = Materiales()

        self.stack.addWidget(self.clases_page)
        self.stack.addWidget(self.syllabus_page)
        self.stack.addWidget(self.materiales_page)

        # Add the sidebar and main stack to the content layout
        content_layout.addWidget(sidebar_widget, 1)  # Sidebar with a fixed width
        content_layout.addWidget(self.stack, 4)      # Main content area with more space

        # Add layouts to main layout
        main_layout.addLayout(top_bar_layout)
        main_layout.addLayout(content_layout)

        # Set the main layout to the central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def show_clases(self):
        self.stack.setCurrentWidget(self.clases_page)

    def show_syllabus(self):
        self.stack.setCurrentWidget(self.syllabus_page)

    def show_materiales(self):
        self.stack.setCurrentWidget(self.materiales_page)

    def wheelEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.scale_factor *= 1.1
            else:
                self.scale_factor /= 1.1
            self.apply_zoom()

    def apply_zoom(self):
        self.setStyleSheet(Styles.get_stylesheet(self.current_style).replace(
            "font-size: 14px;", f"font-size: {int(14 * self.scale_factor)}px;"
        ))

    def apply_stylesheet(self, style_name):
        self.current_style = style_name
        self.setStyleSheet(Styles.get_stylesheet(style_name))
    
    def restore_settings(self):
        size = self.settings.value("size", self.size())
        pos = self.settings.value("pos", self.pos())
        self.resize(size)
        self.move(pos)
    
    def closeEvent(self, event):
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        event.accept()

# Run the application
app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
