from resources.links import movies_with_imdb_links

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class ResultsGUI(QMainWindow):
    def __init__(self, movie_list, previous_page):
        super().__init__()
        self.previous_page = previous_page
        self.movie_list = movie_list
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Movie Recommendations")
        self.setGeometry(self.previous_page.geometry())
        self.setMinimumSize(500, 800)
        self.setMaximumSize(800, 1000)
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)
        main_widget.setStyleSheet("background-color: #708090;")

        # --- Add image at the top ---
        image_label = QLabel()
        main_layout.addWidget(image_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
        QScrollBar:vertical {
            background: #2F4F4F;
            width: 12px;
            margin: 20px 0 20px 0;
            border-radius: 6px;
        }

        QScrollBar::handle:vertical {
            background: #708090;
            min-height: 30px;
            border-radius: 6px;
        }

        QScrollBar::handle:vertical:hover {
            background: #a9b2bb;
        }

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none;
            height: 20px;
            subcontrol-origin: margin;
        }

        QScrollBar::add-line:vertical:hover, QScrollBar::sub-line:vertical:hover {
            background: none;
        }

        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        """)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        if not self.movie_list:
            scroll_layout.addWidget(QLabel("No recommendations found."))
        else:
            medals = ['🥇', '🥈', '🥉']
            colours = ['#FFD700', '#C0C0C0', '#CD7F32']  # Gold, Silver, Bronze colours
            for idx, movie in enumerate(self.movie_list):
                movie_name = movie.get("Movie", "Unknown")
                score = movie.get("Score", "N/A")
                link = movies_with_imdb_links.get(movie_name)

                # Add image for the first movie
                if idx == 0:
                    filename = '_'.join(movie_name.strip().split())
                    image_path = f"resources/images/{filename}.jpg"
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        pixmap = pixmap.scaledToWidth(400, Qt.SmoothTransformation)
                        image_label.setPixmap(pixmap)
                        image_label.setAlignment(Qt.AlignCenter)
                    else:
                        image_label.setText("Image not found.")
                        image_label.setAlignment(Qt.AlignCenter)
                        image_label.setStyleSheet("color: white; font-size: 18px;")

                # Determine medal and colour
                if idx < 3:
                    medal = medals[idx]
                    colour = colours[idx]
                    label_text = f"{medal} {movie_name} (score: {score})"
                    movie_label = QLabel(label_text)
                    movie_label.setWordWrap(True)
                    movie_label.setStyleSheet(f"font-size: 18px; font-weight: bold; padding: 4px; color: {colour};")
                else:
                    label_text = f"{movie_name} (score: {score})"
                    movie_label = QLabel(label_text)
                    movie_label.setWordWrap(True)
                    movie_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 4px; color: white;")

                scroll_layout.addWidget(movie_label)

                if link:
                    link_label = QLabel(f'<a href="{link}">{link}</a>')
                    link_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
                    link_label.setOpenExternalLinks(True)
                    link_label.setStyleSheet("font-size: 14px; color: blue; padding-left: 12px;")
                    scroll_layout.addWidget(link_label)

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.go_back)
        back_button.setStyleSheet("""
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
        main_layout.addWidget(back_button)

        self.setCentralWidget(main_widget)

    def go_back(self):
        self.previous_page.show()
        self.close()
