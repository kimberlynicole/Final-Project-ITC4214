from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile

# Register your models here.

# =========================
# PROFILE INLINE 
# =========================
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


# =========================
# CUSTOM USER ADMIN
# =========================
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)


# =========================
# REGISTER
# =========================
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)