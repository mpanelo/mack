import os
from collections import namedtuple


Document = namedtuple("Document", "id name text")


def batch_read(root, batch_size=100):
    documents = []
    counter = 0

    for path, sub_dirs, file_names in os.walk(root):
        for file_name in file_names:
            abs_file_path = os.path.join(path, file_name)

            with open(abs_file_path) as file:
                documents.append(Document(id=counter, name=abs_file_path, text=file.read()))

            if len(documents) > batch_size:
                yield documents
                documents = []

            counter += 1
