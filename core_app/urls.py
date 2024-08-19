from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.signout, name="logout"),
    path("generator", views.generator, name="email-generator"),
    path("generate-email", views.generate_email, name="generate-email"),
    path("profile/<str:pk>", views.profile, name="profile"),
    path("manage", views.manage, name="manage"),
    path("save-data", views.save_data, name="save-data"),
    path("remove-email/<str:pk>", views.remove_email, name="remove-email"),
    path("search", views.search_record, name="search"),
    path("about", views.about, name="about"),
]
