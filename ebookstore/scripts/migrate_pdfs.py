import os
from books.models import Book
import cloudinary.uploader

for b in Book.objects.all():

    if not b.pdf_file:
        continue

    # skip already migrated files
    if str(b.pdf_file).startswith("http"):
        print("Already migrated:", b.title)
        continue

    try:
        print("Uploading:", b.title)

        file_path = b.pdf_file.path

        with open(file_path, "rb") as f:
            result = cloudinary.uploader.upload(
                f,
                resource_type="raw"
            )

        b.pdf_file = result["secure_url"]
        b.save()

        print("Done:", b.title)

    except Exception as e:
        print("FAILED:", b.title, e)