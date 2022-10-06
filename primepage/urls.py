# primapage/urls.py

from django.urls import path
# from django.http import HttpResponse
from django.views.decorators.cache import never_cache

from primepage.views import Primepage

urlpatterns = [
    path(
        '',
        never_cache(
            Primepage.as_view()
        ),
        name='primepage'  # important for login
    ),
]

