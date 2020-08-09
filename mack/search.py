import string
import collections

TermRecord = collections.namedtuple('TermRecord', 'document_ids')


class DictionaryInvertedIndex:
    def __init__(self):
        self._index = {}

    def get(self, term):
        return self._index[term] if term in self._index else TermRecord(document_ids=[])

    def terms(self):
        return self._index.keys()

    def add(self, document):
        tokens = Tokenizer.tokenize(document.text)

        for token in tokens:
            if token not in self._index:
                self._index[token] = TermRecord(document_ids=[])

            term_record = self._index[token]

            if not term_record.document_ids or term_record.document_ids[-1] != document.id:
                term_record.document_ids.append(document.id)

    def clear(self):
        self._index.clear()


class Tokenizer:
    @staticmethod
    def tokenize(text):
        i = 0
        tokens = []

        while i < len(text):
            token = []
            while i < len(text) and (text[i] in string.digits or text[i] in string.ascii_letters):
                token.append(text[i])
                i += 1
            if token:
                tokens.append(''.join(token).lower())
            i += 1

        return tokens
