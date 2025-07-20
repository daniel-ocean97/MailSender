from django.urls import path

from users.apps import UsersConfig

from .views import (
    CustomLoginView,
    CustomLogoutView,
    RegisterView,
    UserChangeView,
    UserListView,
    toggle_user_active,
)

app_name = UsersConfig.name


urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("change/<int:pk>/", UserChangeView.as_view(), name="change"),
    path("list/", UserListView.as_view(), name="user_list"),
    path("toggle-active/<int:pk>/", toggle_user_active, name="toggle_active"),
]
