from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .forms import WorkerCreationForm, TaskForm
from .models import User, Task


def is_admin(user):
    return user.is_authenticated and user.role == User.Role.ADMIN


def is_worker(user):
    return user.is_authenticated and user.role == User.Role.WORKER


class WorkforceLoginView(LoginView):
    """Custom login page. Sends each user to the right dashboard after login."""

    template_name = "registration/login.html"

    def get_success_url(self):
        if self.request.user.role == User.Role.ADMIN:
            return "/admin-panel/dashboard/"
        return "/worker/dashboard/"


def register_view(request):
    """Public registration always creates an Admin account.
    Workers are added later by an Admin from the Workers page."""
    if request.method == "POST":
        form = WorkerCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.Role.ADMIN
            user.save()
            login(request, user)
            return redirect("admin_dashboard")
    else:
        form = WorkerCreationForm()
    return render(request, "registration/register.html", {"form": form})


# ---------- Admin views ----------

@user_passes_test(is_admin, login_url="login")
def admin_dashboard(request):
    workers = User.objects.filter(role=User.Role.WORKER)
    tasks = Task.objects.all()
    context = {
        "total_workers": workers.count(),
        "pending": tasks.filter(status=Task.Status.PENDING).count(),
        "in_progress": tasks.filter(status=Task.Status.IN_PROGRESS).count(),
        "completed": tasks.filter(status=Task.Status.COMPLETED).count(),
        "recent_tasks": tasks[:5],
    }
    return render(request, "core/admin_dashboard.html", context)


@user_passes_test(is_admin, login_url="login")
def worker_list(request):
    if request.method == "POST":
        form = WorkerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Worker added successfully.")
            return redirect("worker_list")
    else:
        form = WorkerCreationForm()
    workers = User.objects.filter(role=User.Role.WORKER)
    return render(request, "core/worker_list.html", {"workers": workers, "form": form})


@user_passes_test(is_admin, login_url="login")
def worker_delete(request, pk):
    worker = get_object_or_404(User, pk=pk, role=User.Role.WORKER)
    if request.method == "POST":
        worker.delete()
        messages.success(request, "Worker removed.")
    return redirect("worker_list")


@user_passes_test(is_admin, login_url="login")
def task_list(request):
    tasks = Task.objects.all()
    status_filter = request.GET.get("status")
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    return render(request, "core/task_list.html", {"tasks": tasks, "status_filter": status_filter})


@user_passes_test(is_admin, login_url="login")
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task created and assigned.")
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "core/task_form.html", {"form": form})


@user_passes_test(is_admin, login_url="login")
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted.")
    return redirect("task_list")


# ---------- Worker views ----------

@user_passes_test(is_worker, login_url="login")
def worker_dashboard(request):
    tab = request.GET.get("tab", "active")
    tasks = Task.objects.filter(assigned_to=request.user)
    if tab == "completed":
        tasks = tasks.filter(status=Task.Status.COMPLETED)
    else:
        tasks = tasks.exclude(status=Task.Status.COMPLETED)
    context = {
        "tasks": tasks,
        "tab": tab,
        "active_count": Task.objects.filter(assigned_to=request.user).exclude(status=Task.Status.COMPLETED).count(),
        "completed_count": Task.objects.filter(assigned_to=request.user, status=Task.Status.COMPLETED).count(),
    }
    return render(request, "core/worker_dashboard.html", context)


@user_passes_test(is_worker, login_url="login")
def task_advance_status(request, pk):
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    if request.method == "POST":
        if task.status == Task.Status.PENDING:
            task.status = Task.Status.IN_PROGRESS
        elif task.status == Task.Status.IN_PROGRESS:
            task.status = Task.Status.COMPLETED
        task.save()
    return redirect("worker_dashboard")


# ---------- Shared ----------

@login_required
def profile_view(request):
    return render(request, "core/profile.html")
