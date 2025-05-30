import random

from .MultiDropdown import MultiSelectDropdown
from .SwitchButton import SwitchButton

from .results_gui import ResultsGUI

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFormLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QVBoxLayout, QMainWindow,
    QSizePolicy, QHBoxLayout, QButtonGroup, QComboBox, QListWidgetItem, QCheckBox, QListWidget
)
from pyswip import Prolog
import sys
class PreferenceGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.genres_dropdown = None
        self.actors_dropdown = None
        self.selected_actors = None
        self.actor_list = None
        self.result_gui = None
        self.prolog = Prolog()
        self.prolog.consult('movie_expert.pl')
        self.imdb_rating_buttons = None
        self.imdb_rating_layout = None
        self.submit_button = None
        self.year_input = None
        self.age_rating_input = None
        self.language_input = None
        self.imdb_rate_input = None
        self.director_input = None
        self.layout = None
        self.movie = None
        self.gif_label = None
        self.setWindowTitle("Movie Preferences")
        self.gender_input = None
        self.duration_input = None
        self.awards_input = None
        self.switch_button = None
        self.imdb_rating = None


        # Fetch distinct values from Prolog
        self.directors = self.get_prolog_values('director')
        self.actors = self.get_prolog_values('actor')
        self.genres = self.get_prolog_values('genre')
        self.languages = self.get_prolog_values('language')
        self.age_ratings = self.get_prolog_values('age_rating')
        self.years = sorted(self.get_prolog_values('year'))
        self.gender = self.get_prolog_values('lead_gender')
        self.duration = ["1h-1.5h", "1.5h-2h", "2h-3h", ">3h"]
        self.awards = self.get_prolog_values('awards')
        self.setMaximumSize(800, 1000)

        # Initialize the UI
        self.init_ui()

    def get_prolog_values(self, field):
        """Get distinct values for a field from Prolog"""
        result = list(self.prolog.query(f"get_distinct_values({field}, Values)"))
        if result:
            # Extract values from the Prolog result
            values = result[0]['Values']
            # Convert from Prolog format if needed
            if isinstance(values, list):
                return [str(val) for val in values]
            return [str(values)]
        return []

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: #708090;")

        # Set the background GIF to fill the window
        self.gif_label = QLabel(central_widget)
        self.gif_label.setScaledContents(True)
        self.movie = QMovie("resources/movie_theater.gif")
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

        # Create dropdown menus
        self.director_input = QComboBox()
        self.director_input.addItem("", "")  # Empty option to skip
        for director in self.directors:
            self.director_input.addItem(director, director)

        self.actors_dropdown = MultiSelectDropdown(items=self.actors, placeholder="Select actors")
        self.layout.addWidget(self.actors_dropdown)

        self.genres_dropdown = MultiSelectDropdown(items=self.genres, placeholder="Select genres")
        self.layout.addWidget(self.genres_dropdown)

        self.language_input = QComboBox()
        self.language_input.addItem("", "")  # Empty option to skip
        for language in self.languages:
            self.language_input.addItem(language, language)

        self.age_rating_input = QComboBox()
        self.age_rating_input.addItem("", "")  # Empty option to skip
        for rating in self.age_ratings:
            self.age_rating_input.addItem(rating, rating)

        self.duration_input = QComboBox()
        self.duration_input.addItem("", "")  # Empty option to skip
        for duration in self.duration:
            self.duration_input.addItem(duration, duration)

        self.awards_input = QComboBox()
        self.awards_input.addItem("", "")  # Empty option to skip
        for award in self.awards:
            self.awards_input.addItem(award, award)

        self.gender_input = QComboBox()
        self.gender_input.addItem("", "")  # Empty option to skip
        for gender in self.gender:
            self.gender_input.addItem(gender, gender)

        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("2000")
        self.year_input.setMaxLength(4)

        self.switch_button = SwitchButton()

        # IMDB rating buttons layout
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
            if i == 7:
                btn.setChecked(True)  # Make "7" appear selected
                self.set_imdb_rating(7)
            self.imdb_rating_buttons.buttonClicked[int].connect(self.set_imdb_rating)

        dropdown_style = """
            QComboBox {
            background-color: rgba(255, 255, 255, 0.85);
            border: 1px solid #2E1A47;
            border-radius: 6px;
            padding: 6px;
            font-size: 14px;
            color: #1A1A40;
            min-width: 200px;
            }
            QComboBox:hover {
            border: 1px solid #9D7AF0;
            }
            QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid #2E1A47;
            border-top-right-radius: 6px;
            border-bottom-right-radius: 6px;
            }
            QComboBox::down-arrow {
            image: url(resources/down_arrow.png);
            width: 12px;
            height: 12px;
            }
            QComboBox::down-arrow:on {
            top: 1px;
            left: 1px;
            }
        """

        # Style for the input fields
        input_style = """
            QLineEdit {
            background-color: rgba(255, 255, 255, 0.85);
            border: 1px solid #2E1A47;
            border-radius: 6px;
            padding: 6px;
            font-size: 14px;
            color: #1A1A40;
            }
            QLineEdit:focus {
            border: 1px solid #9D7AF0;
            }
            QLineEdit::placeholder {
            color: #A9A9A9;
            }
        """

        # Apply style to each dropdown
        self.gender_input.setStyleSheet(dropdown_style)
        self.director_input.setStyleSheet(dropdown_style)
        self.language_input.setStyleSheet(dropdown_style)
        self.age_rating_input.setStyleSheet(dropdown_style)
        self.duration_input.setStyleSheet(dropdown_style)
        self.awards_input.setStyleSheet(dropdown_style)

        self.year_input.setStyleSheet(input_style)

        # Add form inputs to the layout
        self.layout.addRow("Movie Viewership by Gender:", self.gender_input)
        self.layout.addRow("Favourite Director:", self.director_input)
        self.layout.addRow("Favourite Actor:", self.actors_dropdown)
        self.layout.addRow("Favourite Genre:", self.genres_dropdown)
        self.layout.addRow("Preferred Language:", self.language_input)
        self.layout.addRow("Preferred Age Rating:", self.age_rating_input)
        self.layout.addRow("Preferred Year:", self.year_input)
        self.layout.addRow("Duration:", self.duration_input)
        self.layout.addRow("Number of Awards:", self.awards_input)
        self.layout.addRow("Search for:", self.switch_button)

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
        gender = self.gender_input.currentData()
        director = self.director_input.currentData()
        actor = self.actors_dropdown.get_selected_items()  # Single actor from dropdown
        genre = self.genres_dropdown.get_selected_items()  # Single genre from dropdown
        language = self.language_input.currentData()
        age_rating = self.age_rating_input.currentData()
        year = self.year_input.text()
        duration = self.duration_input.currentData()
        min_duration = 60
        max_duration = 300
        awards = self.awards_input.currentData()
        mode = self.switch_button.get_mode()


        # Handle empty selections

        if not gender:
            gender = "Both"

        if not director:
            director = ""

        if not actor:
            actors_list = ['']
        else:
            actors_list = actor

        # For genres
        if not genre:
            genres_list = ['']
        else:
            genres_list = genre
            
        if not language:
            language = ""

        if not age_rating:
            age_rating = ""
            
        if not year:
            year = 2000

        if not duration:
            duration = ""

        else:
            if '-' in duration:  # e.g., "1h-1.5h"
                parts = duration.replace('h', '').split('-')
                min_duration = float(parts[0]) * 60
                max_duration = float(parts[1]) * 60
            elif duration.startswith('>'):
                min_duration = 180
                max_duration = 300

            min_duration = int(min_duration)
            max_duration = int(max_duration)


        if not awards:
            awards = 0

        if self.imdb_rating is not None:
            imdb = int(self.imdb_rating)
            self.prolog.asserta(f"asked(user, imdb_rate, {imdb})")
        else:
            QMessageBox.warning(self, "Empty field Rating", "Invalid rating!")
            return

        # Clear existing preferences
        self.prolog.retractall("asked(user, _, _)")
        
        # Assert user preferences
        self.prolog.asserta(f"asked(user, director, '{director}')")  # Director input
        self.prolog.asserta(f"asked(user, actors, {actors_list})")  # Actors input as list
        self.prolog.asserta(f"asked(user, genre, {genres_list})")  # Genre input as list
        self.prolog.asserta(f"asked(user, language, '{language}')")  # Language input
        self.prolog.asserta(f"asked(user, age_rating, '{age_rating}')")  # Age rating input
        self.prolog.asserta(f"asked(user, year, {year})")  # Year input as number
        self.prolog.asserta(f"asked(user, imdb_rate, {self.imdb_rating})")  # IMDb rating input as number
        self.prolog.asserta(f"asked(user, lead_gender, '{gender}')")  # Gender input needs quotes
        self.prolog.asserta(f"asked(user, min_duration, {min_duration})")  # Min duration as number
        self.prolog.asserta(f"asked(user, max_duration, {max_duration})")  # Max duration as number
        self.prolog.asserta(f"asked(user, awards, {awards})")  # Awards as number
        self.prolog.asserta(f"asked(user, franchise, '{mode}')")  # Mode input needs quotes


        # Update GUI with confirmation
        print("Saved preferences to Prolog.")

        # Query the Prolog for recommendations based on user preferences

        result = list(self.prolog.query("likes_movie(Movie, Score)"))


        if result:
            # Sort the result by Score in descending order
            sorted_result = sorted(result, key=lambda x: x['Score'], reverse=True)

            # Display sorted recommendations
            recommendations = "Recommended Movies:\n\n"
            for item in sorted_result:
                movie_name = item['Movie']
                score = item['Score']
                recommendations += f"• {movie_name} (score: {score})\n"
                print(f"Recommended Movie: {movie_name} with score: {score}")

            self.result_gui = ResultsGUI(sorted_result, self)
            self.result_gui.show()
            self.hide()
            self.set_values()


        else:
            # If no recommendations are found
            QMessageBox.information(self, "No Results", "No movies match your preferences.")
            print("No movies match your preferences.")

    def set_imdb_rating(self, value):
        self.imdb_rating = value
    
    def set_values(self):
        """Set the values for the dropdowns and inputs."""
        self.director_input.setCurrentText('')
        # Clear the dropdown selections (using a method that should be implemented)
        if hasattr(self.actors_dropdown, 'clear_selection'):
            self.actors_dropdown.clear_selection()
        else:
            print("Warning: MultiSelectDropdown has no clear method")
    
        if hasattr(self.genres_dropdown, 'clear_selection'):
            self.genres_dropdown.clear_selection()
        else:
            print("Warning: MultiSelectDropdown has no clear method")
    
        self.language_input.setCurrentText('')
        self.age_rating_input.setCurrentText('')
        self.year_input.setText('')
        self.duration_input.setCurrentText('')
        self.awards_input.setCurrentText('')
        self.gender_input.setCurrentText('')  # Added this missing reset
    
        # Reset IMDB rating if needed
        if self.imdb_rating_buttons:
            for button in self.imdb_rating_buttons.buttons():
                if int(button.text()) == 7:  # Default to 7 as in init method
                    button.setChecked(True)
                    self.set_imdb_rating(7)
                else:
                    button.setChecked(False)


