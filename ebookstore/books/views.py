from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Category, Wishlist, Rating
from django.db.models import Sum, Avg
from .forms import RatingForm

# ============================================================
# HOME PAGE (SECTIONS)
# ============================================================

def index(request):

    # NEW BOOKS (recently added)
    new_books = Book.objects.all().order_by('-id')[:5]


    # BEST SELLERS (based on purchases)
    best_sellers = Book.objects.annotate(
        total_sold=Sum('orderitem__quantity')
        ).order_by('-total_sold')[:5]


    # TRENDING (based on ratings)
    trending = Book.objects.annotate(
        avg_rating=Avg('ratings__stars')
    ).order_by('-avg_rating')[:5]


    return render(request, 'books/index.html', {
        'new_books': new_books,
        'best_sellers': best_sellers,
        'trending': trending,
    })


# ============================================================
# ALL BOOKS PAGE
# ============================================================

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


# ============================================================
# BOOK DETAIL
# ============================================================


def book_detail(request, id):

    book = get_object_or_404(Book, id=id)
    related_books = Book.objects.filter(category=book.category).exclude(id=id)[:4]
    reviews = book.ratings.select_related('user').order_by('-created_at')
    # 🔁 SIMILAR BOOKS (same category)
    similar_books = Book.objects.filter(
        category=book.category
    ).exclude(id=book.id)[:6]

    form = RatingForm()

    return render(request, 'books/book_detail.html', {
        'book': book,
        'related_books': related_books,
        'reviews': reviews,
        'form': form,
        'similar_books': similar_books
    })

# ========================================================================
#                       RATING
# =======================================================================

def add_rating(request, book_id):

    if not request.user.is_authenticated:
        return redirect('accounts:login')

    book = get_object_or_404(Book, id=book_id)
    stars = int(request.POST.get('stars'))

    Rating.objects.update_or_create(
        user=request.user,
        book=book,
        defaults={'stars': stars}
    )

    return redirect('books:book_detail', id=book_id)

#===============================================================================
#                               Review
#===============================================================================

def add_review(request, book_id):

    if not request.user.is_authenticated:
        return redirect('accounts:login')

    book = get_object_or_404(Book, id=book_id)

    form = RatingForm(request.POST)

    if form.is_valid():

        Rating.objects.update_or_create(
            user=request.user,
            book=book,
            defaults={
                'stars': form.cleaned_data['stars'],
                'comment': form.cleaned_data['comment']
            }
        )
    return redirect('books:book_detail', id=book_id)



# ============================================================
# SEARCH
# ============================================================

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


# ============================================================
# WISHLIST
# ============================================================

def wishlist_view(request):

    if not request.user.is_authenticated:
        return redirect('accounts:login')

    
    wishlist_items = request.user.wishlist_items.all()

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

    return redirect('books:book_detail', id=book_id)


def remove_from_wishlist(request, book_id):

    if not request.user.is_authenticated:
        return redirect('accounts:login')

    Wishlist.objects.filter(
        user=request.user,
        book_id=book_id
    ).delete()

    return redirect('books:wishlist')


