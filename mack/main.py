from mack import fs
from mack import search

documents = {}


def main():
    index = search.DictionaryIndex()
    inverted_index = search.InvertedIndex(index)

    for document in fs.read("enron"):
        inverted_index.add(document)
        documents[document.id] = document

    inverted_index.save('test.index')


if __name__ == "__main__":
    main()
