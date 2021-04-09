# Hangman game
import random

WORDLIST_FILENAME = 'words.txt'

def loadWords():
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


def chooseWord(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)
    
wordlist = loadWords()

secretWord = chooseWord(wordlist)

def isWordGuessed(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    
    lettersGuessed: list, what letters have been guessed so far
    
    returns: boolean, True if all the letters of secretWord are in lettersGuessed;
    False otherwise
    '''
    wordLetters = list(secretWord)

    for e in secretWord:
        if e in lettersGuessed:
            wordLetters.remove(e)

    return len(wordLetters) == 0


def getGuessedWord(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    
    lettersGuessed: list, what letters have been guessed so far
    
    returns: string, comprised of letters and underscores that represents
    what letters in secretWord have been guessed so far.
    '''
    wordLetters = list(secretWord)
    guess = ''

    for index, item in enumerate(wordLetters):
        if item not in lettersGuessed:
            wordLetters[index] = '_ '

    return guess.join(wordLetters)


def getAvailableLetters(lettersGuessed):
    '''
    lettersGuessed: list, what letters have been guessed so far
    
    returns: string, comprised of letters that represents what letters have not
    yet been guessed.
    '''
    import string
    alphabet = list(string.ascii_lowercase)
    r = ''

    for e in lettersGuessed:
        alphabet.remove(e)

    return r.join(alphabet)

def hangman(secretWord):
    print('\nWelcome to the game, Hangman!')
    print('\nI am thinking of a word that is', len(secretWord), 'letters long')
    print('-----------')
    mistakesMade = 0
    lettersGuessed = []
    availableLetters = getAvailableLetters(lettersGuessed)

    while mistakesMade < 8:
        if isWordGuessed(secretWord, lettersGuessed):
            print('Congratulations, you won!')
            break
        else:
            print('You have', 8 - mistakesMade, 'guesses left')
            print('\nAvailable letters: ' + getAvailableLetters(lettersGuessed))
            letter = input("Please guess a letter: ").lower()   
            if letter in availableLetters and letter not in lettersGuessed:
                if letter in secretWord:
                    lettersGuessed.append(letter) 
                    availableLetters = getAvailableLetters(lettersGuessed)
                    print('\nGood guess: ' + getGuessedWord(secretWord, lettersGuessed))
                    print('-----------')
                else:
                    mistakesMade += 1
                    lettersGuessed.append(letter)
                    if mistakesMade != 8:
                        print("\nOops! That letter is not in my word: " + getGuessedWord(secretWord, lettersGuessed))   
                        print('-----------')
                    else:
                        print("\nOops! That letter is not in my word: " + getGuessedWord(secretWord, lettersGuessed))
                        print('-----------')
                        print('\nSorry, you ran out of guesses. The word was else.')
            else:
                print("\nOops! You've already guessed that letter:" + getGuessedWord(secretWord, lettersGuessed))         
                print('-----------')
    return 

hangman(secretWord)