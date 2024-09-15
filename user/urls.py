from django.urls import path
from user import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('logout/', views.LogoutView.as_view(), name='logout_page'),
    path('register/', views.RegisterView.as_view(), name='register_page'),
    path('activate/<uidb64>/<token>/', views.active, name='activate'),
    path('send-email/', views.SendingEmail.as_view(), name='send_email'),
    path('teachers/', views.TeacherListView.as_view(), name='teachers_list'),
]
