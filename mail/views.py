from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import ClientForm, LetterForm, MailingForm
from .models import Client, Letter, Logging, Mailing
from .services import send_mailing


# Client Views
class ClientListView(LoginRequiredMixin, ListView):
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


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("mail:client_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("mail:client_list")

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm("mail.can_view_all_list"):
            return queryset
        return queryset.filter(owner=self.request.user)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = "clients/client_confirm_delete.html"
    success_url = reverse_lazy("mail:client_list")

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm("mail.can_view_all_list"):
            return queryset
        return queryset.filter(owner=self.request.user)


# Letter Views
class LetterListView(LoginRequiredMixin, ListView):
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


class LetterCreateView(LoginRequiredMixin, CreateView):
    model = Letter
    form_class = LetterForm
    template_name = "letters/letter_form.html"
    success_url = reverse_lazy("mail:letter_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class LetterUpdateView(LoginRequiredMixin, UpdateView):
    model = Letter
    form_class = LetterForm
    template_name = "letters/letter_form.html"
    success_url = reverse_lazy("mail:letter_list")

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm("mail.can_view_all_list"):
            return queryset
        return queryset.filter(owner=self.request.user)


class LetterDeleteView(LoginRequiredMixin, DeleteView):
    model = Letter
    template_name = "letters/letter_confirm_delete.html"
    success_url = reverse_lazy("mail:letter_list")

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm("mail.can_view_all_list"):
            return queryset
        return queryset.filter(owner=self.request.user)


# Mailing Views
class MailingListView(LoginRequiredMixin, ListView):
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


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mail:mailing_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing/mailing_detail.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm("mail.can_view_all_list"):
            return queryset
        return queryset.filter(owner=self.request.user)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mail:mailing_list")

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm("mail.can_view_all_list"):
            return queryset
        return queryset.filter(owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mail:letter_list")

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm("mail.can_view_all_list"):
            return queryset
        return queryset.filter(owner=self.request.user)


# Logging Views (только чтение)
class LoggingListView(LoginRequiredMixin, ListView):
    model = Logging
    template_name = "logs/log_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm("mail.can_view_all_list"):
            return queryset
        return queryset.filter(owner=self.request.user)


class LoggingDetailView(LoginRequiredMixin, DetailView):
    model = Logging
    template_name = "logs/log_detail.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm("mail.can_view_all_list"):
            return queryset
        return queryset.filter(owner=self.request.user)


def home(request):
    # Фильтруем данные в зависимости от прав пользователя
    if request.user.has_perm("mail.can_view_all_list"):
        # Если у пользователя есть права на просмотр всех списков, показываем общую статистику
        total_mailings = Mailing.objects.count()
        active_mailings = Mailing.objects.filter(status="started").count()
        unique_clients = Client.objects.distinct().count()
    else:
        # Иначе показываем только данные пользователя
        total_mailings = Mailing.objects.filter(owner=request.user).count()
        active_mailings = Mailing.objects.filter(owner=request.user, status="started").count()
        unique_clients = Client.objects.filter(owner=request.user).distinct().count()

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


def end_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    mailing.status = "Завершена"
    mailing.save()

    return redirect("mail:mailing_detail", pk=pk)
