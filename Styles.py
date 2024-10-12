# Styles.py

def get_stylesheet(theme="default"):
    if theme == "green":
        button_color = "#28a745"
        hover_color = "#218838"
    elif theme == "orange":
        button_color = "#fd7e14"
        hover_color = "#e55300"
    else:  # Default theme
        button_color = "#007bff"
        hover_color = "#0056b3"
    
    return f"""
        QWidget {{
            background-color: #1c1c1c;
            color: #ffffff;
            font-family: Arial, sans-serif;
            font-size: 14px;
        }}
        QPushButton {{
            background-color: {button_color};
            color: #ffffff;
            border: none;
            padding: 15px;
            font-size: 16px;
            text-align: left;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
        QLabel {{
            color: #ffffff;
            font-size: 16px;
        }}
        QComboBox, QDateEdit, QLineEdit {{
            background-color: #333333;
            color: #ffffff;
            padding: 10px;
            border: 1px solid #444444;
            border-radius: 5px;
            font-size: 16px;
        }}
        QComboBox QAbstractItemView {{
            background-color: #333333;
            selection-background-color: #444444;
            color: #ffffff;
        }}
    """
