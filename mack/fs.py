import os
from collections import namedtuple


Document = namedtuple("Document", "id name text")


def read(root):
    documents = []
    counter = 0

    for path, sub_dirs, files in os.walk(root):
        for filename in files:
            abs_path = os.path.join(path, filename)
            with open(abs_path) as file:
                text = file.read()
                documents.append(Document(id=counter, name=abs_path, text=text))
            counter += 1

    return documents
