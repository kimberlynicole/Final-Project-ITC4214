from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,related_name='subcategories' )

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    pages = models.IntegerField()
    language = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='books' )
    cover = CloudinaryField('image')
    pdf_file = CloudinaryField('file')
    published_date = models.DateField()

    def __str__(self):
        return f"{self.title} by {self.author}"
    
     # To calculate the average ratings
    def average_rating(self):
        ratings = self.ratings.all()

        if ratings.exists():
            return sum(r.stars for r in ratings) / ratings.count()
        return 0

    def star_display(self):
        avg = self.average_rating()
        full = int(avg)

        if avg - full >= 0.5:
            half = 1
        else:
            half = 0

        empty = 5 - full - half

        return {
            'full': range(full),
            'half': half,
            'empty': range(empty),
            'avg': round(avg, 1)
        }

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='wishlist_items' )
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')  # prevent duplicates

    def __str__(self):
        return f"{self.user} - {self.book}"




class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='ratings_given')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    stars = models.IntegerField()  # 1 to 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')  # prevent duplicate ratings

    def __str__(self):
        return f"{self.book} - {self.stars}⭐️"