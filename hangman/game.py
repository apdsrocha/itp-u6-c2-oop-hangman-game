from .exceptions import *
import random


class GuessAttempt(object):
    def __init__(self, char, miss=None, hit=None):
        self.char = char
        self.miss = miss
        self.hit = hit
        
        if all([miss,hit]):
            raise InvalidGuessAttempt()
        
    def is_hit(self):
        if self.hit: 
            return True
        return False
            
    def is_miss(self): 
        if self.miss:
            return True
        return False


class GuessWord(object):
    def __init__(self, word_to_guess):
        if not word_to_guess:
            raise InvalidWordException()
        self.answer = word_to_guess.lower()
        self.masked = self.masked_word(self.answer)
    
    def perform_attempt(self, char):
        if len(char) > 1:
            raise InvalidGuessedLetterException()
        
        if char.lower() not in self.answer:
            return GuessAttempt(char, miss=True)
        
        new_word = ''

        for answer_char, masked_char in zip(self.answer, self.masked):
            if char.lower() == answer_char:
                new_word += answer_char
            else:
                new_word += masked_char

        self.masked = new_word
        return GuessAttempt(char, hit=True)
    
    def masked_word(self, word):
        return '*' * len(word)
    

class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    def __init__(self, word_list=None, number_of_guesses=5):
        if not word_list:
            word_list = self.WORD_LIST
        self.word = GuessWord(self.select_random_word(word_list))
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
    
    @classmethod
    def select_random_word(self, word_list=None):
        if not word_list:
            raise InvalidListOfWordsException()
        return random.choice(word_list)
        
    def is_won(self):
        return self.word.masked == self.word.answer

    def is_lost(self):
        return self.remaining_misses == 0

    def is_finished(self):
        return self.is_won() or self.is_lost()

    def guess(self, char):
        char = char.lower()
        if char in self.previous_guesses:
            raise InvalidGuessedLetterException()

        if self.is_finished():
            raise GameFinishedException()

        self.previous_guesses.append(char)
        attempt = self.word.perform_attempt(char)
        if attempt.is_miss():
            self.remaining_misses -= 1

        if self.is_won():
            raise GameWonException()

        if self.is_lost():
            raise GameLostException()

        return attempt
    