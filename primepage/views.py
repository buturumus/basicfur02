# primepage/views.py

# from django.shortcuts import render
from django.views.generic import TemplateView
from misc import lc_strings
from .models import SideMenu
import logging  # noqa


class Primepage(TemplateView):
    template_name = 'primepage/primepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # add to context localized names
        for thekey in lc_strings.LC_NAMES:
            context[thekey] = lc_strings.LC_NAMES[thekey][lc_strings.lc_id]
        # add sidebar menu's items:
        context['sidemenu_items'] = SideMenu.get_template_items()
        # logging.warning(context['SIDEMENU_ITEMS'])
        return context

