from django.shortcuts import render, redirect
from .models import Library


# Create your views here.

def my_library(request):
    if not request.user.is_authenticated:
        return redirect('login')

    books = Library.objects.filter(user=request.user)

    return render(request, 'books/library.html', {
        'books': books
    })


from books.models import Book

def add_to_library(request, book_id):
    if not request.user.is_authenticated:
        return redirect('login')

    book = Book.objects.get(id=book_id)

    Library.objects.get_or_create(
        user=request.user,
        book=book
    )

    return redirect('library')