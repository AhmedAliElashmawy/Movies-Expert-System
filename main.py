import sys

from PyQt5.QtWidgets import QApplication
from  GUI.survey_question import PreferenceGUI


def main():
    app = QApplication(sys.argv)
    gui = PreferenceGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()