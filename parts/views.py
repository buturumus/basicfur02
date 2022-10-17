# parts/views.py

import logging  # noqa
import re
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
from misc.common_functions import lc
# from primepage.models import TabmakingItems
from primepage.models import Partner
from primepage.models import Material
from primepage.models import MoneyEntry
from primepage.models import DataForAnypart
from primepage.models import DataForSimplepartAnymodel
from primepage.models import MATRIX_CONSTS


# Class for all kinds of tab parts
class ShownAnypart:
    tab_cmd = None

    def __init__(self, tab_cmd, *args, **kwargs):
        self.tab_cmd = tab_cmd

    def get_context_data(self, *args, **kwargs):
        context = {}
        context.update(DataForAnypart.get_extra_context(self))
        return context


# Classes for simpliest tab parts: bodies and tab headers
#
# Based on template view class
class ShownSimplepartAnymodel(TemplateView, ShownAnypart):

    def __init__(self, *args, **kwargs):
        TemplateView.__init__(self, *args, **kwargs)
        ShownAnypart.__init__(self, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = TemplateView.get_context_data(self, *args, **kwargs)
        context.update(
            ShownAnypart.get_context_data(self, *args, **kwargs)
        )
        context.update(
            DataForSimplepartAnymodel.get_extra_context(self, *args, **kwargs)
        )
        # logging.warning(context)
        return context


class ShownBodieSummaryAnymodel(ShownSimplepartAnymodel):
    template_name = 'parts/shown_bodie_summary_anymodel.html'


class ShownTabheader(ShownSimplepartAnymodel):
    template_name = 'parts/shown_tabheader.html'


# More comples classes for other tab parts=matrixx
#
class ShownMatrixAnymodel(ShownAnypart):
    pass


# For summary-like matrixx.
# Based on list view class..
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
        # upd.context with disassembled instances' keyvalues
        all_keyvals = context['object_list'].values()
        logging.warning(all_keyvals)
        context.update({
            'object_list_values':
            [{
                shown_key:
                a_dict[shown_key]
                if (
                    shown_key in a_dict
                    and a_dict[shown_key]
                ) else
                self.model._meta.get_field(
                    f'{shown_key}_id').related_model.objects.get(
                    id=a_dict[f'{shown_key}_id'])
                if (
                    f'{shown_key}_id' in a_dict
                    and a_dict[f'{shown_key}_id']
                ) else
                ''
                for shown_key in MATRIX_CONSTS[
                    'summary']['shown_keys'][self.model]
            } for a_dict in all_keyvals],
        })
        # context.update({
        #     'object_list_values':
        #     [{
        #         shown_key:
        #         [
        #             a_dict[shown_key]
        #             if (
        #                 shown_key in a_dict
        #                 and a_dict[shown_key]
        #             ) else
        #             self.model._meta.get_field(shown_key + '_id')
        #                 .related_model
        #                 .objects.get(id=a_dict[shown_key + '_id'])
        #             if (
        #                 (shown_key + '_id') in a_dict
        #                 and a_dict[shown_key + '_id']
        #             ) else
        #             '',
        #             cls
        #         ]
        #         for shown_key, cls in zip(
        #             MATRIX_CONSTS['summary']['shown_keys'][self.model],
        #             MATRIX_CONSTS['summary']['header_html_classes']
        #             [self.model]
        #         )
        #     } for a_dict in all_keyvals],
        # })
        # with header names and html classes
        context.update({
            'headers_data':
            zip(
                [
                    lc(name_key) for name_key in
                    MATRIX_CONSTS['summary'][
                        'header_names_keys'][self.model]
                ],
                [
                    cls for cls in
                    MATRIX_CONSTS['summary'][
                        'header_html_classes'][self.model]
                ],
            )
        })
        #
        logging.warning(context)
        return context


class ShownMatrixSummaryPartner(ShownMatrixSummaryAnymodel):
    model = Partner


class ShownMatrixSummaryMaterial(ShownMatrixSummaryAnymodel):
    model = Material


class ShownMatrixSummaryMoneyEntry(ShownMatrixSummaryAnymodel):
    model = MoneyEntry


class ShownError(TemplateView):
    template_name = 'parts/shown_bodie_error.html'
    tab_cmd = None


def selected_view(request, tab_cmd, part_stage, *args, **kwargs):
    # starting stage for every tab loading
    if part_stage == 'bodie':
        if tab_cmd in (
            'partners_list',
            'materials_list',
            'money_entries_log',
        ):
            view_class = ShownBodieSummaryAnymodel
        else:
            view_class = ShownError
    # 2nd stage for every tab loading
    elif part_stage == 'tabheader':
        view_class = ShownTabheader
    # 3rd stage, could be independent on reload of existing tab
    elif part_stage == 'matrix':
        if tab_cmd == 'partners_list':
            view_class = ShownMatrixSummaryPartner
        elif tab_cmd == 'materials_list':
            view_class = ShownMatrixSummaryMaterial
        elif tab_cmd == 'money_entries_log':
            view_class = ShownMatrixSummaryMoneyEntry
        else:
            view_class = ShownError
    else:
        view_class = ShownError
    return view_class.as_view(tab_cmd=tab_cmd)(request, *args, **kwargs)

