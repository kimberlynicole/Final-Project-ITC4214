from django.urls import path
from . import views

app_name = 'books'
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.books_view, name='books'),
    path('<int:id>/', views.book_detail, name='book_detail'),
    path('search/', views.search, name='search'),

    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:book_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    path('rate/<int:book_id>/', views.add_rating, name='add_rating'),
    path('review/<int:book_id>/', views.add_review, name='add_review'),
]
