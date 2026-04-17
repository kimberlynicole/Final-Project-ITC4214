from django.db import models
from django.contrib.auth.models import User
from books.models import Book

class Library(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='library')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='owned_by')
    purchased_at = models.DateTimeField(auto_now_add=True)
    progress = models.PositiveIntegerField(default=0)
    last_page = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"