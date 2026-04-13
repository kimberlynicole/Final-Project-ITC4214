from django.db import models
from django.contrib.auth.models import User
from books.models import Book

# Create your models here.
class Library(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')  # no duplicate purchases

    def __str__(self):
        return f"{self.user} - {self.book}"