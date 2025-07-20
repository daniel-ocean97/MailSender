from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ClientForm, LetterForm, MailingForm
from .models import Client, Letter, Logging, Mailing
from .services import send_mailing


# Client Views
class ClientListView(ListView):
    model = Client
    template_name = "clients/client_list.html"

    def get_queryset(self):
        # Получаем стандартный queryset
        queryset = super().get_queryset()

        # Если пользователь имеет право can_view_all_list, возвращаем все объекты
        if self.request.user.has_perm("mail.can_view_all_list"):
            return queryset

        # Иначе возвращаем только объекты, владельцем которых является текущий пользователь
        return queryset.filter(owner=self.request.user)


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("mail:client_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("mail:client_list")


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "clients/client_confirm_delete.html"
    success_url = reverse_lazy("mail:client_list")


# Letter Views
class LetterListView(ListView):
    model = Letter
    template_name = "letters/Letters_list.html"

    def get_queryset(self):
        # Получаем стандартный queryset
        queryset = super().get_queryset()

        # Если пользователь имеет право can_view_all_list, возвращаем все объекты
        if self.request.user.has_perm("mail.can_view_all_list"):
            return queryset

        # Иначе возвращаем только объекты, владельцем которых является текущий пользователь
        return queryset.filter(owner=self.request.user)


class LetterCreateView(CreateView):
    model = Letter
    form_class = LetterForm
    template_name = "letters/letter_form.html"
    success_url = reverse_lazy("mail:letter_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class LetterUpdateView(UpdateView):
    model = Letter
    form_class = ClientForm
    template_name = "letters/letter_form.html"
    success_url = reverse_lazy("mail:letter_list")


class LetterDeleteView(DeleteView):
    model = Letter
    template_name = "letters/letter_confirm_delete.html"
    success_url = reverse_lazy("mail:letter_list")


# Mailing Views
class MailingListView(ListView):
    model = Mailing
    template_name = "mailing/mailing_list.html"

    def get_queryset(self):
        # Получаем стандартный queryset
        queryset = super().get_queryset()

        # Если пользователь имеет право can_view_all_list, возвращаем все объекты
        if self.request.user.has_perm("mail.can_view_all_list"):
            return queryset

        # Иначе возвращаем только объекты, владельцем которых является текущий пользователь
        return queryset.filter(owner=self.request.user)


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mail:mailing_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "mailing/mailing_detail.html"


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = ClientForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mail:letter_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mail:letter_list")


# Logging Views (только чтение)
class LoggingListView(ListView):
    model = Logging
    template_name = "logs/log_list.html"


class LoggingDetailView(DetailView):
    model = Logging
    template_name = "logs/log_detail.html"


def home(request):
    # Общее количество рассылок
    total_mailings = Mailing.objects.count()

    # Количество активных рассылок (статус 'Запущена')
    active_mailings = Mailing.objects.filter(status="started").count()

    # Количество уникальных клиентов во всех рассылках
    unique_clients = Client.objects.distinct().count()

    context = {
        "total_mailings": total_mailings,
        "active_mailings": active_mailings,
        "unique_clients": unique_clients,
    }
    return render(request, "mailing/home.html", context)


def start_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)

    # Проверяем права доступа
    if not request.user.is_superuser and mailing.owner != request.user:
        messages.error(request, "У вас нет прав для запуска этой рассылки")
        return redirect("mail:mailing_list")

    try:
        send_mailing(mailing)
        messages.success(request, "Рассылка успешно запущена!")
    except Exception as e:
        messages.error(request, f"Ошибка при запуске рассылки: {str(e)}")

    return redirect("mail:mailing_detail", pk=pk)
