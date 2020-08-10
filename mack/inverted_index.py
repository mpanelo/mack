from mack import parser


class TermRecord:
    @classmethod
    def deserialize(cls, serialization):
        return cls(document_ids=[int(document_id) for document_id in serialization.split(',')])

    def __init__(self, document_ids=None):
        if document_ids is None:
            self.document_ids = []
        else:
            self.document_ids = document_ids

    def serialize(self):
        return ','.join([str(document_id) for document_id in self.document_ids])


class DictionaryInvertedIndex:
    def __init__(self):
        self._index = {}

    def get(self, term):
        return self._index[term] if term in self._index else TermRecord(document_ids=[])

    def terms(self):
        return self._index.keys()

    def add(self, document):
        for term in parser.Tokenizer.tokenize(document.text):
            if term not in self._index:
                self._index[term] = TermRecord(document_ids=[])

            term_record = self._index[term]

            if not term_record.document_ids or term_record.document_ids[-1] != document.id:
                term_record.document_ids.append(document.id)

    def clear(self):
        self._index.clear()

