from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from user.models import Teacher
from .forms import CommentForm
from .models import Course, Category, Blog, Customer, Video


class CategoryListView(ListView):
    model = Category
    template_name = 'course/index.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teachers = Teacher.objects.all()
        courses = Course.objects.all()
        context['teachers'] = teachers
        context['courses'] = courses
        context['popular_categories'] = Category.objects.all().order_by('-title')[:5]
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'course/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = self.object.courses.all()
        return context


class CourseListView(ListView):
    model = Course
    template_name = 'course/courses_list.html'
    context_object_name = 'courses'
    ordering = ['name']

    def get_queryset(self):
        return Course.objects.select_related('category', 'teacher').order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['popular_courses'] = Course.objects.filter(category__isnull=False).order_by('-rating')[:5]
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = 'course/courses_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        course = self.get_object()
        context = super().get_context_data(**kwargs)
        videos = course.videos.all()
        context['related_courses'] = Course.objects.filter(category=self.object.category).exclude(id=self.object.id)[:5]
        context['videos'] = videos
        return context


class AboutView(TemplateView):
    template_name = 'course/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers'] = Teacher.objects.all()
        return context


class BlogListView(ListView):
    model = Blog
    template_name = 'course/blog_list.html'
    context_object_name = 'blogs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_blogs'] = Blog.objects.order_by('-created_at')[:5]
        context['categories'] = Category.objects.all()
        return context


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'course/blog_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_blogs'] = Blog.objects.exclude(id=self.object.id).order_by('-created_at')[:5]
        context['categories'] = Category.objects.all()
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        blog = self.get_object()
        form = CommentForm()

        if 'comment' in request.GET:
            form = CommentForm(request.GET)

            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.blog = blog
                comment.save()
                return redirect('index')

        return redirect('index')


class CustomerListView(ListView):
    model = Customer
    template_name = 'course/customer_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        return Customer.objects.select_related('user').order_by('-id')


class VideoListView(ListView):
    model = Video
    template_name = 'course/video_list.html'
    context_object_name = 'videos'


class VideoDetailView(DetailView):
    model = Video
    template_name = 'course/video_detail.html'
    context_object_name = 'video'

    def post(self, request, *args, **kwargs):
        blog = self.get_object()
        form = CommentForm()

        if 'comment' in request.GET:
            form = CommentForm(request.GET)

            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.blog = blog
                comment.save()
                return redirect('index')

        return redirect('index')

