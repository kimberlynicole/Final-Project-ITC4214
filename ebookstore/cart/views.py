from django.shortcuts import render, redirect, redirect, get_object_or_404
from books.models import Book
from .models import Cart, CartItem
from .forms import PaymentForm
from library.models import Library


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

        if str(id) not in cart:
            cart[str(id)] = {
                'title': book.title,
                'price': str(book.price)
            }

        request.session['cart'] = cart

    return redirect('cart:cart_detail')



def cart_detail(request):

    if request.user.is_authenticated:

        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all()

        total = sum(item.book.price for item in items)

        return render(request, 'cart/cart_detail.html', {
            'items': items,
            'total': total
        })

    else:
        return render(request, 'cart/cart_detail.html', {
            'items': [],
            'total': 0
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
    # FORCE LOGIN BEFORE ANYTHING
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()
    total = sum(item.book.price for item in items)

    form = PaymentForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():
            return redirect('cart:success')

    return render(request, 'cart/checkout.html', {
        'form': form,
        'items': items,
        'total': total
    })




def payment_simulation(request):

    # BLOCK GUEST USERS
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    cart = get_object_or_404(Cart, user=request.user)

    if request.method == "POST":

        form = PaymentForm(request.POST)

        if form.is_valid():

            # MOVE BOOKS TO LIBRARY
            for item in cart.items.all():
                Library.objects.get_or_create(
                    user=request.user,
                    book=item.book
                )

            # CLEAR CART
            cart.items.all().delete()

            return redirect('cart:success')

        else:
            return render(request, 'cart/checkout.html', {
                'form': form,
                'items': cart.items.all(),
                'total': sum(item.book.price for item in cart.items.all())
            })

    # GET request
    form = PaymentForm()

    return render(request, 'cart/checkout.html', {
        'form': form,
        'items': cart.items.all(),
        'total': sum(item.book.price for item in cart.items.all())
    })


def payment_success(request):
    return render(request, 'cart/success.html')