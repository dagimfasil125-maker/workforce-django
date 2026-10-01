from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import path, include


@login_required
def home_redirect(request):
    if request.user.role == "ADMIN":
        return redirect("admin_dashboard")
    return redirect("worker_dashboard")


urlpatterns = [
    path("", home_redirect, name="home"),
    path("django-admin/", admin.site.urls),
    path("", include("core.urls")),
]
