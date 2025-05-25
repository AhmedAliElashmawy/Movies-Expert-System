from PyQt5.QtWidgets import QPushButton

class SwitchButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setCheckable(True)
        self.setChecked(False)
        self.setMinimumSize(60, 30)
        self.update_style()
        self.toggled.connect(self.update_style)  # update on toggle
        self.mode = "single"

    def update_style(self):
        if self.isChecked():
            self.setText("Franchises")
            self.mode = "franchise"
            self.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    border: 2px solid #4CAF50;
                    border-radius: 15px;
                    color: white;
                    font-weight: bold;
                }
            """)
        else:
            self.setText("Movies and Series")
            self.mode = "single"
            self.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    border: 2px solid #f44336;
                    border-radius: 15px;
                    color: white;
                    font-weight: bold;
                }
            """)

    def get_mode(self):
        return self.mode
