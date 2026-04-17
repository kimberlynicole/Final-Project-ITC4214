from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.my_library, name='my_library'),
    path('read/<int:book_id>/', views.read_book, name='read_book'),

    path('update-progress/<int:book_id>/', views.update_progress, name='update_progress'),
    
   
]