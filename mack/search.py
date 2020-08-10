from mack import parser
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
        for token in parser.Tokenizer.tokenize(document.text):
            if token not in self._index:
                self._index[token] = TermRecord(document_ids=[])

            term_record = self._index[token]

            if not term_record.document_ids or term_record.document_ids[-1] != document.id:
                term_record.document_ids.append(document.id)

    def clear(self):
        self._index.clear()

