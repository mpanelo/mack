from mack import search
from mack import fs
import collections
import heapq
import os


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

    def write(self, inverted_index: search.DictionaryInvertedIndex):
        with open(self.path_generator.generate(), 'w') as file:
            for term in sorted(inverted_index.terms()):
                document_ids = [str(document_id) for document_id in inverted_index.get(term).document_ids]
                file.write("{};{}\n".format(term, ','.join(document_ids)))


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
            term, serialized_document_ids = line.split(';')

            if buffer is None:
                buffer = Merger.Buffer(term, document_id_groups=[Merger._deserialize(serialized_document_ids)])
            elif buffer.term == term:
                buffer.document_id_groups.append(Merger._deserialize(serialized_document_ids))
            else:
                Merger._write_buffer(dest_file, buffer)
                buffer = Merger.Buffer(term, document_id_groups=[Merger._deserialize(serialized_document_ids)])

            next_line = file.readline().rstrip()
            if next_line != '':
                heapq.heappush(min_heap, (next_line, file))
            else:
                file.close()

        if buffer is not None:
            Merger._write_buffer(dest_file, buffer)

    @staticmethod
    def _deserialize(document_ids):
        return [int(document_id) for document_id in document_ids.split(',')]

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
