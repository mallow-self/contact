from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

file_name = "test_upload.txt"
content = ContentFile(b"Hello, GCS!")
file_path = default_storage.save(file_name, content)

print(f"File uploaded to: {file_path}")
