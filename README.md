File Chunker

```python
if __name__ == "__main__":
    generate_random_file()
    key = base64.urlsafe_b64encode(hashlib.sha256(b"password").digest())
  
    encrypt("random.txt", key)
    chunker = Chunker("random.txt", 5)

    chunker.produce_chunks()
    chunker.hash_file()

    chunker.ensure_secure_chunking()
```
