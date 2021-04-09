import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

WORDLIST_FILENAME = './words.txt'

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print("  ", len(wordList), "words loaded.")
    return wordList

def displayHand(hand):
    """
    Displays the letters currently in the hand.

    For example:
    >>> displayHand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter,end=" ")       # print all on the same line
    print() 

def dealHand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    numVowels = n // 3
    
    for i in range(numVowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(numVowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand
    
def getFrequencyDict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq

def getWordScore(word, n):
    
    score = 0
    
    for letter in word:
        score += SCRABBLE_LETTER_VALUES.get(letter, 0) * len(word)
         
    if len(word) == n:
        score += 50
    
    return score

def updateHand(hand, word):
    
    new_hand = hand.copy()
    
    for letter in word:
        qty = new_hand.get(letter,0)
        qty -= 1
        new_hand[letter] = qty
        
    return new_hand    
    
def isValidWord(word, hand, wordList):
    if word in wordList:
        
        d1 = getFrequencyDict(word)
        result = []
        
        for key, value in d1.items():
            result.append(value <= hand.get(key, 0))
        
        return False not in result
    
    else:
        return False
    
def calculateHandlen(hand):
    
    length = 0
    
    for value in hand.values():
        length += value
        
    return length

def compChooseWord(hand, wordList, n):
    """
    Given a hand and a wordList, find the word that gives 
    the maximum value score, and return it.

    This word should be calculated by considering all the words
    in the wordList.

    If no words in the wordList can be made from the hand, return None.

    hand: dictionary (string -> int)
    wordList: list (string)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)

    returns: string or None
    """
    # Create a new variable to store the maximum score seen so far (initially 0)
    bestScore = 0
    # Create a new variable to store the best word seen so far (initially None)  
    bestWord = None
    # For each word in the wordList
    for word in wordList:
        # If you can construct the word from your hand
        if isValidWord(word, hand, wordList):
            # find out how much making that word is worth
            score = getWordScore(word, n)
            # If the score for that word is higher than your best score
            if (score > bestScore):
                # update your best score, and best word accordingly
                bestScore = score
                bestWord = word
    # return the best word you found.
    return bestWord

#
# Computer plays a hand
#
def compPlayHand(hand, wordList, n):
    """
    Allows the computer to play the given hand, following the same procedure
    as playHand, except instead of the user choosing a word, the computer 
    chooses it.

    1) The hand is displayed.
    2) The computer chooses a word.
    3) After every valid word: the word and the score for that word is 
    displayed, the remaining letters in the hand are displayed, and the 
    computer chooses another word.
    4)  The sum of the word scores is displayed when the hand finishes.
    5)  The hand finishes when the computer has exhausted its possible
    choices (i.e. compChooseWord returns None).
 
    hand: dictionary (string -> int)
    wordList: list (string)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    """
    # Keep track of the total score
    totalScore = 0
    # As long as there are still letters left in the hand:
    while (calculateHandlen(hand) > 0) :
        # Display the hand
        print("Current Hand: ", end=' ')
        displayHand(hand)
        # computer's word
        word = compChooseWord(hand, wordList, n)
        # If the input is a single period:
        if word == None:
            # End the game (break out of the loop)
            break
            
        # Otherwise (the input is not a single period):
        else :
            # If the word is not valid:
            if (not isValidWord(word, hand, wordList)) :
                print('This is a terrible error! I need to check my own code!')
                break
            # Otherwise (the word is valid):
            else :
                # Tell the user how many points the word earned, and the updated total score 
                score = getWordScore(word, n)
                totalScore += score
                print('"' + word + '" earned ' + str(score) + ' points. Total: ' + str(totalScore) + ' points')              
                # Update hand and show the updated hand to the user
                hand = updateHand(hand, word)
                print()
    # Game is over (user entered a '.' or ran out of letters), so tell user the total score
    print('Total score: ' + str(totalScore) + ' points.')
        
def playHand(hand, wordList, n):
        
    word = ''
    total_score = 0
    
    while word != "." and calculateHandlen(hand) > 0:
        
        print('Current Hand: ', end=' '), displayHand(hand)
        word = input('Enter a word, or a "." to indicate that you are finished: ')
        
        if not isValidWord(word, hand, wordList):
            if word == ".":
                pass
            else:
                print('Invalid word, please try again.')
        else:
            word_score = getWordScore(word, n)
            total_score += word_score
            print(f'"{word}" earned {word_score} points. Total:{total_score} points.')
            hand = updateHand(hand, word)
        
        #return total_score
    
        if word == '.':
            print(f'Goodbye! Total score: {total_score}.')
        elif calculateHandlen(hand) == 0:
            print(f'Run out of letters. Total score:{total_score}.')    
        
    return

def playGame(wordList):

    HAND_SIZE = 10
    
    choice = ''
    player = ''
    hand = {}
    
    while True:
        
        choice = input('Enter n to deal a new hand, r to replay the last hand, or e to end game: ')
    
        if choice == 'e':
            break
        
        elif choice not in ['n', 'r']:
            print('Invalid command.')
            pass
        
        else:
                       
            if choice == 'r' and hand:
                
                while True:
                    player =  input('Enter u to have yourself play, c to have the computer play: ')
                    if player not in ['u', 'c']:
                        print('Invalid command.')
                    else:
                        break
                    
                if player == 'u':
                    playHand(hand, wordList, HAND_SIZE)
                
                else:
                    compPlayHand(hand, wordList, HAND_SIZE)
                
            elif choice == 'r' and not hand:
                    print('You have not played a hand yet. Please play a new hand first!')
                
            else:
                
                hand = dealHand(HAND_SIZE)
                
                while True:
                    player =  input('Enter u to have yourself play, c to have the computer play: ')
                    if player not in ['u', 'c']:
                        print('Invalid command.')
                    else:
                        break
                    
                if player == 'c':
                    compPlayHand(hand, wordList, HAND_SIZE)
                
                else:
                    playHand(hand, wordList, HAND_SIZE)
    
    return
    
#Test
wordList = loadWords()
playGame(wordList)
        
    
    
    
    
    