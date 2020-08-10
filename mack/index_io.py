from mack import inverted_index
from mack import fs
import bisect
import collections
import heapq
import os


class SegmentLoader:
    @staticmethod
    def load(path):
        segment = []
        with open(path, 'r') as file:
            for line in file:
                term, serialized_record = line.rstrip().split(';')
                record = inverted_index.TermRecord.deserialize(serialized_record)
                segment.append((term, record))
        return segment


class IndexLookupTable:
    def __init__(self, src):
        if not os.path.exists(src) or not os.path.isfile(src):
            raise IOError("'{}' is not a file or does not exist".format(src))
        self.lookup_table = IndexLookupTable._load_lookup_table(src)

    @staticmethod
    def _load_lookup_table(src):
        lookup_table = []
        with open(src, 'r') as file:
            for line in file:
                term, path = line.rstrip().split(';')
                lookup_table.append((term, path))
        return lookup_table

    def __getitem__(self, term):
        terms, segment_files = zip(*self.lookup_table)
        index = bisect.bisect_left(terms, term)
        return segment_files[index]


class UniquePathGenerator:
    def __init__(self, root, prefix="segment", extension='index'):
        self.root = root
        self.prefix = prefix
        self.extension = extension
        self.counter = 0

    def generate(self):
        file_name = "{}_{:03}.{}".format(self.prefix, self.counter, self.extension)
        path = os.path.join(self.root, file_name)
        self.counter += 1
        return path


class Writer:
    def __init__(self, dest):
        fs.clean_up_dir(dest)
        self.path_generator = UniquePathGenerator(dest)

    def write(self, index: inverted_index.DictionaryInvertedIndex):
        with open(self.path_generator.generate(), 'w') as file:
            for term in sorted(index.terms()):
                record = index.get(term)
                file.write("{};{}\n".format(term, record.serialize()))


class Merger:
    Buffer = collections.namedtuple('Buffer', 'term document_id_groups')

    @staticmethod
    def merge(src, dest):
        Merger._validate_src(src)
        with open(dest, 'w') as dest_file:
            Merger._merge_k_sorted_files(dest_file, Merger._initialize_min_heap(src))

    @staticmethod
    def _validate_src(src):
        if not os.path.isdir(src):
            raise IOError("'{}' does not exist or is not a directory")

    @staticmethod
    def _initialize_min_heap(src):
        min_heap = []
        for segment_file in (open(os.path.join(src, path)) for path in os.listdir(src)):
            heapq.heappush(min_heap, (segment_file.readline().rstrip(), segment_file))
        return min_heap

    @staticmethod
    def _merge_k_sorted_files(dest_file, min_heap):
        buffer = None

        while min_heap:
            line, file = heapq.heappop(min_heap)
            term, serialized_record = line.rstrip().split(';')
            record = inverted_index.TermRecord.deserialize(serialized_record)

            if buffer is None:
                buffer = Merger.Buffer(term, document_id_groups=[record.document_ids])
            elif buffer.term == term:
                buffer.document_id_groups.append(record.document_ids)
            else:
                Merger._write_buffer(dest_file, buffer)
                buffer = Merger.Buffer(term, document_id_groups=[record.document_ids])

            next_line = file.readline().rstrip()
            if next_line != '':
                heapq.heappush(min_heap, (next_line, file))
            else:
                file.close()

        if buffer is not None:
            Merger._write_buffer(dest_file, buffer)

    @staticmethod
    def _write_buffer(dest_file, buffer):
        def _merge_document_ids(a, b):
            if a[-1] <= b[0]:
                return a + b
            return b + a

        merged_document_ids = buffer.document_id_groups[0]
        for chunk in buffer.document_id_groups[1:]:
            merged_document_ids = _merge_document_ids(merged_document_ids, chunk)

        serialized_document_ids = [str(document_id) for document_id in merged_document_ids]
        dest_file.write('{};{}\n'.format(buffer.term, ','.join(serialized_document_ids)))


class FileSplitter:
    def __init__(self, dest, lookup_table_dest):
        fs.clean_up_file(lookup_table_dest)
        fs.clean_up_dir(dest)
        self.lookup_table_dest = lookup_table_dest
        self.path_generator = UniquePathGenerator(dest)

    def split(self, src, chunk_size):
        lines = []
        threshold = chunk_size

        with open(src, 'r') as source_file:
            while True:
                line = source_file.readline()
                if line == '':
                    self.flush(lines)
                    break

                lines.append(line)

                bytes_read = source_file.tell()
                if bytes_read >= threshold:
                    self.flush(lines)
                    threshold = bytes_read + chunk_size
                    lines = []

    def flush(self, lines):
        if not lines:
            return

        path = self.path_generator.generate()
        term, _ = lines[0].rstrip().split(';')

        with open(path, 'w') as segment_file:
            segment_file.writelines(line for line in lines)

        with open(self.lookup_table_dest, 'a') as lookup_table_file:
            lookup_table_file.write("{};{}\n".format(term, path))
