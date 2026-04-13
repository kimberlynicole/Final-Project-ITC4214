from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.my_library, name='library'),
    path('add/<int:book_id>/', views.add_to_library, name='add_to_library'),
]