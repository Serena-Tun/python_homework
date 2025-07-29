# Task 4: Closure Practice

def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter)
        display = ''.join([char if char in guesses else '_' for char in secret_word])
        print(display)
        return all(char in guesses for char in secret_word)
    return hangman_closure

if __name__ == "__main__":
    secret = input("Enter the secret word: ").lower()
    print("\n" * 50)  # Clear screen effect
    guess_func = make_hangman(secret)

    while True:
        letter = input("Guess a letter: ").lower()
        is_complete = guess_func(letter)
        if is_complete:
            print("Congratulations! You've guessed the word!")
            break
