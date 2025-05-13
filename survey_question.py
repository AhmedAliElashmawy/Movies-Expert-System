from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFormLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QVBoxLayout, QMainWindow,
    QSizePolicy, QHBoxLayout, QButtonGroup
)
from pyswip import Prolog
import sys


class PreferenceGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.imdb_rating_buttons = None
        self.imdb_rating_layout = None
        self.submit_button = None
        self.year_input = None
        self.age_rating_input = None
        self.genre_input = None
        self.language_input = None
        self.imdb_rate_input = None
        self.actors_input = None
        self.director_input = None
        self.layout = None
        self.movie = None
        self.gif_label = None
        self.setWindowTitle("Movie Preferences")
        self.imdb_rating = None
        self.prolog = Prolog()
        self.prolog.consult('movie_expert.pl')

        self.setMaximumSize(800, 1000)

        # Initialize the UI
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: #708090;")

        # Set the background GIF to fill the window
        self.gif_label = QLabel(central_widget)
        self.gif_label.setScaledContents(True)
        self.movie = QMovie("movie theater GIF by James Curran.gif")
        self.gif_label.setMovie(self.movie)
        self.movie.start()

        # Create a central layout to center everything
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter)  # Center everything in the layout

        # Overlay widget for form over background
        overlay_widget = QWidget(central_widget)
        overlay_widget.setAttribute(Qt.WA_TranslucentBackground)

        # Layout for the form
        overlay_layout = QVBoxLayout(overlay_widget)
        overlay_layout.setAlignment(Qt.AlignCenter)  # Center the form layout

        self.layout = QFormLayout()
        overlay_layout.addLayout(self.layout)

        # Add your form inputs here, e.g.:
        self.director_input = QLineEdit()
        self.actors_input = QLineEdit()
        self.genre_input = QLineEdit()
        self.language_input = QLineEdit()
        self.age_rating_input = QLineEdit()
        self.year_input = QLineEdit()
        # self.imdb_rate_input = QLineEdit()
        self.imdb_rating_layout = QHBoxLayout()
        self.imdb_rating_buttons = QButtonGroup(self)
        self.imdb_rating_layout.setSpacing(0)

        # Create square buttons 1-10
        for i in range(1, 11):
            btn = QPushButton(str(i))
            btn.setCheckable(True)
            btn.setFixedSize(30, 30)  # square size
            btn.setStyleSheet("""
                QPushButton {
                    border: 2px solid #ccc;
                    border-radius: 5px;
                    background-color: white;
                }
                QPushButton:checked {
                    background-color: #4caf50;
                    color: white;
                    font-weight: bold;
                }
            """)
            self.imdb_rating_buttons.addButton(btn, i)
            self.imdb_rating_layout.addWidget(btn)
            self.imdb_rating_buttons.buttonClicked[int].connect(self.set_imdb_rating)

        # Set placeholder texts
        self.director_input.setPlaceholderText("e.g., Christopher Nolan")
        self.actors_input.setPlaceholderText("e.g., Tom Hanks, Emma Stone")
        self.genre_input.setPlaceholderText("e.g., Sci-Fi, Drama")
        self.language_input.setPlaceholderText("e.g., English")
        self.age_rating_input.setPlaceholderText("G, PG, PG-13, R")
        self.year_input.setPlaceholderText("e.g., 2010 or 2015-2020")
        # self.imdb_rate_input.setPlaceholderText("e.g., 7.5")

        # Common style for all inputs
        input_style = """
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.85);
                border: 1px solid #2E1A47;
                border-radius: 6px;
                padding: 6px;
                font-size: 14px;
                color: #1A1A40;
            }
            QLineEdit::placeholder {
                color: #2E1A47;
                font-style: italic;
            }
        """

        # Apply style to each input
        self.director_input.setStyleSheet(input_style)
        self.actors_input.setStyleSheet(input_style)
        self.genre_input.setStyleSheet(input_style)
        self.language_input.setStyleSheet(input_style)
        self.age_rating_input.setStyleSheet(input_style)
        self.year_input.setStyleSheet(input_style)
        # self.imdb_rate_input.setStyleSheet(input_style)

        # Add form inputs to the layout
        self.layout.addRow("Favourite Director:", self.director_input)
        self.layout.addRow("Favourite Actors (list or single):", self.actors_input)
        self.layout.addRow("Favourite Genres (list or single):", self.genre_input)
        self.layout.addRow("Preferred Language:", self.language_input)
        self.layout.addRow("Preferred Age Rating (G, PG, PG-13, R):", self.age_rating_input)
        self.layout.addRow("Preferred Year:", self.year_input)
        # self.layout.addRow("Minimum IMDB Rating (1-10):", self.imdb_rate_input)
        self.layout.addRow("Minimum IMDB Rating (1-10):", self.imdb_rating_layout)
        # Add overlay widget with form to the main layout
        main_layout.addWidget(self.gif_label)
        main_layout.addWidget(overlay_widget)

        self.submit_button = QPushButton()
        self.submit_button.setText("Submit")
        self.submit_button.setCursor(Qt.PointingHandCursor)
        self.submit_button.clicked.connect(self.submit_preferences)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #9D7AF0;           /* Soft purple matching vaporwave tone */
                color: #1A1A40;                      /* Deep navy text for contrast */
                border: 2px solid #2E1A47;           /* Dark purple border */
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D6C3FF;          /* Pale lilac on hover */
                
                color: #0B1B3A;                      /* Slightly deeper navy */
            }
            QPushButton:pressed {
                background-color: #FFC7C7;          /* Soft peach/pink on click */
            }
        """)
        self.layout.addRow("", self.submit_button)

    def submit_preferences(self):
        director = self.director_input.text()
        actors = self.actors_input.text().split(',')  # Assuming comma-separated input for multiple actors
        genre = self.genre_input.text().split(',')  # Assuming comma-separated input for multiple genres
        language = self.language_input.text()
        age_rating = self.age_rating_input.text()



        year_text = self.year_input.text().strip()
        if year_text:
            try:
                year = int(year_text)
            except ValueError:
                QMessageBox.warning(self, "Invalid Year", "Invalid year!")
                return
        else:
            QMessageBox.warning(self, "Empty field", "Using 2000 as default year")
            year = 2000

        if self.imdb_rating is not None:
            imdb = int(self.imdb_rating)
        else:
            QMessageBox.warning(self, "Empty field Rating", "Invalid rating!")
            return

        # Clearing any old preferences
        self.prolog.query("retractall(asked(_, _, _))")


        # Assert user preferences

        self.prolog.assertz(f"asked(user, director, '{director}')")  # Director input
        self.prolog.assertz(f"asked(user, actors, {actors})")  # Actors input as list
        self.prolog.assertz(f"asked(user, genre, {genre})")  # Genre input as list
        self.prolog.assertz(f"asked(user, language, '{language}')")  # Language input
        self.prolog.assertz(f"asked(user, age_rating, '{age_rating}')")  # Age rating input
        self.prolog.assertz(f"asked(user, year, {year})")  # Year input as number
        self.prolog.assertz(f"asked(user, imdb_rate, {self.imdb_rating})")  # IMDb rating input as number

        # Update GUI with confirmation
        print("Saved preferences to Prolog.")

        # Query the Prolog for recommendations based on user preferences

        result = list(self.prolog.query("likes_movie(Movie, Score)"))
        # After querying:
        self.prolog.query("retractall(asked(_, _, _))")

        if result:
            # Sort the result by Score in descending order
            sorted_result = sorted(result, key=lambda x: x['Score'], reverse=True)

            # Display sorted recommendations
            for item in sorted_result:
                print(f"Recommended Movie: {item['Movie']} with score: {item['Score']}")
        else:
            # If no recommendations are found
            print("No movies match your preferences.")

    def set_imdb_rating(self, value):
        self.imdb_rating = value


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = PreferenceGUI()
    gui.show()
    sys.exit(app.exec_())
