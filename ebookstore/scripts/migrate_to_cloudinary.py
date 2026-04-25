import os
from books.models import Book
import cloudinary.uploader

for b in Book.objects.all():

    # =========================
    # IMAGE UPLOAD
    # =========================
    if b.cover:

        file_path = b.cover.path

        if os.path.exists(file_path):
            try:
                print(f"Uploading image: {b.title}")

                result = cloudinary.uploader.upload(file_path)

                b.cover = result["secure_url"]
                b.save()

                print(f" Image done: {b.title}")

            except Exception as e:
                print(f"Image failed {b.title}: {e}")

        else:
            print(f" Missing image: {b.title}")


    # =========================
    # PDF UPLOAD (THIS IS THE PART YOU ASKED)
    # =========================
    if b.pdf_file:

        pdf_path = b.pdf_file.path

        if os.path.exists(pdf_path):
            try:
                print(f"Uploading PDF: {b.title}")

                result = cloudinary.uploader.upload(
                    pdf_path,
                    resource_type="raw"   # REQUIRED FOR PDFs
                )

                b.pdf_file = result["secure_url"]
                b.save()

                print(f" PDF done: {b.title}")

            except Exception as e:
                print(f" PDF failed {b.title}: {e}")

        else:
            print(f" Missing PDF: {b.title}")