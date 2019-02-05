# Problem Set 2, hangman.py
# Name: Griffin Leonard
# Collaborators: n/a
# Time spent: 3:00

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------


# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def check_game_won(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for i in secret_word:
        if i not in letters_guessed:
            return False
    return True


def get_word_progress(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes the letters in
      secret_word are all lowercase.
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters and carets (^) that represents
      which letters in secret_word have not been guessed so far.
    '''
    progress = str()
    for i in secret_word:
        if i in letters_guessed:
            progress += i
        else:
            progress += '^'
    return progress


def get_remaining_possible_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which 
      letters have not yet been guessed. The letters should be returned in
      alphabetical order.
    '''
    letters = str()
    for i in string.ascii_lowercase:
        if i not in letters_guessed:
            letters += i
    return letters


def score(secret_word, guesses):
    '''
    secret_word: string, the word the user is guessing; assumes the letters in
      secret_word are all lowercase.
    guesses: integer, remaining number of guesses the user has.
    returns: integer, the user's score
    '''
    unique_letters = int()
    for i in string.ascii_lowercase:
        if i in secret_word:
            unique_letters += 1
    return 2*guesses+3*len(secret_word)*unique_letters


def hint(secret_word, letters):
    '''
    secret_word: string, the word the user is guessing; assumes the letters in
      secret_word are all lowercase.
    letters: string (of letters), comprised of letters that represents which 
      letters have not yet been guessed. The letters should be returned in
      alphabetical order.
    returns: string, a letter to be revealed to the user
    '''
    choose_from = str()
    for i in string.ascii_lowercase:
        if i in letters:
            if i in secret_word:
                choose_from += i
    new = random.randint(0, len(choose_from)-1) 
    exposed_letter = choose_from[new]
    return exposed_letter

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses they start with.

    * The user should start with 10 guesses.

    * Before each round, you should display to the user how many guesses
      they have left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''
    print('Welcome to Hangman!')
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    guesses = 10
    letters_guessed = []
    while not check_game_won(secret_word, letters_guessed):
        print('--------------')
        print('You have', guesses, 'guesses left.')
        print('Available letters:', get_remaining_possible_letters(letters_guessed))
        guess = str(input('Please guess a letter: '))
        if guess not in string.ascii_lowercase:
            if guess in string.ascii_uppercase:
                str.lower(guess)
            else:
                print('Oops! that is not a valid letter. Please input a letter from the alphabet:', get_word_progress(secret_word, letters_guessed))
        if guess in string.ascii_lowercase:
           if guess in secret_word:
               if guess in letters_guessed:
                   print('Opps! You already guessed that letter:', get_word_progress(secret_word, letters_guessed))
               else:
                   letters_guessed.append(guess)
                   print('Good guess:', get_word_progress(secret_word, letters_guessed))
           else:
               print('Opps! That letter is not in my word:', get_word_progress(secret_word, letters_guessed))
               guesses -= 1
               letters_guessed.append(guess)
        if guesses == 0:
            break
    print('--------------')
    if check_game_won(secret_word, letters_guessed):
        print('Congratlations, You won!')
        print('Your total score for this game is:', score(secret_word, guesses))
    else:
        print('Sorry, you ran out of guesses. The word was', secret_word)
           
    

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def hangman_with_help(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses they start with.

    * The user should start with 10 guesses.

    * Before each round, you should display to the user how many guesses
      they have left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make sure that
      the user puts in a letter.

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.

    * If the guess is the symbol ?, you should reveal to the user one of the 
      letters missing from the word at the cost of 2 guesses. If the user does 
      not have 2 guesses remaining, print a warning message. Otherwise, add 
      this letter to their guessed word and continue playing normally.

    Follows the other limitations detailed in the problem write-up.
    '''
    print('Welcome to Hangman!')
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    guesses = 10
    letters_guessed = []
    while not check_game_won(secret_word, letters_guessed):
        print('--------------')
        print('You have', guesses, 'guesses left.')
        print('Available letters:', get_remaining_possible_letters(letters_guessed))
        guess = str(input('Please guess a letter: '))
        if guess not in string.ascii_lowercase:
            if guess in string.ascii_uppercase:
                str.lower(guess)
            elif guess == '?':
                guesses -= 2
                exposed_letter = hint(secret_word, get_remaining_possible_letters(letters_guessed))
                letters_guessed.append(exposed_letter)
                print('Letter revealed:', exposed_letter)
                print(get_word_progress(secret_word, letters_guessed))
            else:
                print('Oops! that is not a valid letter. Please input a letter from the alphabet:', get_word_progress(secret_word, letters_guessed))
        if guess in string.ascii_lowercase:
           if guess in secret_word:
               if guess in letters_guessed:
                   print('Opps! You already guessed that letter:', get_word_progress(secret_word, letters_guessed))
               else:
                   letters_guessed.append(guess)
                   print('Good guess:', get_word_progress(secret_word, letters_guessed))
           else:
               print('Opps! That letter is not in my word:', get_word_progress(secret_word, letters_guessed))
               guesses -= 1
               letters_guessed.append(guess)
        if guesses == 0:
            break
    print('--------------')
    if check_game_won(secret_word, letters_guessed):
        print('Congratlations, You won!')
        print('Your total score for this game is:', score(secret_word, guesses))
    else:
        print('Sorry, you ran out of guesses. The word was', secret_word)


# When you've completed your hangman_with_help function, comment the two similar
# lines below that were used to run the hangman function, and then uncomment
# those two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.

    secret_word = choose_word(wordlist)
    hangman_with_help(secret_word)
