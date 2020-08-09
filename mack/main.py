from mack import fs
from mack import search
from mack import index_io


def main():
    segment_generator = index_io.SegmentGenerator(root="inverted_index_segments")
    writer = index_io.Writer(segment_generator)

    inverted_index = search.DictionaryInvertedIndex()

    for documents in fs.batch_read("enron", 100):
        for document in documents:
            inverted_index.add(document)
        writer.write(inverted_index)
        inverted_index.clear()

    merger = index_io.Merger(destination="merged_segments.index")
    merger.merge(segment_generator.get_generated_segment_paths())


if __name__ == "__main__":
    main()
