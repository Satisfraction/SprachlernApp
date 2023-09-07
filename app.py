import sys
import random
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QKeySequence

def get_random_word(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT deutsch, englisch FROM words ORDER BY RANDOM() LIMIT 1')
    row = cursor.fetchone()
    if row:
        return row
    else:
        return None, None

def get_random_sentence(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT deutsch, englisch FROM sentences ORDER BY RANDOM() LIMIT 1')
    row = cursor.fetchone()
    if row:
        return row
    else:
        return None, None

def check_translation_case_insensitive(user_input, correct_translation):
    return user_input.lower() == correct_translation.lower()

class LanguageLearningApp(QWidget):
    def __init__(self, conn, learning_type):
        super().__init__()
        self.conn = conn
        self.learning_type = learning_type
        self.init_ui()
        self.load_next_item()

    def init_ui(self):
        self.layout = QVBoxLayout()

        if self.learning_type == "words":
            self.item_label = QLabel("Übersetze das Wort:")
        else:
            self.item_label = QLabel("Übersetze den Satz:")

        self.layout.addWidget(self.item_label)

        self.translation_input = QLineEdit()
        self.layout.addWidget(self.translation_input)
        self.translation_input.setFocus()

        self.result_label = QLabel()
        self.layout.addWidget(self.result_label)

        self.check_button = QPushButton("Überprüfen")
        self.check_button.setDefault(True)
        self.check_button.clicked.connect(self.check_translation)
        self.layout.addWidget(self.check_button)

        self.next_button = QPushButton("Nächstes Element")
        self.next_button.clicked.connect(self.load_next_item)
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)

    def load_next_item(self):
        if self.learning_type == "words":
            self.current_item, self.current_translation = get_random_word(self.conn)
        else:
            self.current_item, self.current_translation = get_random_sentence(self.conn)

        if self.current_item:
            self.item_label.setText(f"Übersetze das Element: {self.current_item}")
            self.translation_input.clear()
            self.result_label.clear()
        else:
            self.item_label.setText("Keine Elemente verfügbar.")

    def check_translation(self):
        if not self.current_item:
            return

        user_input = self.translation_input.text()
        if check_translation_case_insensitive(user_input, self.current_translation):
            self.result_label.setText("Richtig!")
        else:
            self.result_label.setText(f"Falsch. Die korrekte Übersetzung lautet: {self.current_translation}")

class VocabularyApp(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.learn_words_button = QPushButton("Vokabeln lernen")
        self.learn_words_button.clicked.connect(self.start_learning_words)
        self.layout.addWidget(self.learn_words_button)

        self.learn_sentences_button = QPushButton("Sätze lernen")
        self.learn_sentences_button.clicked.connect(self.start_learning_sentences)
        self.layout.addWidget(self.learn_sentences_button)

        self.quit_button = QPushButton("Beenden")
        self.quit_button.clicked.connect(self.close)
        self.layout.addWidget(self.quit_button)

        self.setLayout(self.layout)
        self.setWindowTitle("Sprachlern-App")
        self.resize(450, 200)

    def start_learning_words(self):
        self.learning_app = LanguageLearningApp(self.conn, "words")
        self.learning_app.show()

    def start_learning_sentences(self):
        self.learning_app = LanguageLearningApp(self.conn, "sentences")
        self.learning_app.show()

def main():
    app = QApplication(sys.argv)
    conn = sqlite3.connect('vocabulary.db')
    vocab_app = VocabularyApp(conn)
    vocab_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
