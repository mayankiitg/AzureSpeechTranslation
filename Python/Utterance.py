class WordWithDuration:
    def __init__(self, duration: int, offset:int, word: str):
        self.duration = duration
        self.offset = offset
        self.word = word
    
    def __str__(self):
        return f'Duration:{self.duration}\n Offset:{self.offset}\n Word: {self.word}'

class Utterance:
    def __init__(self, originalSentences: list, translation: list, words: list, duration: int):
        self.originalSentences = originalSentences
        self.translation = translation
        self.words = words
        self.duration = 0
    
    def __str__(self):
        return f'originalSentences:{self.originalSentences}\nTranslation:{self.translation}\nWords: {self.words}\nDuration: {self.duration}'
