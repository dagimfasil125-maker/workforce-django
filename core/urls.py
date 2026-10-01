from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.WorkforceLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile_view, name="profile"),

    path("admin-panel/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-panel/workers/", views.worker_list, name="worker_list"),
    path("admin-panel/workers/<int:pk>/delete/", views.worker_delete, name="worker_delete"),
    path("admin-panel/tasks/", views.task_list, name="task_list"),
    path("admin-panel/tasks/create/", views.task_create, name="task_create"),
    path("admin-panel/tasks/<int:pk>/delete/", views.task_delete, name="task_delete"),

    path("worker/dashboard/", views.worker_dashboard, name="worker_dashboard"),
    path("worker/tasks/<int:pk>/advance/", views.task_advance_status, name="task_advance_status"),
]
