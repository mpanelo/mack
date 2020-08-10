import json


class DocumentDB:
    @classmethod
    def load_from(cls, src):
        with open(src, 'r') as f:
            cls(db=json.load(f))

    def __init__(self, db=None):
        if db is None:
            self.db = {}
        else:
            self.db = db

    def add(self, id, document):
        self.db[id] = document.name

    def save_to(self, dest):
        with open(dest, 'w') as f:
            json.dump(self.db, f)

