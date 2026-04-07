from django.urls import path
from . import views

app_name = 'accounts'  # still define this for namespacing in templates

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
]