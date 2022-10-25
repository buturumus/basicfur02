# parts/views.py

import logging  # noqa
from django.views.generic.list import ListView  # noqa
# from django.shortcuts import render
# from models import AsViewContainer
# from django.template.loader import render_to_string
"""
from django.http import JsonResponse
from django.http import Http404
from django.views.defaults import page_not_found
from django.views.generic.list import ListView
"""
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.views.generic import CreateView
from misc.common_functions import lc
from primepage.models import Partner
from primepage.models import Material
from primepage.models import MoneyEntry
from primepage.models import DataForAnypart
from primepage.models import DataForSimplepartAnymodel
from primepage.models import DataForBodieSummaryAnymodel
from primepage.models import DataForBodieEditAnymodel
from primepage.models import DataForMatrixSummaryAnymodel
from primepage.models import DataForMatrixEditAnymodel


# Class for all kinds of tab parts
class ShownAnypart:
    tab_cmd = None
    pk = 0

    def __init__(self, *args, **kwargs):
        self.tab_cmd = kwargs['tab_cmd']
        self.pk = kwargs['pk']

    def get_context_data(self, *args, **kwargs):
        context = {}
        context.update(DataForAnypart.get_extra_context(self))
        return context


# Classes for simpliest tab parts: bodies and tab headers
#
# Based on template view class
class ShownSimplepartAnymodel(TemplateView,
                              ShownAnypart,
                              DataForSimplepartAnymodel
                              ):

    def __init__(self, *args, **kwargs):
        TemplateView.__init__(self, *args, **kwargs)
        ShownAnypart.__init__(self, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = TemplateView.get_context_data(self, *args, **kwargs)
        context.update(ShownAnypart.get_context_data(
            self, *args, **kwargs))
        context.update(DataForSimplepartAnymodel.get_extra_context(
            self, *args, **kwargs))
        # logging.warning(context)
        return context


class ShownTabheader(ShownSimplepartAnymodel):
    template_name = 'parts/shown_tabheader.html'


class ShownBodieSummaryAnymodel(ShownSimplepartAnymodel,
                                DataForBodieSummaryAnymodel
                                ):
    template_name = 'parts/shown_bodie_summary_anymodel.html'

    def get_context_data(self, *args, **kwargs):
        context = ShownSimplepartAnymodel.get_context_data(
            self, *args, **kwargs)
        context.update(DataForBodieSummaryAnymodel.get_extra_context(
            self, *args, **kwargs))
        return context


class ShownBodieEditAnymodel(ShownSimplepartAnymodel,
                             DataForBodieEditAnymodel,
                             ):
    template_name = 'parts/shown_bodie_edit_anymodel.html'

    def get_context_data(self, *args, **kwargs):
        context = ShownSimplepartAnymodel.get_context_data(
            self, *args, **kwargs)
        context.update(DataForBodieSummaryAnymodel.get_extra_context(
            self, *args, **kwargs))
        return context


# More comples classes for other tab parts=matrixx
#
class ShownMatrixAnymodel(ShownAnypart):
    pass


# For summary-like matrixx.
# Based on list view class.
class ShownMatrixSummaryAnymodel(ListView, ShownMatrixAnymodel):
    template_name = 'parts/shown_matrix_summary_anymodel.html'

    def __init__(self, *args, **kwargs):
        ListView.__init__(self, *args, **kwargs)
        ShownMatrixAnymodel.__init__(self, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = ListView.get_context_data(self, *args, **kwargs)
        context.update(
            ShownMatrixAnymodel.get_context_data(self, *args, **kwargs)
        )
        context.update(
            DataForMatrixSummaryAnymodel.get_context_data(
                self, *args, 
                object_list=context['object_list'], 
                **kwargs
            )
        )
        #
#       logging.warning(context)
        return context


class ShownMatrixSummaryPartner(ShownMatrixSummaryAnymodel):
    model = Partner


class ShownMatrixSummaryMaterial(ShownMatrixSummaryAnymodel):
    model = Material


class ShownMatrixSummaryMoneyEntry(ShownMatrixSummaryAnymodel):
    model = MoneyEntry


# For edit-like matrixx.
# Based on detail view class.
class ShownMatrixEditAnymodel(DetailView, ShownMatrixAnymodel):
    template_name = 'parts/shown_matrix_edit_anymodel.html'

    def __init__(self, *args, **kwargs):
        if kwargs['pk'] != 0:
            DetailView.__init__(self, *args, **kwargs)
        ShownMatrixAnymodel.__init__(self, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = DetailView.get_context_data(self, *args, **kwargs)
        context.update(
            ShownMatrixAnymodel.get_context_data(self, *args, **kwargs)
        )
        context.update(
            DataForMatrixEditAnymodel.get_context_data(
                self, *args, 
                object_keyvals=context['object'], 
                **kwargs
            )
        )
        #
        # logging.warning(context)
        return context


class ShownMatrixEditPartner(ShownMatrixEditAnymodel):
    model = Partner


class ShownMatrixNewAnymodel(CreateView, ShownMatrixAnymodel):
    template_name = 'parts/shown_matrix_edit_anymodel.html'

    def __init__(self, *args, **kwargs):
        CreateView.__init__(self, *args, **kwargs)
        ShownMatrixAnymodel.__init__(self, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = CreateView.get_context_data(self, *args, **kwargs)
        context.update(
            ShownMatrixAnymodel.get_context_data(self, *args, **kwargs)
        )
        context.update(
            DataForMatrixEditAnymodel.get_context_data(
                self, *args, 
                object_keyvals=context['object'], 
                **kwargs
            )
        )
        #
        # logging.warning(context)
        return context


class ShownMatrixNewPartner(ShownMatrixNewAnymodel):
    model = Partner


class ShownError(TemplateView):
    template_name = 'parts/shown_bodie_error.html'
    tab_cmd = None
    pk = 0


def selected_view(request, tab_cmd, part_stage, *args, **kwargs):
    # unwrap urlconf's vals: tab_cmd and part_stage as simple vars
    # and pk as a kwargs val - only it must be transferred with view'a kwargs
    #
    # tab bodie:
    # startstage for every tab load
    if part_stage == 'bodie':
        if tab_cmd in (
            'partners_list',
            'materials_list',
            'money_entries_log',
        ):
            view_class = ShownBodieSummaryAnymodel
        elif tab_cmd in (
            'new_partner',
            'new_material',
            'pensil_partner',
            'pensil_material',
        ):
            view_class = ShownBodieEditAnymodel
        else:
            view_class = ShownError
    #
    # tab header:
    # 2nd stage for every tab loading
    elif part_stage == 'tabheader':
        view_class = ShownTabheader
    #
    # tab matrix:
    # 3rd stage, could be independent on reload of existing tab
    elif part_stage == 'matrix':
        if tab_cmd == 'partners_list':
            view_class = ShownMatrixSummaryPartner
        elif tab_cmd == 'materials_list':
            view_class = ShownMatrixSummaryMaterial
        elif tab_cmd == 'money_entries_log':
            view_class = ShownMatrixSummaryMoneyEntry
        elif tab_cmd in ('new_partner', 'pensil_partner'):
            view_class = ShownMatrixNewPartner if kwargs[
                'pk'] == 0 else ShownMatrixEditPartner 
        else:
            view_class = ShownError
    else:
        view_class = ShownError
    # return view of selected class
    return view_class.as_view(
        tab_cmd=tab_cmd,
        pk=kwargs['pk']
    )(request, *args, **kwargs)

