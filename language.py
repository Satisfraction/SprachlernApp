import random
import json

def load_vocab(file):
    with open(file, 'r') as f:
        return json.load(f)

def save_vocab(file, vocab):
    with open(file, 'w') as f:
        json.dump(vocab, f, indent=4)

def language_learning_app(vocab):
    keys = list(vocab.keys())
    random.shuffle(keys)

    for word in keys:
        print("Übersetze das Wort: ", word)
        user_input = input("Gib deine Übersetzung auf Englisch ein: ")

        if user_input.lower() == vocab[word].lower():
            print("Richtig!")
        else:
            print("Falsch. Die korrekte Übersetzung lautet:", vocab[word])

def add_vocabulary(vocab):
    word = input("Gib das Wort ein: ")
    translation = input("Gib die Übersetzung auf Englisch ein: ")

    vocab[word] = translation
    save_vocab("vocab.json", vocab)

    print("Vokabel erfolgreich hinzugefügt.")


def main():
    vocab_file = "vocab.json"
    vocab = load_vocab(vocab_file)

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
