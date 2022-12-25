import uuid
import os
import hashlib


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
        _hash = hashlib.sha1()
        with open(self.file_name, "rb") as file:

            chunk = 0
            while chunk != b"":
                chunk = file.read(1024)
                _hash.update(chunk)

        with open(f"{self.primary_uuid}_hashfile.hash", "wb") as hash_file:
            hash_file.write(bytes(_hash.hexdigest(), "utf-8"))


if __name__ == "__main__":

    chunker = Chunker("random.txt", 5)
    chunker.produce_chunks()
    chunker.hash_file()
    chunker.ensure_secure_chunking()
