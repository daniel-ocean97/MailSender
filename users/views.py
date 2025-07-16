from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER
from users.forms import CustomUserCreationForm


class CustomLoginView(LoginView):
    template_name = "login.html"  # Шаблон для отображения формы входа
    success_url = reverse_lazy("home")


class CustomLogoutView(LogoutView):
    template_name = "logout.html"
    next_page = reverse_lazy("catalog:home")


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = "Добро пожаловать в наш сервис"
        message = "Спасибо, что зарегистрировались в нашем сервисе!"
        recipient_list = [user_email]
        send_mail(
            subject, message, from_email=EMAIL_HOST_USER, recipient_list=recipient_list
        )
from django.shortcuts import render

# Create your views here.
