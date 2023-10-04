import sys
import random
import sqlite3
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

class Word:
    def __init__(self, deutsch, englisch):
        self.deutsch = deutsch
        self.englisch = englisch

class Sentence:
    def __init__(self, deutsch, englisch):
        self.deutsch = deutsch
        self.englisch = englisch

class LanguageLearningApp(QWidget):
    def __init__(self, conn, learning_type, learn_mode=False):
        super().__init__()
        self.conn = conn
        self.learning_type = learning_type
        self.learn_mode = learn_mode
        self.num_learned = 0
        self.num_correct = 0
        self.num_errors = 0
        self.init_ui()
        self.load_next_item()
        self.update_progress_label()

    def init_ui(self):
        self.layout = QVBoxLayout()

        if self.learning_type == "words":
            self.item_label = QLabel(
                "Übersetze das Wort ins Englische:")
        else:
            self.item_label = QLabel(
                "Übersetze den Satz ins Englische:")

        self.layout.addWidget(self.item_label)

        self.translation_input = QLineEdit()
        self.layout.addWidget(self.translation_input)
        self.translation_input.setFocus()

        self.result_label = QLabel()
        self.layout.addWidget(self.result_label)

        if self.learn_mode:
            self.show_solution_button = QPushButton("Lösung anzeigen")
            self.show_solution_button.clicked.connect(self.show_solution)
            self.layout.addWidget(self.show_solution_button)

        self.check_button = QPushButton("Überprüfen")
        self.check_button.setDefault(True)
        self.check_button.clicked.connect(self.check_translation)
        self.check_button.setToolTip("Drücken Sie Enter, um zu überprüfen")
        self.layout.addWidget(self.check_button)

        self.next_button = QPushButton("Nächstes Element")
        self.next_button.clicked.connect(self.load_next_item)
        self.next_button.setToolTip("Drücken Sie F2 für das nächste Element")
        self.layout.addWidget(self.next_button)

        self.mode_label = QLabel("Lernmodus")
        self.layout.addWidget(self.mode_label)

        self.progress_label = QLabel()
        self.layout.addWidget(self.progress_label)

        self.setLayout(self.layout)

    def load_next_item(self):
        if self.learning_type == "words":
            self.current_item = self.get_random_word()
        else:
            self.current_item = self.get_random_sentence()

        self.num_learned += 1
        self.update_progress_label()

        if self.current_item:
            self.item_label.setText(
                f"Übersetze: '{self.current_item.deutsch}' ins Englische:")
            self.translation_input.clear()
            self.result_label.clear()
            if self.learn_mode:
                self.show_solution_button.setDisabled(False)
        else:
            self.item_label.setText("Keine Elemente verfügbar.")
            self.show_solution_button.setDisabled(True)

    def get_random_word(self):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT deutsch, englisch FROM words ORDER BY RANDOM() LIMIT 1')
        row = cursor.fetchone()
        if row:
            return Word(*row)
        else:
            return None

    def get_random_sentence(self):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT deutsch, englisch FROM sentences ORDER BY RANDOM() LIMIT 1')
        row = cursor.fetchone()
        if row:
            return Sentence(*row)
        else:
            return None

    def check_translation(self):
        if not self.current_item:
            return
    
        user_input = self.translation_input.text()
        if self.check_translation_case_insensitive(user_input, self.current_item.englisch):
            self.result_label.setText("Richtig!")
            self.num_correct += 1
        else:
            QMessageBox.critical(self, "Falsche Antwort",
                                f"Falsch. Die korrekte Übersetzung lautet: '{self.current_item.englisch}'")
            self.translation_input.setFocus()
            self.num_errors += 1
    
        self.update_statistics()

        self.update_progress_label()

    def check_translation_case_insensitive(self, user_input, correct_translation):
        return user_input.lower() == correct_translation.lower()

    def show_solution(self):
        if self.current_item:
            self.result_label.setText(
                f"Die richtige Übersetzung lautet: '{self.current_item.englisch}'")

    def set_learn_mode(self, learn_mode):
        self.learn_mode = learn_mode
        if learn_mode:
            self.show_solution_button.setDisabled(False)
        else:
            self.show_solution_button.setDisabled(True)
        self.mode_label.setText(
            "Lernmodus" if self.learn_mode else "Testmodus")
        
    def get_progress(self):
        return self.num_learned, self.num_correct
    
    def update_progress_label(self):
        self.progress_label.setText(f"Gelernt: {self.num_learned} / Korrekt: {self.num_correct} / Fehler: {self.num_errors}")
        
    def update_statistics(self):
        conn = sqlite3.connect('vocabulary.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO statistics (learned_count, correct_count, error_count)
            VALUES (?, ?, ?)
        ''', (self.num_learned, self.num_correct, self.num_errors))
        
        conn.commit()
        conn.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.check_translation()
        elif event.key() == Qt.Key_F2:
            self.load_next_item()

class VocabularyApp(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.current_learning_app = None
        self.learn_mode = True
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.learn_words_button = QPushButton("Vokabeln lernen")
        self.learn_words_button.clicked.connect(self.start_learning_words)
        self.layout.addWidget(self.learn_words_button)

        self.learn_sentences_button = QPushButton("Sätze lernen")
        self.learn_sentences_button.clicked.connect(
            self.start_learning_sentences)
        self.layout.addWidget(self.learn_sentences_button)

        self.quit_button = QPushButton("Beenden")
        self.quit_button.clicked.connect(self.close)
        self.layout.addWidget(self.quit_button)

        self.current_learning_app = None
        self.back_button = QPushButton("Zurück")
        self.back_button.clicked.connect(self.show_vocabulary_selection)
        self.back_button.setDisabled(True)
        self.layout.addWidget(self.back_button)

        self.learn_mode_button = QPushButton("Lernmodus wechseln")
        self.learn_mode_button.clicked.connect(self.toggle_learn_mode)
        self.learn_mode_button.setDisabled(True)
        self.layout.addWidget(self.learn_mode_button)

        self.statistics_button = QPushButton("Statistik anzeigen")
        self.statistics_button.clicked.connect(self.show_statistics)
        self.layout.addWidget(self.statistics_button)
        
        self.visualize_statistics_button = QPushButton("Statistiken visualisieren")
        self.visualize_statistics_button.clicked.connect(self.visualize_statistics)
        self.layout.addWidget(self.visualize_statistics_button)

        self.setLayout(self.layout)
        self.setWindowTitle("Sprachlern-App")
        self.resize(450, 200)

    def show_statistics(self):
        conn = sqlite3.connect('vocabulary.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT learned_count, correct_count, error_count FROM statistics ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        
        if row:
            learned_count, correct_count, error_count = row
            QMessageBox.information(self, "Statistik", f"Gelernt: {learned_count}\nKorrekt: {correct_count}\nFehler: {error_count}")
        else:
            QMessageBox.information(self, "Statistik", "Keine Statistik verfügbar.")
        
        conn.close()

    def start_learning_words(self):
        if self.current_learning_app:
            self.layout.removeWidget(self.current_learning_app)
            self.current_learning_app.hide()
        self.current_learning_app = LanguageLearningApp(
            self.conn, "words", learn_mode=self.learn_mode)
        self.layout.addWidget(self.current_learning_app)
        self.learn_words_button.setDisabled(True)
        self.learn_sentences_button.setDisabled(True)
        self.back_button.setDisabled(False)
        self.learn_mode_button.setDisabled(False)

    def start_learning_sentences(self):
        if self.current_learning_app:
            self.layout.removeWidget(self.current_learning_app)
            self.current_learning_app.hide()
        self.current_learning_app = LanguageLearningApp(
            self.conn, "sentences", learn_mode=self.learn_mode)
        self.layout.addWidget(self.current_learning_app)
        self.learn_words_button.setDisabled(True)
        self.learn_sentences_button.setDisabled(True)
        self.back_button.setDisabled(False)
        self.learn_mode_button.setDisabled(False)

    def show_vocabulary_selection(self):
        if self.current_learning_app:
            self.layout.removeWidget(self.current_learning_app)
            self.current_learning_app.hide()
        self.learn_words_button.setDisabled(False)
        self.learn_sentences_button.setDisabled(False)
        self.back_button.setDisabled(True)
        self.learn_mode_button.setDisabled(True)

    def toggle_learn_mode(self):
        self.learn_mode = not self.learn_mode
        if self.current_learning_app:
            self.current_learning_app.set_learn_mode(self.learn_mode)
            
    def visualize_statistics(self):
        conn = sqlite3.connect('vocabulary.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT learned_count, correct_count, error_count FROM statistics')
        rows = cursor.fetchall()
        
        if not rows:
            QMessageBox.information(self, "Statistik", "Keine Statistik verfügbar.")
            return
        
        learned_counts, correct_counts, error_counts = zip(*rows)
        dates = range(1, len(rows) + 1)
        
        plt.figure(figsize=(10, 6))
        
        plt.plot(dates, learned_counts, label="Gelernt", marker='o', linewidth=10, color='#1f77b4ff', linestyle='-')
        plt.plot(dates, correct_counts, label="Korrekt", marker='D', markersize=8, color='#55aa00ff', linestyle='-')
        plt.plot(dates, error_counts, label="Fehler", marker='o', markersize=8, color='#ff0000ff', linestyle='--')
        
        plt.xlabel('Lernversuche')
        plt.ylabel('Anzahl')
        plt.title('Statistikverlauf')
        plt.legend()
        plt.grid(True)
        
        plt.show()
        
        conn.close()

def main():
    app = QApplication(sys.argv)
    conn = sqlite3.connect('vocabulary.db')
    vocab_app = VocabularyApp(conn)
    vocab_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
