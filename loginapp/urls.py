from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("", views.index),
    path("register", views.register),
    path("success", views.success),
    path("logout", views.logout),
    path("login", views.login),

]
