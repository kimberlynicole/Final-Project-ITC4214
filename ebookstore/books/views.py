from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Avg, Q
from django.http import JsonResponse
from .models import Book, Category, Wishlist, Rating
from .forms import RatingForm
from library.models import Library



# ============================================================
# HOME PAGE (SECTIONS)
# ============================================================

def index(request):

    # NEW BOOKS (recently added)
    new_books = Book.objects.all().order_by('-id')[:5]


    # BEST SELLERS (based on purchases)
    best_sellers = Book.objects.annotate(
        total_sold=Sum('order_items__quantity')
    ).filter(total_sold__gt=0).order_by('-total_sold')[:5]


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
    category_id = request.GET.get('category')

    selected_category = None

    if category_id:
        selected_category = Category.objects.filter(id=category_id).first()
        books = books.filter(category_id=category_id)

    main_categories = Category.objects.filter(parent=None).prefetch_related('subcategories')

    return render(request, 'books/books.html', {
        'books': books,
        'main_categories': main_categories,
        'selected_category': selected_category
    })


# ============================================================
# BOOK DETAIL
# ============================================================


def book_detail(request, id):

    book = get_object_or_404(Book, id=id)
    related_books = Book.objects.filter(category=book.category).exclude(id=id)[:4]
    reviews = book.ratings.select_related('user').order_by('-created_at')
    similar_books = Book.objects.filter(category=book.category).exclude(id=book.id)[:6]

    form = RatingForm()

    item_exists = False

    if request.user.is_authenticated:
        item_exists = Library.objects.filter(
            user=request.user,
            book=book
        ).exists()

    
    is_wishlisted = False
    if request.user.is_authenticated:
        is_wishlisted = Wishlist.objects.filter(
            user=request.user,
            book=book
        ).exists()

    return render(request, 'books/book_detail.html', {
        'book': book,
        'related_books': related_books,
        'reviews': reviews,
        'form': form,
        'similar_books': similar_books,
        'item_exists': item_exists,
        'is_wishlisted': is_wishlisted,
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
#                           SEARCH
# ============================================================


def search(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    books = Book.objects.all()

    # Search by title OR author
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )

    # Filter by category
    if category:
        books = books.filter(category_id=category)

    #  Filter by price range
    if min_price:
        books = books.filter(price__gte=min_price)

    if max_price:
        books = books.filter(price__lte=max_price)

    return render(request, 'books/search.html', {
        'books': books,
        'categories': Category.objects.all()
    })


# ============================================================
#                               WISHLIST
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



def toggle_wishlist(request, book_id):

    if not request.user.is_authenticated:
        return JsonResponse({"error": "not logged in"}, status=403)

    book = Book.objects.get(id=book_id)

    obj, created = Wishlist.objects.get_or_create(
        user=request.user,
        book=book
    )

    # if already existed → remove it
    if not created:
        obj.delete()
        return JsonResponse({"status": "removed"})

    return JsonResponse({"status": "added"})

