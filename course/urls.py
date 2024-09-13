from django.urls import path
from course import views

urlpatterns = [
    path('index/', views.CategoryListView.as_view(), name='index'),
    path('courses_list/', views.CourseListView.as_view(), name='courses_list'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('teachers/', views.TeacherListView.as_view(), name='teachers_list'),
    path('blog_list/', views.BlogListView.as_view(), name='blog_list'),
    path('login/', views.LoginView.as_view(), name='login_page'),
]
