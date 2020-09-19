from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from tasks.models import Tasks
from users.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class TasksAdmin(admin.ModelAdmin):
    model = Tasks
    list_display = ('id', 'title', 'description', 'due_date', 'is_done')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'description')
    list_editable = ('is_done',)
    list_filter = ('is_done',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Tasks, TasksAdmin)
