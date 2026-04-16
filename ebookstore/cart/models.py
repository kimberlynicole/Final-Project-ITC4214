from django.db import models
from django.contrib.auth.models import User
from books.models import Book

# Create your models here.

# CART (1 per user)
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"


# CART ITEMS (books inside cart)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name='cart_items')
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.quantity * self.book.price

    def __str__(self):
        return f"{self.book.title} x {self.quantity}"
    
    class Meta:
        unique_together = ('cart', 'book')