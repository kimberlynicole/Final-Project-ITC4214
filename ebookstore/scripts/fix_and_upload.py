import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ebookstore.settings")
django.setup()

from books.models import Book
from django.conf import settings

MEDIA_ROOT = settings.MEDIA_ROOT

def find_file(filename):
    """
    Try to find a matching file inside media/books/
    even if the name is slightly wrong
    """
    books_dir = os.path.join(MEDIA_ROOT, "books")

    if not os.path.exists(books_dir):
        return None

    for f in os.listdir(books_dir):
        if filename.lower().split('.')[0] in f.lower():
            return os.path.join(books_dir, f)

    return None


for book in Book.objects.all():

    if not book.cover:
        continue

    db_path = book.cover.name  # e.g. books/wutheirng.png
    filename = os.path.basename(db_path)

    correct_path = os.path.join(MEDIA_ROOT, db_path)

    #  file exists → upload normally
    if os.path.exists(correct_path):
        print(f"OK: {book.title}")

        with open(correct_path, "rb") as f:
            book.cover.save(filename, f, save=True)

    
    else:
        print(f" Fixing: {book.title} → {filename}")

        found = find_file(filename)

        if found:
            print(f"   ✔ Found match: {found}")

            with open(found, "rb") as f:
                new_name = os.path.basename(found)
                book.cover.save(new_name, f, save=True)

        else:
            print(f"  Still missing: {filename}")