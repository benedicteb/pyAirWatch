#!/usr/bin/env python
import os.path as op
import base64

class FileChunkIterator:
    def __init__(self, path_to_file, chunk_size=1024):
        self.total_application_size = op.getsize(path_to_file) # [bytes]
        self.file_object = open(path_to_file, 'r')
        self.chunk_sequence_number = 1
        self.transaction_id = None
        self.chunk_size = chunk_size # [bytes]

    def __iter__(self):
        return self

    def set_transaction_id(self, transaction_id):
        self.transaction_id = transaction_id

    def next(self):
        out_object = {
            'ChunkSequenceNumber': self.chunk_sequence_number,
            'TotalApplicationSize': self.total_application_size
        }

        if self.transaction_id:
            out_object['TransactionId'] = self.transaction_id

        self.chunk_sequence_number += 1

        next_chunk = self.file_object.read(self.chunk_size)

        if next_chunk == '':
            self.file_object.close()
            raise StopIteration
        else:
            out_object['ChunkData'] = base64.b64encode(next_chunk)
            return out_object
