from django.shortcuts import render, get_object_or_404, redirect

from .models import Book, Category, Wishlist

# Create your views here.

def index(request):
    highlights = Book.objects.all().order_by('-id')[:6]
    all_books = Book.objects.all()

    return render(request, 'books/index.html', {
        'highlights': highlights,
        'books': all_books
    })


def books_view(request):
    books = Book.objects.all()
    main_categories = Category.objects.filter(parent=None)

    category_id = request.GET.get('category')

    if category_id:
        books = books.filter(category_id=category_id)

    return render(request, 'books/books.html', {
        'books': books,
        'main_categories': main_categories
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

#Wishlist
def wishlist_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    wishlist_items = Wishlist.objects.filter(user=request.user)

    return render(request, 'books/wishlist.html', {
        'wishlist_items': wishlist_items
    })

def add_to_wishlist(request, book_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    book = Book.objects.get(id=book_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        book=book
    )

    return redirect('book_detail', id=book_id)

def remove_from_wishlist(request, book_id):
    if not request.user.is_authenticated:
        return redirect('login')

    Wishlist.objects.filter(
        user=request.user,
        book_id=book_id
    ).delete()

    return redirect('wishlist')

