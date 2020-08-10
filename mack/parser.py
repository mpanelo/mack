class Tokenizer:
    @staticmethod
    def tokenize(text):
        i = 0

        while i < len(text):
            token = []

            while i < len(text) and text[i].isalnum():
                token.append(text[i])
                i += 1
            if token:
                yield ''.join(token).lower()

            i += 1
