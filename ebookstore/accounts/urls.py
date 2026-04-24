from django.urls import path
from . import views

app_name = 'accounts'  # still define this for namespacing in templates

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('admin/books/', views.admin_books, name='admin_books'),
    path('admin/books/add/', views.add_book, name='add_book'),
    path('admin/books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('admin/books/delete/<int:book_id>/', views.delete_book, name='delete_book'),

    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
]