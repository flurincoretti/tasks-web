from django.views.generic import ListView

from .models import Timeblock


class TimeblockListView(ListView):
    model = Timeblock
    template_name = "timeblocks/index.html"
    context_object_name = "timeblocks"
