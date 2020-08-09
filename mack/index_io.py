from mack import search
import collections
import heapq
import os
import shutil


class SegmentGenerator:
    def __init__(self, root):
        SegmentGenerator._clean_root(root)
        self.root = root
        self.counter = 0
        self.segment_paths = []

    @staticmethod
    def _clean_root(root):
        if os.path.exists(root):
            if os.path.isdir(root):
                shutil.rmtree(root)
            else:
                os.remove(root)
        os.mkdir(root)

    def generate_path(self):
        path = os.path.join(self.root, "segment_{:03d}.index".format(self.counter))
        self.segment_paths.append(path)
        self.counter += 1
        return path

    def get_generated_segment_paths(self):
        return self.segment_paths


class Writer:
    def __init__(self, index_segment_generator: SegmentGenerator):
        self.index_segment_generator = index_segment_generator

    def write(self, inverted_index: search.DictionaryInvertedIndex):
        segment_path = self.index_segment_generator.generate_path()

        with open(segment_path, 'w') as file:
            for term in sorted(inverted_index.terms()):
                document_ids = [str(document_id) for document_id in inverted_index.get(term).document_ids]
                file.write("{};{}\n".format(term, ','.join(document_ids)))


class Merger:
    Buffer = collections.namedtuple('Buffer', 'term document_id_groups')

    def __init__(self, destination):
        self.output_file = open(destination, 'w')

    def merge(self, segment_paths):
        def get_segment_files():
            for segment_path in segment_paths:
                yield open(segment_path, 'r')

        def deserialize_document_ids(document_ids):
            return [int(document_id) for document_id in document_ids.split(',')]

        min_heap = []
        for segment_file in get_segment_files():
            heapq.heappush(min_heap, (segment_file.readline().rstrip(), segment_file))

        buffer = None
        while min_heap:
            line, file = heapq.heappop(min_heap)
            term, serialized_document_ids = line.split(';')

            if buffer is None:
                buffer = Merger.Buffer(term, document_id_groups=[deserialize_document_ids(serialized_document_ids)])
            elif buffer.term == term:
                buffer.document_id_groups.append(deserialize_document_ids(serialized_document_ids))
            else:
                self._write_buffer(buffer)
                buffer = Merger.Buffer(term, document_id_groups=[deserialize_document_ids(serialized_document_ids)])

            next_line = file.readline().rstrip()
            if next_line != '':
                heapq.heappush(min_heap, (next_line, file))

        if buffer is not None:
            self._write_buffer(buffer)
        self.output_file.close()

    def _write_buffer(self, buffer):
        def _merge_document_ids(a, b):
            if a[-1] <= b[0]:
                return a + b
            return b + a

        merged_document_ids = buffer.document_id_groups[0]
        for chunk in buffer.document_id_groups[1:]:
            merged_document_ids = _merge_document_ids(merged_document_ids, chunk)

        serialized_document_ids = [str(document_id) for document_id in merged_document_ids]
        self.output_file.write('{};{}\n'.format(buffer.term, ','.join(serialized_document_ids)))
