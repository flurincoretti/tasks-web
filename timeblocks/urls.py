from django.urls import path

from .views import TimeblockListView

urlpatterns = [
    path("", TimeblockListView.as_view(), name="timeblock_list"),
]
