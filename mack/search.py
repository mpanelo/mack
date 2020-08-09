import string
import collections

TermRecord = collections.namedtuple('TermRecord', 'document_ids')


class DictionaryIndex:
    def __init__(self):
        self.index = {}

    def contains(self, key):
        return key in self.index

    def terms(self):
        return self.index.keys()

    def __setitem__(self, key, value):
        self.index[key] = value

    def __getitem__(self, key):
        return self.index[key]


class InvertedIndex:
    def __init__(self, index: DictionaryIndex):
        self.index = index

    def add(self, document):
        tokens = Tokenizer.tokenize(document.text)

        for token in tokens:
            if not self.index.contains(token):
                self.index[token] = TermRecord(document_ids=[])

            term_record = self.index[token]

            if not term_record.document_ids or term_record.document_ids[-1] != document.id:
                term_record.document_ids.append(document.id)

    def save(self, filename):
        with open(filename, 'w') as file:
            for term in sorted(self.index.terms()):
                document_ids = [str(document_id) for document_id in self.index[term].document_ids]
                file.write("{};{}\n".format(term, ','.join(document_ids)))


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
