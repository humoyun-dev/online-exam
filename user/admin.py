# In admin.py of your user app or any appropriate app

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin


from .models import CustomUser, Students_group

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'phone_number', 'is_teacher', 'is_student', 'first_name', 'last_name']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_teacher', 'is_student', "group_of_student")}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        # ("Groups", {"group":("group_of_student", )})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone_number', 'is_teacher', 'is_student', "group_of_student")}
        ),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


class Students_groupAdmin(admin.ModelAdmin):
    model = Students_group
    list_display = ["group_name", "description"]
    search_fields = ("group_name", )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Students_group, Students_groupAdmin)