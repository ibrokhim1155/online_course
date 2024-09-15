from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from user.models import User,  Teacher

admin.site.register(Teacher)

@admin.register(User)
class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'email', 'is_staff', 'is_active')
