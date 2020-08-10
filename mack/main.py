from mack import fs
from mack import inverted_index
from mack import index_io
from mack import parser
import time

SEGMENT_FILES_ROOT = "inverted_index_segments"
MERGED_INVERTED_INDEX_FILE = "merged_inverted_index.index"
INDEX_LOOKUP_TABLE = "inverted_index_lookup.txt"


def main():
    build_index_start_time = time.time()
    build_index()
    print("Index took {:.2f}s to build!".format(time.time() - build_index_start_time))


def search(query):
    terms = parser.Tokenizer.tokenize(query)


def build_index():
    writer = index_io.Writer(dest=SEGMENT_FILES_ROOT)
    index = inverted_index.DictionaryInvertedIndex()

    for documents in fs.batch_read("enron", 1000):
        for document in documents:
            index.add(document)
        writer.write(index)
        index.clear()

    index_io.Merger.merge(src=SEGMENT_FILES_ROOT, dest=MERGED_INVERTED_INDEX_FILE)

    splitter = index_io.FileSplitter(dest=SEGMENT_FILES_ROOT, lookup_table_dest=INDEX_LOOKUP_TABLE)
    splitter.split(src=MERGED_INVERTED_INDEX_FILE, chunk_size=1048576)


if __name__ == "__main__":
    main()
