from django.contrib import admin


from django.contrib import admin

from course.models import Course, Category, Video, Teacher

admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Video)
admin.site.register(Teacher)
