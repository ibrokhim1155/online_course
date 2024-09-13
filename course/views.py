from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from .models import Course, Category, Blog, Teacher, Customer



class CategoryListView(ListView):
    model = Category
    template_name = 'course/index.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_categories'] = Category.objects.all().order_by('-title')[:5]
        return context



class CategoryDetailView(DetailView):
    model = Category
    template_name = 'course/category_detail.html'
    context_object_name = 'category'

    def get_object(self):
        return get_object_or_404(Category, pk=self.kwargs['pk'])

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

    def get_object(self):
        return get_object_or_404(Course, id=self.kwargs.get('course_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_courses'] = Course.objects.filter(category=self.object.category).exclude(id=self.object.id)[:5]
        return context



class AboutView(TemplateView):
    template_name = 'course/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers'] = Teacher.objects.all()
        return context



class TeacherListView(ListView):
    model = Teacher
    template_name = 'course/teachers_list.html'
    context_object_name = 'teachers'

    def get_queryset(self):
        return Teacher.objects.prefetch_related('courses').order_by('last_name')



class BlogListView(ListView):
    model = Blog
    template_name = 'course/blog_list.html'
    context_object_name = 'blogs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_blogs'] = Blog.objects.order_by('-created_at')[:5]
        return context



class CustomerListView(ListView):
    model = Customer
    template_name = 'course/customer_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        return Customer.objects.select_related('user').order_by('-id')

from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse_lazy

class LoginView(AuthLoginView):
    template_name = 'course/login.html'
    success_url = reverse_lazy('home')

