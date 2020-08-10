from collections import namedtuple
import os
import shutil

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
            with open(file_name, 'r', encoding='cp1252') as file:
                documents.append(Document(id=counter, name=file_name, text=file.read()))
            counter += 1
        yield documents


def clean_up_dir(dir_path):
    if os.path.exists(dir_path):
        if not os.path.isdir(dir_path):
            raise IOError("Unable to remove '{}' because it is not a directory")
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)


def clean_up_file(file_path):
    if os.path.exists(file_path):
        if not os.path.isfile(file_path):
            raise IOError("Unable to remove '{}' because it is not a file")
        os.remove(file_path)
