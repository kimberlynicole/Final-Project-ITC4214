from django.shortcuts import render, redirect, get_object_or_404
from .models import Library
from books.models import Book

# =========================
# MY LIBRARY
# =========================
def my_library(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    books = Library.objects.filter(user=request.user)
    return render(request, 'library/my_library.html', {
        'books': books
    })

def add_to_library(request, book_id):

    if not request.user.is_authenticated:
        return redirect('accounts:login')

    book = get_object_or_404(Book, id=book_id)
    # CHECK FIRST
    exists = Library.objects.filter(user=request.user, book=book).exists()
    if exists:
        return redirect('library:my_library')  # already owned

    # CREATE ONLY IF NOT EXISTS
    Library.objects.create(user=request.user, book=book)

    return redirect('library:my_library')



def remove_from_library(request, book_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    Library.objects.filter(
        user=request.user,
        book_id=book_id
    ).delete()

    return redirect('library:my_library')



def read_book(request, book_id):

    if not request.user.is_authenticated:
        return redirect('accounts:login')
    lib = get_object_or_404(Library, user=request.user, book_id=book_id)
    book = get_object_or_404(Book, id=book_id)
    total_pages = book.pages if book.pages > 0 else 1
    page = int(request.GET.get("page", lib.last_page or 1))

    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    # UPDATE PROGRESS
    lib.last_page = page
    lib.progress = int((page / total_pages) * 100)
    lib.save()

    return render(request, 'library/read_book.html', {
        'book': book,
        'page': page,
        'total_pages': total_pages,
        'progress': lib.progress
    })




