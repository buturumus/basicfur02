# parts/urls.py

from django.urls import path
# from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from .views import selected_view

urlpatterns = [
    path(
        '<str:tab_cmd>/<str:part_stage>/<int:pk>/',
        never_cache(
            selected_view
        )
    ),
    path(
        '<str:tab_cmd>/<str:part_stage>/',
        never_cache(
            selected_view
        )
    ),
]
