from django.shortcuts import render, redirect
from books.models import Book
from .models import Cart, CartItem

# Create your views here.
def add_to_cart(request, id):
    book = Book.objects.get(id=id)

    # 👤 LOGGED-IN USER → DATABASE CART
    if request.user.is_authenticated:

        cart, created = Cart.objects.get_or_create(user=request.user)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            book=book
        )

        if not created:
            item.quantity += 1
            item.save()

    # 👤 GUEST USER → SESSION CART
    else:
        cart = request.session.get('cart', {})

        if str(id) in cart:
            cart[str(id)]['quantity'] += 1
        else:
            cart[str(id)] = {
                'title': book.title,
                'price': str(book.price),
                'quantity': 1
            }

        request.session['cart'] = cart

    return redirect('cart_detail')

def cart_detail(request):

    # 👤 LOGGED-IN USER
    if request.user.is_authenticated:

        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all()

        total = sum(item.quantity * item.book.price for item in items)

        return render(request, 'cart/cart_detail.html', {
            'items': items,
            'total': total
        })

    # 👤 GUEST USER
    else:
        session_cart = request.session.get('cart', {})

        total = 0
        for item in session_cart.values():
            total += float(item['price']) * item['quantity']

        return render(request, 'cart/cart_detail.html', {
            'session_cart': session_cart,
            'total': total
        })
    

def remove_from_cart(request, id):

    # 👤 LOGGED-IN USER
    if request.user.is_authenticated:

        cart = Cart.objects.get(user=request.user)
        CartItem.objects.filter(cart=cart, book_id=id).delete()

    # 👤 GUEST USER
    else:
        cart = request.session.get('cart', {})

        if str(id) in cart:
            del cart[str(id)]

        request.session['cart'] = cart

    return redirect('cart_detail')

def clear_cart(request):

    if request.user.is_authenticated:

        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()

    else:
        request.session['cart'] = {}

    return redirect('cart_detail')