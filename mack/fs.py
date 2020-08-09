import os
from collections import namedtuple


Document = namedtuple("Document", "id name text")


def batch_read(root, batch_size=100):
    counter = 0
    file_names = [os.path.join(path, file_name)
                  for path, _, file_names in os.walk(root)
                  for file_name in file_names]

    for i in range(0, len(file_names), batch_size):
        batch_file_names = file_names[i:i+batch_size]
        documents = []
        for file_name in batch_file_names:
            with open(file_name) as file:
                documents.append(Document(id=counter, name=file_name, text=file.read()))
            counter += 1
        yield documents
