from django.urls import path
from course import views
from user.views import TeacherListView
from .views import VideoListView, VideoDetailView, BlogDetailView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('index/', views.CategoryListView.as_view(), name='index'),
    path('courses_list/', views.CourseListView.as_view(), name='courses_list'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('teachers/', TeacherListView.as_view(), name='teachers_list'),
    path('blog_list/', views.BlogListView.as_view(), name='blog_list'),
    path('blog_detail/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('courses_detail/<int:pk>/', views.CourseDetailView.as_view(), name='courses_detail'),
    path('videos/', VideoListView.as_view(), name='video_list'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
