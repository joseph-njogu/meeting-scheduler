from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

app_name = "meetingsched"

urlpatterns = [
    path("", views.login, name="login"),
    path("login", views.login, name="login"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("create-meeting", views.create_meeting, name="create-meeting"),
    path("today-meeting", views.today_meeting, name="today-meeting"),
    path("past-meeting", views.past_meeting, name="past-meeting"),
    path("all-meeting", views.all_meeting, name="all-meeting"),
    path("register", views.register, name="register"),

]