import cloudinary.uploader
from books.models import Book
import os

for b in Book.objects.all():

    if b.pdf_file and hasattr(b.pdf_file, "path"):

        path = b.pdf_file.path

        if os.path.exists(path):

            result = cloudinary.uploader.upload(
                path,
                resource_type="raw"
            )

            b.pdf_file = result["secure_url"]
            b.save()

            print("FIXED:", b.title)

        else:
            print("MISSING LOCAL FILE:", b.title)