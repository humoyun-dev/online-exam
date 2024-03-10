from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('phone_number', 'first_name', 'last_name',)
    search_fields = ('phone_number', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'phone_number', 'parents_phone_number', 'is_teacher', 'is_student', 'gender',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'phone_number', 'password1', 'password2', 'parents_phone_number', 'is_teacher', 'is_student', 'gender', 'is_staff', 'is_superuser'),
        }),
    )
    ordering = ('phone_number',)

admin.site.register(CustomUser, CustomUserAdmin)
