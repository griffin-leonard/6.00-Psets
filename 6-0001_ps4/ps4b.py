# Problem Set 4B
# Name: Griffin Leonard
# Collaborators: n/a
# Time Spent: 7:00

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, input_text):
        '''
        Initializes a Message object

        input_text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = input_text
        self.valid_words = load_words('words.txt')

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.

        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]

    def make_shift_dicts(self, input_shifts):
        '''
        Creates a list of dictionaries; each dictionary can be used to apply a
        cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. By shifted down, we mean
        that if 'a' is shifted down by 2, the result is 'c.'

        The dictionary should have 52 keys of all the uppercase letters and
        all the lowercase letters only.

        input_shifts (list of integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a list of dictionaries mapping letter (string) to
                 another letter (string).
        '''
        shifter1 = {}
        shifter2 = {}
        
        lowercaseShift = string.ascii_lowercase
        #maps the lowercase letters (keys) to their shifted value (values) for the dictionaries shifter1 and shifter2 using
        #input_shifts[0] and input_shifts[1] respectively 
        for i in range(len(lowercaseShift)):
            #if the letter's postion in the alphabet (i) plus input_shifts[0] yields a valid position in alphabet,
            #simply map the orginal position (key for shifter1) to the shifted position (value for shifter 1)
            if i+input_shifts[0] < 26:
                shifter1.update({lowercaseShift[i]:lowercaseShift[i+input_shifts[0]]})
            #deals with wrap-around case (when the shifted position is >26 and therefor not a valid index of lowercaseShift)
            else:
                shifter1.update({lowercaseShift[i]:lowercaseShift[i+input_shifts[0]-26]}) 
                
            #uses the same process as above for shifter2
            if i+input_shifts[1] < 26:
                shifter2.update({lowercaseShift[i]:lowercaseShift[i+input_shifts[1]]})
            else:
                shifter2.update({lowercaseShift[i]:lowercaseShift[i+input_shifts[1]-26]})

        uppercaseShift = string.ascii_uppercase
        #uses the same process as above, but now for the uppercase letters
        for i in range(len(uppercaseShift)):
            if i+input_shifts[0] < 26:
                shifter1.update({uppercaseShift[i]:uppercaseShift[i+input_shifts[0]]})
            else:
                shifter1.update({uppercaseShift[i]:uppercaseShift[i+input_shifts[0]-26]})
            if i+input_shifts[1] < 26:
                shifter2.update({uppercaseShift[i]:uppercaseShift[i+input_shifts[1]]})
            else:
                shifter2.update({uppercaseShift[i]:uppercaseShift[i+input_shifts[1]-26]})
        
        return [shifter1,shifter2]


    def apply_shifts(self, shift_dicts):
        '''
        Applies the Caesar Cipher to self.message_text with letter shifts
        specified in shift_dicts. Creates a new string that is self.message_text,
        shifted down the alphabet by some number of characters, determined by
        the shift value that shift_dicts was built with.

        shift_dicts: list of dictionaries; each dictionary with 52 keys, mapping
            lowercase and uppercase letters to their new letters
            (as built by make_shift_dicts)

        Returns: the message text (string) with every letter shifted using the
            input shift_dicts

        '''
        #break shift_dicts into two separate dictionaries
        shifter1 = shift_dicts[0]
        shifter2 = shift_dicts[1]
        
        encryptedMessage = str()
        for i in range(len(self.message_text)):
            #if index i of the message_text is a letter, change it's value using the shift dictionaries
            if self.message_text[i] in string.ascii_letters:
                #alternates between using shifter1 and shifter2
                if i%2 == 0:
                    encryptedMessage += shifter1[self.message_text[i]]
                else:
                    encryptedMessage += shifter2[self.message_text[i]]
            #if index i of the message_text isn't a letter, just concatenate it onto the encrypted message
            else:
                encryptedMessage += self.message_text[i]
                
        return encryptedMessage
            

class PlaintextMessage(Message):
    def __init__(self, input_text, input_shifts):
        '''
        Initializes a PlaintextMessage object.

        input_text (string): the message's text
        input_shifts (list of integers): the list of shifts associated with this message

        A PlaintextMessage object inherits from Message. It has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shifts (list of integers, determined by input shifts)
            self.encryption_dicts (list of dictionaries, built using shifts)
            self.encrypted_message_text (string, encrypted using self.encryption_dict)

        '''
        Message.__init__(self, input_text)
        self.shifts = input_shifts
        self.encryption_dicts = self.make_shift_dicts(input_shifts)
        self.encrypted_message_text = self.apply_shifts(self.encryption_dicts)

    def get_shifts(self):
        '''
        Used to safely access self.shifts outside of the class

        Returns: self.shifts
        '''
        return self.shifts

    def get_encryption_dicts(self):
        '''
        Used to safely access a copy self.encryption_dicts outside of the class

        Returns: a COPY of self.encryption_dicts
        '''
        import copy
        return copy.deepcopy(self.encryption_dicts)

    def get_encrypted_message_text(self):
        '''
        Used to safely access self.encrypted_message_text outside of the class

        Returns: self.encrypted_message_text
        '''
        return self.encrypted_message_text

    def modify_shifts(self, input_shifts):
        '''
        Changes self.shifts of the PlaintextMessage, and updates any other
        attributes that are determined by the shift list.

        input_shifts (list of length 2): the new shift that should be associated with this message.
        [0 <= shift < 26]

        Returns: nothing
        '''
        self.shifts = input_shifts
        self.encryption_dicts = self.make_shift_dicts(input_shifts)
        self.encrypted_message_text = self.apply_shifts(self.encryption_dicts)


class EncryptedMessage(Message):
    def __init__(self, input_text):
        '''
        Initializes an EncryptedMessage object

        input_text (string): the message's text

        an EncryptedMessage object inherits from Message. It has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, input_text)

    def decrypt_message(self):
        '''
        Decrypts self.message_text by trying every possible combination of shift
        values and finding the "best" one.
        We will define "best" as the list of shifts that creates the maximum number
        of valid English words when we use apply_shifts(shifts)on the message text.
        If [a, b] are the original shift values used to encrypt the message, then we
        would expect [(26 - a), (26 - b)] to be the best shift values for
        decrypting it.

        Note: if multiple lists of shifts are equally good, such that they all create
        the maximum number of valid words, you may choose any of those lists
        (and their corresponding decrypted messages) to return.

        Returns: a tuple of the best shift value list used to decrypt the message
        and the decrypted message text using that shift value
        '''
        #keeps track of the greatest number of valid words that can 
        #be created by all the shift values that have been checked so far
        maxValidWords = 0 
                          
        #loops make sure that every combination of shift values (a and b) is checked
        for a in range(26): 
            for b in range (26):
                
                #creates a decoded message with shift values, then turns 
                #the message into a list of "words"
                dicts = self.make_shift_dicts([a,b])
                message = self.apply_shifts(dicts)
                messageWords = message.split()
                
                #finds the number of actual words in each list of "words"
                wordCount = 0 
                for i in messageWords:
                    if is_word(self.valid_words,i):
                        wordCount += 1
                        
                #saves the shift values (a and b) if they yeild more valid words 
                #than all previously checked shift values
                if wordCount > maxValidWords:
                    bestAB = [a,b] #stores the new best shift values
                    maxValidWords = wordCount #updates the greatest number of valid words
        
        #uses best shift values to create a decoded message; returns shift values and message as a tuple
        return (bestAB,self.apply_shifts(self.make_shift_dicts(bestAB)))


def test_plaintext_message():
    '''
    Write two test cases for the PlaintextMessage class here.
    Each one should handle different cases (see handout for
    more details.) Write a comment above each test explaining what
    case(s) it is testing.
    '''
    #test for encoding a string with lowercase, uppercase, and punctuation
    plaintext = PlaintextMessage('Hello!', [2,3])
    print('Expected Output: Jhnoq!')
    print('Actual Output:', plaintext.get_encrypted_message_text())
    
    #test for encoding a string with lowercase, and whitespace
    plaintext = PlaintextMessage('duck castle cat lizard', [5,3])
    print('Expected Output: ixhn ffvyoj hdy qledwg')
    print('Actual Output:', plaintext.get_encrypted_message_text())


def test_encrypted_message():
    '''
    Write two test cases for the EncryptedMessage class here.
    Each one should handle different cases (see handout for
    more details.) Write a comment above each test explaining what
    case(s) it is testing.
    '''
    #test for decoding a string with lowercase, uppercase, and punctuation
    encrypted = EncryptedMessage('Fbjim!')
    print('Expected Output:', ([2,3], 'Hello!'))
    print('Actual Output:', encrypted.decrypt_message())
    
    #test for decoding a string with uppercase, lowercase, and whitespace
    encrypted = EncryptedMessage('ixhn ffvyoj hdy qledwg')
    print('Expected Output:', ([21,23], 'duck castle cat lizard'))
    print('Actual Output:', encrypted.decrypt_message())


def decode_story():
    '''
    Write your code here to decode the story contained in the file story.txt.
    Hint: use the helper function get_story_string and your EncryptedMessage class.

    Returns: a tuple containing (best_shift, decoded_story)
    '''
    story = EncryptedMessage(get_story_string())
    return story.decrypt_message()

if __name__ == '__main__':

    # Uncomment these lines to try running your test cases
    test_plaintext_message()
    test_encrypted_message()

    # Uncomment these lines to try running decode_story_string()
    best_shift, story = decode_story()
    print("Best shift:", best_shift)
    print("Decoded story: ", story)
