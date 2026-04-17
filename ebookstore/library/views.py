from django.shortcuts import render, redirect, get_object_or_404
from .models import Library
from books.models import Book
from django.http import JsonResponse
import json


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


def read_book(request, book_id):

    if not request.user.is_authenticated:
        return redirect('accounts:login')

    lib = Library.objects.get(user=request.user, book_id=book_id)
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




def update_progress(request, book_id):

    if not request.user.is_authenticated:
        return JsonResponse({"error": "not logged in"}, status=403)

    if request.method != "POST":
        return JsonResponse({"error": "invalid method"}, status=400)

    data = json.loads(request.body)
    page = data.get("page", 1)
    total = data.get("total", 1)

    lib = get_object_or_404(Library, user=request.user, book_id=book_id)
    # 👇 DEBUG LINES GO HERE
    print("PAGE:", page)
    print("TOTAL:", total)
    
    lib.last_page = page
    lib.progress = int((page / total) * 100)
    print("PROGRESS:", lib.progress)
    lib.save()

    return JsonResponse({"success": True, "progress": lib.progress})