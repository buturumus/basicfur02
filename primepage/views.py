# primepage/views.py

import logging  # noqa
# from django.shortcuts import render
from django.views.generic import TemplateView
from .models import SideMenu
from .lc_data import LcData

lc = LcData.lc
lc_num = LcData.lc_num
LC_NAMES = LcData.LC_NAMES


class Primepage(TemplateView):
    template_name = 'primepage/primepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # add to context localized names
        for thekey in LC_NAMES:
            context[thekey] = LC_NAMES[thekey][lc_num]
        # add sidebar menu's items:
        context['sidemenu_items'] = SideMenu.get_sidemenu_items()
        return context

