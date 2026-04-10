from django.shortcuts import render, get_object_or_404
from .models import Book, Category

# Create your views here.

#  Book List
def book_list(request):
    books = Book.objects.all()
    categories = Category.objects.filter(parent=None)

    return render(request, 'books/book_list.html', {
        'books': books,
        'categories': categories
    })


#  Book Detail
def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    related_books = Book.objects.filter(category=book.category).exclude(id=id)[:4]

    return render(request, 'books/book_detail.html', {
        'book': book,
        'related_books': related_books
    })


# Search + Filtering
def search(request):
    query = request.GET.get('q')
    author = request.GET.get('author')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    books = Book.objects.all()

    if query:
        books = books.filter(title__icontains=query)

    if author:
        books = books.filter(author__icontains=author)

    if min_price and max_price:
        books = books.filter(price__range=[min_price, max_price])

    return render(request, 'books/search.html', {'books': books})