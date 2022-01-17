from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="homepage"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("request-password-change", views.request_change, name="requestPasswordChange"),
    path("change-password/<str:token>", views.change_unknown_pasword, name="changeUnknownPassword"),
    path("change-password", views.change_password, name="changeCurrentPassword"),
    path("change-name", views.change_name, name="changeName")
]