from django.db.models import Case, IntegerField, When
from django.views.generic import ListView

from .models import Task


class TaskListView(ListView):
    model = Task
    template_name = "tasks/index.html"
    context_object_name = "tasks"

    def get_queryset(self):
        # Sort status: Ongoing → Open → Done → Obsolete
        status_order = Case(
            When(status=Task.Status.ONGOING, then=0),
            When(status=Task.Status.OPEN, then=1),
            When(status=Task.Status.DONE, then=2),
            When(status=Task.Status.OBSOLETE, then=3),
            default=4,
            output_field=IntegerField(),
        )

        # Sort priority within each status: High → Medium → Low
        priority_order = Case(
            When(priority=Task.Priority.HIGH, then=0),
            When(priority=Task.Priority.MEDIUM, then=1),
            When(priority=Task.Priority.LOW, then=2),
            default=3,
            output_field=IntegerField(),
        )

        return Task.objects.order_by(status_order, priority_order, "-created_at")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Map status values to section titles (rename DONE → Closed)
        ctx["section_titles"] = {
            Task.Status.ONGOING: "Ongoing",
            Task.Status.OPEN: "Open",
            Task.Status.DONE: "Closed",
            Task.Status.OBSOLETE: "Obsolete",
        }
        return ctx
