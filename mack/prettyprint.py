OFFSET = 50


def print_search_result(term, documentdb, document_ids):
    print("Search Results for {}".format(highlight(term)))

    for i, document_id in enumerate(document_ids):
        path = documentdb.get(document_id)

        with open(path, 'r') as f:
            snippet = get_snippet(f.read().lower(), term)
            highlighted_text = snippet.replace(term, "\u001b[31m{}\u001b[0m".format(term))
            print("{}) {}".format(i+1, highlighted_text))
    print("-----------------------------------------------------------")


def get_snippet(document_text, term):
    idx = document_text.index(term)
    start = max(0, idx-OFFSET)
    end = min(len(document_text), idx+OFFSET)
    return document_text[start:end]


def highlight(text):
    return "\u001b[31m{}\u001b[0m".format(text)
