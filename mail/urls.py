from django.urls import path
from . import views
from mail.apps import MailConfig

app_name = MailConfig.name

urlpatterns = [
    path('', views.home, name='home'),

    # Client URLs
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/create/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/edit/', views.ClientUpdateView.as_view(), name='client_edit'),
    path('clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),

    # Letter URLs
    path('letters/', views.LetterListView.as_view(), name='letter_list'),
    path('letters/create/', views.LetterCreateView.as_view(), name='letter_create'),
    path('letters/update/', views.LetterUpdateView.as_view(), name='letter_update'),
    path('letters/delete/', views.LetterDeleteView.as_view(), name='letter_delete'),

    # Mailing URLs
    path('mailings/', views.MailingListView.as_view(), name='mailing_list'),
    path('mailings/create/', views.MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/update/', views.MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/delete/', views.MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings/detail/<int:pk>/', views.MailingDetailView.as_view(), name='mailing_detail'),
    # Logging URLs
    path('logs/', views.LoggingListView.as_view(), name='log_list'),
    path('logs/<int:pk>/', views.LoggingDetailView.as_view(), name='log_detail'),
]