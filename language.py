import sys
import random
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QInputDialog
from PyQt5.QtGui import QKeySequence


class Vocabulary:
    @classmethod
    def load(cls, file):
        with open(file, 'r') as f:
            return json.load(f)

    @classmethod
    def save(cls, file, vocab):
        with open(file, 'w') as f:
            json.dump(vocab, f, indent=4)

class LanguageLearningApp(QWidget):
    def __init__(self, vocab):
        super().__init__()
        self.vocab = vocab
        self.keys = list(vocab.keys())
        self.current_word = None
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.word_label = QLabel("Übersetze das Wort:")
        self.layout.addWidget(self.word_label)

        self.translation_input = QLineEdit()
        self.layout.addWidget(self.translation_input)
        self.translation_input.setFocus()  # Setze automatisch den Fokus auf das Eingabefeld

        self.result_label = QLabel()
        self.layout.addWidget(self.result_label)

        self.check_button = QPushButton("Überprüfen")
        self.check_button.setDefault(True)  # Aktiviere Schaltfläche mit der Eingabetaste
        self.check_button.clicked.connect(self.check_translation)
        self.layout.addWidget(self.check_button)

        self.next_button = QPushButton("Nächstes Wort")
        self.next_button.clicked.connect(self.load_next_word)
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)
        self.load_next_word()

    def load_next_word(self):
        self.current_word = random.choice(self.keys)
        self.word_label.setText(f"Übersetze das Wort: {self.current_word}")
        self.translation_input.clear()
        self.result_label.clear()

    def check_translation(self):
        user_input = self.translation_input.text()
        if user_input.lower() == self.vocab[self.current_word].lower():
            self.result_label.setText("Richtig!")
        else:
            self.result_label.setText(f"Falsch. Die korrekte Übersetzung lautet: {self.vocab[self.current_word]}")

class VocabularyApp(QWidget):
    def __init__(self, vocab):
        super().__init__()
        self.vocab = vocab
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
    
        self.learn_button = QPushButton("Lernen starten")
        self.learn_button.setShortcut(QKeySequence("Ctrl+L"))  # Tastaturkürzel Ctrl+L
        self.learn_button.clicked.connect(self.start_learning)
        self.layout.addWidget(self.learn_button)
    
        self.add_button = QPushButton("Neue Vokabel hinzufügen")
        self.add_button.clicked.connect(self.add_vocabulary)
        self.layout.addWidget(self.add_button)
    
        self.quit_button = QPushButton("Beenden")
        self.quit_button.clicked.connect(self.close)
        self.layout.addWidget(self.quit_button)
    
        self.setLayout(self.layout)
    
        # Set the size of the main window
        self.resize(450, 200)

    def start_learning(self):
        self.learning_app = LanguageLearningApp(self.vocab)
        self.learning_app.show()

    def add_vocabulary(self):
        word, translation = self.get_new_vocabulary()
        if word and translation:
            self.vocab[word] = translation
            Vocabulary.save("vocab.json", self.vocab)
            print("Vokabel erfolgreich hinzugefügt.")

    def get_new_vocabulary(self):
        word, ok = QInputDialog.getText(self, "Neue Vokabel hinzufügen", "Gib das Wort ein:")
        if ok:
            translation, ok = QInputDialog.getText(self, "Neue Vokabel hinzufügen", "Gib die Übersetzung auf Englisch ein:")
            if ok:
                return word, translation
        return None, None

def main():
    app = QApplication(sys.argv)
    vocab_file = "vocab.json"
    vocab = Vocabulary.load(vocab_file)
    vocab_app = VocabularyApp(vocab)
    vocab_app.setWindowTitle("Sprachlern-App")
    vocab_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
