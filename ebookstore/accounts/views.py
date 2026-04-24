from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import RegisterForm, LoginForm
from .models import Profile

from books.models import Book, Category
from orders.models import Order
from accounts.forms import BookForm
from .forms import ProfileForm, UserForm


# =========================
# HELPERS 
# =========================

def get_all_subcategories(category):
    all_ids = [category.id]
    children = category.subcategories.all()

    for child in children:
        all_ids += get_all_subcategories(child)

    return all_ids


def get_allowed_category_ids(role):

    if role == "fiction_employee":
        try:
            root = Category.objects.get(name="Fiction")
            return get_all_subcategories(root)
        except:
            return []

    elif role == "nonfiction_employee":
        try:
            root = Category.objects.get(name="Non-Fiction")
            return get_all_subcategories(root)
        except:
            return []
    return []


def get_role(user):
    if not user.is_authenticated:
        return "customer"

    profile, _ = Profile.objects.get_or_create(user=user)
    return getattr(profile, "role", "customer")


# =========================
# REGISTER 
# =========================
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )

            Profile.objects.get_or_create(user=user)

            login(request, user)
            messages.success(request, "Account created successfully")

            if user.is_staff:
                return redirect('accounts:dashboard')
            else:
                return redirect('books:index')

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {
        'form': form,
        "page": "register"
    })


# =========================
# LOGIN 
# =========================
def user_login(request):

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if user:
                login(request, user)

                # SUPERUSER → Django admin ALWAYS FIRST
                if user.is_superuser:
                    return redirect('/admin/')

                # NEXT URL SAFETY CHECK
                next_url = request.GET.get('next')

                # Only allow safe next redirects (NOT dashboard bypass)
                if next_url and "dashboard" not in next_url:
                    return redirect(next_url)

                # ROLE-BASED REDIRECT
                if user.is_staff:
                    return redirect('accounts:dashboard')

                return redirect('books:index')
            else:
                messages.error(request, "Invalid username or password")

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {
        'form': form,
        "page": "login"
    })


# =========================
# LOGOUT 
# =========================
def user_logout(request):
    logout(request)
    return redirect('accounts:login')


# =========================
# DASHBOARD 
# =========================
def dashboard(request):

    if not request.user.is_authenticated:
        return redirect('accounts:login')

    profile, _ = Profile.objects.get_or_create(user=request.user)
    role = get_role(request.user)

    # USER DASHBOARD
    if not request.user.is_staff:

        user_orders = Order.objects.filter(user=request.user)

        return render(request, 'accounts/dashboard.html', {
            'role': 'user',
            'profile': profile,
            'user_orders': user_orders,
        })

 
    # EMPLOYEE DASHBOARD

    total_books = Book.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()

    # -------- BOOK FILTER (ROLE BASED) --------
    if role == "fiction_employee":
        root = Category.objects.get(name="Fiction")
        allowed_ids = get_all_subcategories(root)
        books = Book.objects.filter(category_id__in=allowed_ids)

    elif role == "nonfiction_employee":
        root = Category.objects.get(name="Non-Fiction")
        allowed_ids = get_all_subcategories(root)
        books = Book.objects.filter(category_id__in=allowed_ids)

    else:
        books = Book.objects.none()

    orders = Order.objects.all().order_by('created_at')

    labels = []
    values = []

    for order in orders:
        labels.append(str(order.created_at.date()))
        values.append(float(order.total_price))

    total_revenue = sum(values)

    # TOP BOOKS
    top_books = []
    for book in Book.objects.all():
        sold = 0
        for item in book.order_items.all():
            sold += item.quantity

        top_books.append({
            "title": book.title,
            "sold": sold
        })

    # RECENT DATA
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    for order in recent_orders:
        first_item = order.items.first()
        order.book = first_item.book if first_item else None

    recent_users = User.objects.all().order_by('-date_joined')[:5]

    return render(request, 'accounts/dashboard.html', {
        'role': 'admin',
        'profile': profile,
        'total_books': total_books,
        'total_orders': total_orders,
        'total_users': total_users,
        'total_revenue': total_revenue,
        'top_books': top_books,
        'recent_orders': recent_orders,
        'recent_users': recent_users,
        'books': books,
        'labels': labels,
        'values': values,
    })


# =========================
# ADMIN BOOKS 
# =========================
def admin_books(request):

    if not request.user.is_staff:
        return redirect('accounts:dashboard')

    role = get_role(request.user)

    allowed_ids = get_allowed_category_ids(role)

    books = Book.objects.filter(category_id__in=allowed_ids)
    categories = Category.objects.filter(id__in=allowed_ids)

    selected_category = request.GET.get('category')

    if selected_category:
        category = Category.objects.get(id=selected_category)
        all_ids = get_all_subcategories(category)
        books = books.filter(category_id__in=all_ids)

    return render(request, 'accounts/admin_books.html', {
        'books': books,
        'categories': categories,
        'selected_category': selected_category
    })


# =========================
# ADD BOOK
# =========================
def add_book(request):

    if not request.user.is_staff:
        return redirect('accounts:dashboard')

    role = get_role(request.user)
    allowed_ids = get_allowed_category_ids(role)

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            book = form.save(commit=False)

            if book.category.id not in allowed_ids:
                messages.error(request, "Not allowed.")
                return redirect('accounts:admin_books')

            book.save()
            return redirect('accounts:admin_books')

    else:
        form = BookForm()

    return render(request, "accounts/add_book.html", {"form": form})


# =========================
# EDIT BOOK
# =========================
def edit_book(request, book_id):

    if not request.user.is_staff:
        return redirect('accounts:dashboard')

    role = get_role(request.user)
    allowed_ids = get_allowed_category_ids(role)

    book = get_object_or_404(Book, id=book_id)

    if book.category.id not in allowed_ids:
        return redirect('accounts:admin_books')

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)

        if form.is_valid():
            updated = form.save(commit=False)

            if updated.category.id not in allowed_ids:
                return redirect('accounts:admin_books')

            updated.save()
            return redirect('accounts:admin_books')

    else:
        form = BookForm(instance=book)

    return render(request, "accounts/edit_book.html", {"form": form})


# =========================
# DELETE BOOK
# =========================
def delete_book(request, book_id):

    if not request.user.is_staff:
        return redirect('accounts:dashboard')

    role = get_role(request.user)
    allowed_ids = get_allowed_category_ids(role)

    book = get_object_or_404(Book, id=book_id)

    if book.category.id not in allowed_ids:
        return redirect('accounts:admin_books')

    book.delete()
    return redirect('accounts:admin_books')


# =========================
# PROFILE
# =========================
def edit_profile(request):

    if not request.user.is_authenticated:
        return redirect('accounts:login')

    profile = request.user.profile

    if request.method == "POST":

        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:dashboard')

    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, "accounts/edit_profile.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })