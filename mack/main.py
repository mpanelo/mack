from mack import fs
from mack import search
from mack import index_io

SEGMENT_FILES_ROOT = "inverted_index_segments"


def main():
    writer = index_io.Writer(dest=SEGMENT_FILES_ROOT)
    inverted_index = search.DictionaryInvertedIndex()

    for documents in fs.batch_read("enron", 100):
        for document in documents:
            inverted_index.add(document)
        writer.write(inverted_index)
        inverted_index.clear()

    index_io.Merger.merge(SEGMENT_FILES_ROOT, "merged_segments.index")


if __name__ == "__main__":
    main()

# splitter = index_io.FileSplitter(index_io.UniquePathGenerator(root="inverted_index_segments"))
# splitter.split("merged_segments.index", 512000)
