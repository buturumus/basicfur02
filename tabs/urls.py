# tabs/urls.py

from django.urls import path
# from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from .views import ShownTab

urlpatterns = [
    path(
        'tabs/<slug:click_id>/',
        never_cache(
            ShownTab.as_view()
        )
    ),
]

