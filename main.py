import random
import string
import uuid
import math
import os
import os, fnmatch
import hashlib


def generate_random_file():
    with open("random.txt", "wb") as f:
        f.write("".join(random.randbytes(8) for _ in range(1000000)))


class Chunker:
    def __init__(self, file_name, size) -> None:
        self.file_name = file_name
        self.size = size
        self.primary_uuid = uuid.uuid4()

    def chunks(self):
        _size = os.stat(self.file_name).st_size // self.size
        with open(self.file_name) as f:
            while content := f.read(_size):
                yield content

    def produce_chunks(self):
        split_files = self.chunks()
        count = 0
        for chunk in split_files:
            with open(f"{self.primary_uuid}_chunk_{uuid.uuid4()}_{count}", "wb") as f:
                count += 1
                f.write(bytes(chunk, "utf-8"))

    def hash_file(self):
        """ "This function returns the SHA-1 hash
        of the file passed into it"""

        # make a hash object
        _hash = hashlib.sha1()
        # open file for reading in binary mode
        with open(self.file_name, "rb") as file:

            # loop till the end of the file
            chunk = 0
            while chunk != b"":
                # read only 1024 bytes at a time
                chunk = file.read(1024)
                _hash.update(chunk)

        # return the hex representation of digest
        with open(f"{self.primary_uuid}_hashfile.hash", "wb") as hash_file:
            hash_file.write(bytes(_hash.hexdigest(), "utf-8"))

    def find(self, pattern, path):
        result = []
        for root, dirs, files in os.walk(path):
            result.extend(
                os.path.join(root, name)
                for name in files
                if fnmatch.fnmatch(name, pattern)
            )
        return result

    def reconstruct_file(self):
        chunks = self.find(f"{self.primary_uuid}_chunk*", os.getcwd())
        with open(f"{self.primary_uuid}_reconstructed.txt", "wb") as reconstructed:
            for chunk in chunks:
                with open(chunk, "rb") as f:
                    reconstructed.write(f.read())

    def ensure_secure_chunking(self):
        # use the hash file to ensure that the chunks match the original file hash
        with open(f"{self.primary_uuid}_hashfile.hash", "rb") as hash_file:
            hash_content = hash_file.read()

        hash_content = bytes(hash_content).decode("utf-8")

        with open(f"{self.primary_uuid}_chunk_{uuid.uuid4()}", "rb") as chunk:
            chunk_content = chunk.read()

        chunk_content = bytes(chunk_content).decode("utf-8")

        if hash_content != chunk_content:
            return False
        return True


if __name__ == "__main__":

    chunker = Chunker("random.txt", 5)
    chunker.produce_chunks()
    chunker.hash_file()
    chunker.ensure_secure_chunking()
