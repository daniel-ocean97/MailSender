from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, ListView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import CustomUserCreationForm

from .models import User


class CustomLoginView(LoginView):
    template_name = "login.html"  # Шаблон для отображения формы входа
    success_url = reverse_lazy("home")


class CustomLogoutView(LogoutView):
    template_name = "logout.html"
    next_page = reverse_lazy("mail:home")


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy("mail:home")

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


class UserChangeView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserCreationForm
    context_object_name = "user"
    template_name = "user_form.html"
    success_url = reverse_lazy("mail:home")


@method_decorator(cache_page(60 * 15), name="dispatch")
class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "user_list.html"
    context_object_name = "object_list"

    def get_queryset(self):
        managers = Group.objects.get(name='Managers')
        qs = super().get_queryset().exclude(is_superuser=True).exclude(groups__in=[managers])
        return qs


    def test_func(self):
        return self.request.user.has_perm("users.can_block_users")


def toggle_user_active(request, pk):
    if not request.user.has_perm("users.can_block_user"):
        messages.error(request, "У вас нет прав для выполнения этого действия")
        return redirect("home")

    user = get_object_or_404(get_user_model(), pk=pk)

    # Не позволяем блокировать себя
    if user == request.user:
        messages.warning(request, "Вы не можете заблокировать себя")
        return redirect("users:user_list")

    user.is_active = not user.is_active
    user.save()

    action = "заблокирован" if not user.is_active else "активирован"
    messages.success(request, f"Пользователь {user.username} {action}")

    return redirect("users:user_list")
