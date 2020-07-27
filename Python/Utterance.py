from typing import List

class WordWithDuration:
    def __init__(self, duration: int, offset:int, word: str):
        self.duration = duration
        self.offset = offset
        self.word = word
    
    def __str__(self):
        return f'Duration:{self.duration}\n Offset:{self.offset}\n Word: {self.word}'

class Utterance:
    def __init__(self, english: str, hindi: str, words: List[WordWithDuration], duration: int):
        self.English = english
        self.Hindi = hindi
        self.words = words
        self.duration = 0
    
    def __str__(self):
        return f'English:{self.English}\nHindi:{self.Hindi}\nWords: {self.words}\nDuration: {self.duration}'
