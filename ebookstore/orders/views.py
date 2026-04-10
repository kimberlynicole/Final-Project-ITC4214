from django.shortcuts import render, redirect
from cart.models import Cart, CartItem
from books.models import Book

# Create your views here.
def checkout(request):

    # ❗ If NOT logged in → redirect to login
    if not request.user.is_authenticated:
        return redirect('/login/?next=/orders/checkout/')

    # 🧠 Move session cart → DB cart after login
    session_cart = request.session.get('cart')

    if session_cart:
        cart, created = Cart.objects.get_or_create(user=request.user)

        for key, item in session_cart.items():
            book = Book.objects.get(id=key)

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                book=book
            )

            if not created:
                cart_item.quantity += item['quantity']
                cart_item.save()

        # 🧹 Clear session cart
        del request.session['cart']

    # 📦 Now use DB cart
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()

    total = sum(i.quantity * i.book.price for i in items)

    return render(request, 'orders/checkout.html', {
        'items': items,
        'total': total
    })

from .models import Order, OrderItem

def place_order(request):

    if not request.user.is_authenticated:
        return redirect('login')

    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()

    total = sum(i.quantity * i.book.price for i in items)

    # 🧾 Create Order
    order = Order.objects.create(
        user=request.user,
        total_price=total
    )

    # 📦 Create Order Items
    for item in items:
        OrderItem.objects.create(
            order=order,
            book=item.book,
            quantity=item.quantity,
            price=item.book.price
        )

    # 🧹 Clear Cart after purchase
    cart.items.all().delete()

    return redirect('order_success')

def order_success(request):
    return render(request, 'orders/success.html')