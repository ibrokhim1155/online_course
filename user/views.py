from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.generic import FormView, ListView, CreateView

from user.forms import RegisterModelForm, SendingEmailForm
from user.models import User


class LoginView(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')

    def get_success_url(self):
        return self.success_url


class LogoutView(LogoutView):
    next_page = 'login_page'


class RegisterView(CreateView):
    form_class = RegisterModelForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def active(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login_page')
    else:
        return render(request, 'activation_invalid.html')


class SendingEmail(FormView):
    template_name = 'send-email.html'
    form_class = SendingEmailForm

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        recipient_list = form.cleaned_data['recipient_list'].split(',')
        send_mail(subject, message, 'your_email@example.com', recipient_list)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('send_email')


class TeacherListView(ListView):
    model = User
    template_name = 'teachers_list.html'
    context_object_name = 'teachers'

    def get_queryset(self):
        return User.objects.filter(is_teacher=True)
