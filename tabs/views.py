# tabs/view.py

import logging  # noqa
# from django.shortcuts import render
# from models import AsViewContainer
# from django.template.loader import render_to_string
from django.http import JsonResponse
from django.http import Http404
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView


class AsViewContainer:

    def make_json_resp(self, request):
        if request.is_ajax() and request.method == 'POST':
            return True
        else:
            raise Http404
        return JsonResponse({
            'html_in_json':
            ''
            # self.make_html_resp(request)
        })

    @classmethod
    def as_view(cls):
        tab_part = cls()
        return tab_part.make_json_resp


class ShownHeader(ListView, AsViewContainer):

    def __init__(self):
        logging.warning('start init')
        self.template = 'tabs/header.html'
        super().__init__()


class ShownBody(AsViewContainer):
    pass


class ShownSumMatrixStd(ListView):
    template_name = 'mainpage/mainpage.html'


class ShownTab(TemplateView):
    template_name = 'tabs/body_summary.html'

    def get_context_data(self, *args, **kwargs):
        logging.warning('get_context_data')
        context = super().get_context_data(*args, **kwargs)

        """
        @classmethod
        def as_view(cls, **initkwargs):
            self = cls(**initkwargs)
            view = super(TemplateView, cls).as_view(**initkwargs)
            logging.warning(view())
            return view
        """
        