
from django.contrib import admin

from course.models import Course, Category, Video, Blog

admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Video)
admin.site.register(Blog)
# admin.site.register(Teacher)
