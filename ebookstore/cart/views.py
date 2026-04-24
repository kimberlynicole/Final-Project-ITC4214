from django.shortcuts import render, redirect, get_object_or_404
from books.models import Book
from .models import Cart, CartItem
from .forms import PaymentForm
from library.models import Library
from orders.models import Order, OrderItem
from django.contrib import messages


# Create your views here.
def add_to_cart(request, id):
    book = Book.objects.get(id=id)

    if request.user.is_authenticated:

        cart, created = Cart.objects.get_or_create(user=request.user)

        CartItem.objects.get_or_create(
            cart=cart,
            book=book
        )
    else:
            cart = request.session.get('cart', {})
            book_id = str(id)

            cart[book_id] = book_id   

            request.session['cart'] = cart
            request.session.modified = True

    return redirect('cart:cart_detail')



def cart_detail(request):

    # =========================
    # LOGGED IN USER
    # =========================
    if request.user.is_authenticated:

        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all()

        total = sum(item.book.price for item in items)

        normalized_items = []

        for item in items:
            normalized_items.append({
                "id": item.book.id,
                "title": item.book.title,
                "author": item.book.author,
                "price": item.book.price,
                "cover": item.book.cover
            })

        return render(request, 'cart/cart_detail.html', {
            'items': normalized_items,
            'total': total
        })

    # =========================
    # GUEST USER
    # =========================
    else:

        session_cart = request.session.get('cart', {})

        normalized_items = []
        total = 0

        for book_id in session_cart.keys():
            book = Book.objects.get(id=book_id)

            normalized_items.append({
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "price": book.price,
                "cover": book.cover
            })

            total += book.price

        return render(request, 'cart/cart_detail.html', {
            'items': normalized_items,
            'total': total
        })
    

def remove_from_cart(request, id):

    # LOGGED-IN USER
    if request.user.is_authenticated:

        cart = Cart.objects.get(user=request.user)
        CartItem.objects.filter(cart=cart, book_id=id).delete()

    # GUEST USER
    else:
        cart = request.session.get('cart', {})

        if str(id) in cart:
            del cart[str(id)]

        request.session['cart'] = cart

    return redirect('cart:cart_detail')

def clear_cart(request):

    if request.user.is_authenticated:

        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()

    else:
        request.session['cart'] = {}

    return redirect('cart:cart_detail')



def checkout(request):

    if not request.user.is_authenticated:
        return redirect('accounts:login')

    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()
    total = sum(item.book.price for item in items)

    form = PaymentForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            # CREATE ORDER
            order = Order.objects.create(
                user=request.user,
                total_price=total
            )

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    quantity=1,
                    price=item.book.price
                )

                Library.objects.get_or_create(
                    user=request.user,
                    book=item.book
                )

            cart.items.all().delete()

            messages.success(request, "Payment successful!")
            return redirect('cart:success')

        else:
            messages.error(request, "Please fix the errors below.")

    return render(request, 'cart/checkout.html', {
        'form': form,
        'items': items,
        'total': total
    })



def payment_simulation(request):

    if not request.user.is_authenticated:
        return redirect('accounts:login')

    cart = get_object_or_404(Cart, user=request.user)

    if request.method == "POST":

        form = PaymentForm(request.POST)

        if form.is_valid():

            # CALCULATE TOTAL
            total = sum(item.book.price for item in cart.items.all())

            # CREATE ORDER
            order = Order.objects.create(
                user=request.user,
                total_price=total
            )

            # LOOP ITEMS
            for item in cart.items.all():

                OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    quantity=1,
                    price=item.book.price
                )

                # ADD TO LIBRARY
                Library.objects.get_or_create(
                    user=request.user,
                    book=item.book
                )

            # CLEAR CART
            cart.items.all().delete()

            # SUCCESS MESSAGE
            messages.success(request, "Payment successful! Books added to your library.")

            return redirect('cart:success')

        else:
            messages.error(request, "Payment failed. Please fix the form.")

    return redirect('cart:checkout')




def payment_success(request):
    return render(request, 'cart/success.html')