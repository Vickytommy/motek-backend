from django.urls import path, include
from . import views

app_name = 'admin'
urlpatterns = [
    path("index", views.index, name="index"),
    path("users", views.users, name="users"),
]