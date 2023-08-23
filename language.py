import random
import json

class Vocabulary:
    @classmethod
    def load(cls, file):
        with open(file, 'r') as f:
            return json.load(f)

    @classmethod
    def save(cls, file, vocab):
        with open(file, 'w') as f:
            json.dump(vocab, f, indent=4)

def language_learning_app(vocab):
    keys = list(vocab.keys())
    random.shuffle(keys)

    for count, word in enumerate(keys):
        print(f"Übersetze das Wort: {word}")
        user_input = input("Gib deine Übersetzung auf Englisch ein: ")

        if user_input.lower() == vocab[word].lower():
            print("Richtig!")
        else:
            print("Falsch. Die korrekte Übersetzung lautet:", vocab[word])

        if (count + 1) % 5 == 0:  # Check if 5 words have been learned
            choice = input("Möchtest du weiterlernen? (ja/nein): ")
            if choice.lower() == "nein":
                break

def add_vocabulary(vocab):
    word = input("Gib das Wort ein: ")
    translation = input("Gib die Übersetzung auf Englisch ein: ")

    vocab[word] = translation
    Vocabulary.save("vocab.json", vocab)

    print("Vokabel erfolgreich hinzugefügt.")

def main():
    vocab_file = "vocab.json"
    vocab = Vocabulary.load(vocab_file)

    while True:
        print("1. Lernen starten")
        print("2. Neue Vokabel hinzufügen")
        print("3. Beenden")

        choice = input("Gib deine Auswahl ein: ")

        if choice == "1":
            language_learning_app(vocab)
        elif choice == "2":
            add_vocabulary(vocab)
        elif choice == "3":
            print("Programm beendet.")
            break
        else:
            print("Ungültige Auswahl. Bitte versuche es erneut.")


if __name__ == "__main__":
    main()
