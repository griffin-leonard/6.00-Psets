# 6.0001 Fall 2018
# Written by: sylvant, muneezap, charz, anabell, nhung, wang19k

# Problem Set 3
# Name: Griffin Leonard
# Collaborators: n/a
# Time Spent: 2:00

import string

### DO NOT MODIFY THIS FUNCTION
def load_text(filename):
    """
    Args:
        filename: string, name of file to read
    Returns:
        string, contains file contents
    """
    print("Loading file...")
    inFile = open(filename, 'r', encoding='ascii', errors='ignore')
    line = inFile.read()
    for char in string.punctuation:
        line = line.replace(char, "")
    inFile.close()
    return line.lower()

### Problem 1 ###
def get_frequencies(words):
    """
    Args:
        words: either a string of words or a list of words
    Returns:
        dictionary that maps str:int where each str 
        is a word in words and the corresponding int 
        is the frequency of the word in words
    """
    if type(words) == str:
        wordList = words.split() #converts a string of words into a list of words
    else:
        wordList = words 
    
    #if a word in wordList is in dictA, increase its value (frequency) by 1 
    #otherwise, add the word to dictA with a value (frequency) of 1
    dictA = {}
    for i in wordList:
        if i in dictA.keys():
            dictA[i] += 1
        else:
            dictA.update({i:1})
    return dictA
    

### Problem 2 ###
def find_bigrams(text):
    """
    Args:
        text: string
    Returns:
        list of bigrams from input text
    """
    wordList = text.split()
    wordPairs = []
    pair = False
    for i in wordList:
        #saves the first word in wordList as word1, only executes once
        if not pair:
            word1 = i
            pair = True
        #for every subsequent word in wordList: creates a bigram (word_pair)
        #and updates word1 so the next iteration of the loop correctly creates the next bigram
        else:
            word_pair = word1+' '+i
            wordPairs.append(word_pair)
            word1 = i
    return wordPairs
        

### Problem 3 ###
def calculate_similarity(dict1, dict2):
    """
    Args:
        dict1: frequency dictionary of bigrams for one text
        dict2: frequency dictionary of bigrams for another text
    Returns:
        float, a number between 0 and 1, inclusive 
        representing how similar the texts are to each other
        
        The difference in text frequencies = DIFF sums words 
        from these three scenarios: 
        * If a word occurs in dict1 and dict2 then 
          get the difference in frequencies
        * If a word occurs only in dict1 then take the 
          frequency from dict1
        * If a word occurs only in dict2 then take the 
          frequency from dict2
         The total frequencies = ALL is calculated by summing 
         all frequencies in both dict1 and dict2. 
        Return 1-DIFF/ALL rounded to 2 decimal places
    """
    diffs = [] #list of differences in frequencies for each word
    for i in dict1.keys():
        #if a word is in dict1 and dict2, calculate the difference in frequency 
        #and add it to the list (diffs)
        if i in dict2.keys():
            diffs.append(abs(dict1[i]-dict2[i]))    
        
        #if a word is only in dict1, add its frequency to the list (diffs)
        else:
            diffs.append(dict1[i])
            
    for i in dict2.keys():
        #if a word is only in dict2, add its frequency to the list (diffs)
        if i not in dict1.keys():
            diffs.append(dict2[i])
    
    #adds the items in list (diffs)
    diff = 0
    for i in diffs:
        diff += i
    #finds the total number of words in the dictionaries
    total = 0
    for i in dict1.keys():
        total += dict1[i]
    for i in dict2.keys():
        total += dict2[i]
    return round(1-diff/total,2)

### Problem 4 ###
def get_most_frequent_words(dict1, dict2):
    """
    Args:
        dict1: frequency dictionary for one text
        dict2: frequency dictionary for another text
    Returns:
        list of the most frequent word(s) shared between the 2 texts
        
        The most frequent word is defined as the combined 
        frequency of shared words across both texts.
        If multiple words share the same highest frequency, return
        all of them in alphabetical order.
    """
    #creates a dictionary (freq) including all the words in both dict1 and/or dict2,
    #adding the values for each word that occurs in both dict1 and dict2
    freq = dict1.copy()
    for i in dict2.keys():
        if i in freq:
            freq[i] += dict2[i]
        #if the words aren't in dict1, add the word to freq
        else:
            freq[i] = dict2[i]
    
    #creats a list of all word with the highest values (frequency)
    maxValue = max(freq.values())
    freqWord = []
    for i in freq.keys():
        if freq[i] == maxValue:
            freqWord.append(i)
    return sorted(freqWord)
            
    
filename1 = "hello_world.txt"
filename2 = "hello_friends.txt"

# load texts
text1 = load_text(filename1)
text2 = load_text(filename2)

# get bigrams
bigrams1 = find_bigrams(text1)
bigrams2 = find_bigrams(text2)

# get frequency dictionaries for each text using each method
freq_dict1_word = get_frequencies(text1)
freq_dict2_word = get_frequencies(text2)
freq_dict1_bigram = get_frequencies(bigrams1)
freq_dict2_bigram = get_frequencies(bigrams2)

# get how similar the texts are
similarity_w = calculate_similarity(freq_dict1_word, freq_dict2_word)
similarity_b = calculate_similarity(freq_dict1_bigram, freq_dict2_bigram)
print("Similarity based on words: ", similarity_w)
print("Similarity based on bigrams: ", similarity_b)

# get most frequent word in both texts
most_frequent_word = get_most_frequent_words(freq_dict1_word, freq_dict2_word)
print("Most frequent shared word: ", most_frequent_word)
