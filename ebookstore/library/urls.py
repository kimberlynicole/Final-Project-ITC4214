from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.my_library, name='my_library'),
    path('read/<int:book_id>/', views.read_book, name='read_book'),
    path('remove/<int:book_id>/', views.remove_from_library, name='remove_from_library'),
    path('add/<int:book_id>/', views.add_to_library, name='add_to_library'),
    
   
]