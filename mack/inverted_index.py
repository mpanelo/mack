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


class TrieNode:
    ASCII_TABLE_SIZE = 127

    def __init__(self, value=None, is_leaf=False):
        self.value = value
        self.is_leaf = is_leaf
        self.children = [None for _ in range(self.ASCII_TABLE_SIZE)]


class TrieInvertedIndex:

    def __init__(self):
        self.root = TrieNode()

    def insert(self, term, record):
        curr_node = self.root

        for char in term:
            char_index = ord(char)

            if curr_node.children[char_index] is None:
                next_node = TrieNode()
                curr_node.children[char_index] = next_node
            else:
                next_node = curr_node.children[char_index]

            curr_node = next_node

        curr_node.is_leaf = True
        curr_node.value = record

    def prefix_search(self, prefix):
        curr_node = self.root

        for char in prefix:
            char_index = ord(char)
            curr_node = curr_node.children[char_index]

            if curr_node is None:
                return []

        result = []
        self._recursive_search(curr_node, list(prefix), result)
        return result

    def _recursive_search(self, root, chars, result):
        if root.is_leaf:
            result.append((''.join(chars), root.value))

        for char_index, child in enumerate(root.children):
            if child is not None:
                chars.append(chr(char_index))
                self._recursive_search(child, chars, result)
                chars.pop()
