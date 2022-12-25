File Chunker

```python
if __name__ == "__main__":
    generate_random_file()
    key = base64.urlsafe_b64encode(hashlib.sha256(b"password").digest())
  
    encrypt("random.txt", key)
    decrypt("random.txt", key)
```
