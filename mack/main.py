from mack import fs
from mack import inverted_index
from mack import index_io
from mack import parser
import time
import argparse

SEGMENT_FILES_ROOT = "inverted_index_segments"
MERGED_INVERTED_INDEX_FILE = "merged_inverted_index.index"
INDEX_LOOKUP_TABLE = "inverted_index_lookup.txt"
SAMPLE_ENRON_DATA_SET = "enron"
FULL_ENRON_DATA_SET = "enron_mail_20150507"


def main():
    args = parse_args()

    if args.sample_build or args.full_build:
        build_index_start_time = time.time()
        build_index(SAMPLE_ENRON_DATA_SET if args.sample_build else FULL_ENRON_DATA_SET)
        print("Index took {:.2f}s to build!".format(time.time() - build_index_start_time))
    elif args.query:
        search_start_time = time.time()
        search(args.query)
        print("Search took {:.2f}s!".format(time.time() - search_start_time))


def parse_args():
    arg_parser = argparse.ArgumentParser(description="MACK - The Enron email search engine")
    group = arg_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-sb", "--sample-build",
                       dest="sample_build",
                       action="store_true",
                       help="Build the inverted index of the sample data set and store to disk")
    group.add_argument("-fb", "--full-build",
                       dest="full_build",
                       action="store_true",
                       help="Build the inverted index of the entire data set and store to disk")
    group.add_argument("-s", "--search",
                       dest="query",
                       help="Search through Enron email corpus with a single term")
    return arg_parser.parse_args()


def search(query):
    terms = list(parser.Tokenizer.tokenize(query))
    table = index_io.IndexLookupTable(src=INDEX_LOOKUP_TABLE)
    index = inverted_index.TrieInvertedIndex()

    for query_term in terms:
        segment_file = table[query_term]
        for term, record in index_io.SegmentLoader.load(segment_file):
            index.insert(term, record)

    result = index.prefix_search(terms[0])
    for term, record in result:
        print(term, record.document_ids)


def build_index(data_set_path):
    writer = index_io.Writer(dest=SEGMENT_FILES_ROOT)
    index = inverted_index.DictionaryInvertedIndex()

    for documents in fs.batch_read(data_set_path, 1000):
        for document in documents:
            index.add(document)
        writer.write(index)
        index.clear()

    index_io.Merger.merge(src=SEGMENT_FILES_ROOT, dest=MERGED_INVERTED_INDEX_FILE)

    splitter = index_io.FileSplitter(dest=SEGMENT_FILES_ROOT, lookup_table_dest=INDEX_LOOKUP_TABLE)
    splitter.split(src=MERGED_INVERTED_INDEX_FILE, chunk_size=1048576)


if __name__ == "__main__":
    main()
