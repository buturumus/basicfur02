# parts/views.py

import logging  # noqa
from django.http import JsonResponse
"""
# from django.http import HttpResponse
from django.http import Http404
from django.views.defaults import page_not_found
from datetime import datetime
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import DetailView
from .forms import EditPartnerForm
from .forms import EditMaterialForm
"""
from django.views.generic.list import ListView  # noqa
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
# app-level imports
from primepage.models import Partner
from primepage.models import Material
from primepage.models import MoneyEntry
from primepage.models import TabStarter
from primepage.models import MultimodelMatrixSummary
from primepage.models import MultimodelMatrixEdit
from primepage.models import MATRIX_CONSTS
from primepage.lc_data import LcData


# Class for all kinds of tab parts
class ShownAnypart(TabStarter, LcData):
    request = None
    tab_cmd = None
    pk = 0

    def __init__(self, *args, **kwargs):
        self.request = kwargs['request']
        self.tab_cmd = kwargs['tab_cmd']
        self.pk = kwargs['pk']
        self.label_keys_to_localize = ()
        self.tabclick_keys_to_localize = ()
        # fill std.fields width init.consts.data set
        TabStarter.__init__(self, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = {}
        context.update(TabStarter.get_context_data(self))
        context.update(LcData.get_context_data(self))
        # add  manually
        context.update({'pk': self.pk})
        #
        # logging.warning(context)
        #
        return context


# Classes for simpliest tab parts: bodies and tab headers

# based on template view class
class ShownBodieOrHeaderAnymodel(TemplateView, ShownAnypart):

    def __init__(self, *args, **kwargs):
        TemplateView.__init__(self, *args, **kwargs)
        ShownAnypart.__init__(self, *args, **kwargs)
        self.tabclick_keys_to_localize = ('lc_tab_title', )

    def get_context_data(self, *args, **kwargs):
        context = TemplateView.get_context_data(self, *args, **kwargs)
        context.update(
            ShownAnypart.get_context_data(self, *args, **kwargs)
        )
        return context


class ShownTabheader(ShownBodieOrHeaderAnymodel):
    template_name = 'parts/shown_tabheader.html'

    def __init__(self, *args, **kwargs):
        ShownBodieOrHeaderAnymodel.__init__(self, *args, **kwargs)


class ShownBodieSummaryAnymodel(ShownBodieOrHeaderAnymodel):
    template_name = 'parts/shown_bodie_summary_anymodel.html'

    def __init__(self, *args, **kwargs):
        ShownBodieOrHeaderAnymodel.__init__(self, *args, **kwargs)
        self.label_keys_to_localize = ('btn_f5', 'btn_close', )


class ShownBodieEditAnymodel(ShownBodieOrHeaderAnymodel):
    template_name = 'parts/shown_bodie_edit_anymodel.html'

    def __init__(self, *args, **kwargs):
        ShownBodieOrHeaderAnymodel.__init__(self, *args, **kwargs)
        self.label_keys_to_localize = ('btn_close_not_save', )


# More complex classes for matrixx tab part

class ShownMatrixAnymodel(ShownAnypart):
    pass


# anymodel class for summary-like matrixx, based on list view
class ShownMatrixSummaryAnymodel(ListView,
                                 ShownMatrixAnymodel,
                                 MultimodelMatrixSummary):
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
            MultimodelMatrixSummary.get_context_data(
                self, *args,
                object_list=context['object_list'],
                **kwargs
            )
        )
        return context


class ShownMatrixSummaryPartner(ShownMatrixSummaryAnymodel):
    model = Partner


class ShownMatrixSummaryMaterial(ShownMatrixSummaryAnymodel):
    model = Material


class ShownMatrixSummaryMoneyEntry(ShownMatrixSummaryAnymodel):
    model = MoneyEntry


# For edit-like matrixx

# common class for both new and edit cases
class ShownMatrixNewOrEditAnymodel(ShownMatrixAnymodel,
                                   MultimodelMatrixEdit):

    def __init__(self, *args, **kwargs):
        ShownMatrixAnymodel.__init__(self, *args, **kwargs)
        self.template_name = 'parts/shown_matrix_edit_anymodel.html'
        self.fields = MATRIX_CONSTS['edit']['shown_keys'][self.model]
        # move bottom buttons from bodie to form == to matrix
        self.label_keys_to_localize = ('btn_save_close', 'btn_delete', )
        # get initial values from model
        # initial = self.model.get_initials(self.request)

    def get_context_data(self, *args, **kwargs):
        context = ShownMatrixAnymodel.get_context_data(self, *args, **kwargs)
        return context

    # common for 'new' and 'edit' saving procedure
    def form_valid(self, form):
        # add keyvals written on backend side
        written_by_backend = self.model.get_written_by_backend(self.request)
        for field in written_by_backend:
            setattr(form.instance, field, written_by_backend[field])
        # save instance
        logging.warning(self)
        response = self.super_form_valid(form)
        return (
            JsonResponse({'pk': self.object.pk})
            if self.request.is_ajax() else response
        )
    # def form_valid(self, form):
    #     return self.render_to_response(self.get_context_data())


# anymodel class for new case only, based on create view
class ShownMatrixNewAnymodel(CreateView, ShownMatrixNewOrEditAnymodel):

    def __init__(self, *args, **kwargs):
        ShownMatrixNewOrEditAnymodel.__init__(self, *args, **kwargs)
        CreateView.__init__(self, *args, **kwargs)
        # self.initial = self.model.get_initials(self.request)

    def get_context_data(self, *args, **kwargs):
        context = ShownMatrixNewOrEditAnymodel.get_context_data(
            self, *args, **kwargs)
        context.update(
            CreateView.get_context_data(self, *args, **kwargs)
        )
        context.update(
            MultimodelMatrixEdit.get_context_data(
                self, *args,
                object_keyvals={},  # empty for 'new'
                form=context['form'],
                **kwargs
            )
        )
        return context

    def super_form_valid(self, form):
        return CreateView.form_valid(self, form)

    # and now rewrite form_valid
    def form_valid(self, form):
        return ShownMatrixNewOrEditAnymodel.form_valid(self, form)


# common data for edit case only, based on update view
class ShownMatrixEditAnymodel(UpdateView, ShownMatrixNewOrEditAnymodel):

    def __init__(self, *args, **kwargs):
        ShownMatrixNewOrEditAnymodel.__init__(self, *args, **kwargs)
        UpdateView.__init__(self, *args, **kwargs)
        # self.initial = self.model.get_initials(self.request)

    def get_context_data(self, *args, **kwargs):
        context = ShownMatrixNewOrEditAnymodel.get_context_data(
            self, *args, **kwargs)
        context.update(
            UpdateView.get_context_data(self, *args, **kwargs)
        )
        context.update(
            MultimodelMatrixEdit.get_context_data(
                self, *args,
                object_keyvals=context['object'],  # got from update view
                form=context['form'],
                **kwargs
            )
        )
        return context

    def super_form_valid(self, form):
        return UpdateView.form_valid(self, form)

    # and now rewrite form_valid
    def form_valid(self, form):
        return ShownMatrixNewOrEditAnymodel.form_valid(self, form)


# new/edit Partner
class ShownMatrixNewOrEditPartner:
    model = Partner


class ShownMatrixNewPartner(ShownMatrixNewOrEditPartner,
                            ShownMatrixNewAnymodel):

    def __init__(self, *args, **kwargs):
        ShownMatrixNewAnymodel.__init__(self, *args, **kwargs)


class ShownMatrixEditPartner(ShownMatrixNewOrEditPartner,
                             ShownMatrixEditAnymodel):

    def __init__(self, *args, **kwargs):
        ShownMatrixEditAnymodel.__init__(self, *args, **kwargs)


# new/edit Material
class ShownMatrixNewOrEditMaterial:
    model = Material


class ShownMatrixNewMaterial(ShownMatrixNewOrEditMaterial,
                             ShownMatrixNewAnymodel):

    def __init__(self, *args, **kwargs):
        ShownMatrixNewAnymodel.__init__(self, *args, **kwargs)


class ShownMatrixEditMaterial(ShownMatrixNewOrEditPartner,
                              ShownMatrixEditAnymodel):

    def __init__(self, *args, **kwargs):
        ShownMatrixEditAnymodel.__init__(self, *args, **kwargs)


# For 'delete' cases

class ShownDelAnymodel(DeleteView, ShownAnypart):
    template_name = 'parts/yesno.html'
    success_url = '.'

    def __init__(self, *args, **kwargs):
        ShownAnypart.__init__(self, *args, **kwargs)
        UpdateView.__init__(self, *args, **kwargs)
        self.label_keys_to_localize = (
            'yesno_sure_question', 'yesno_no_answer', 'yesno_yes_answer',
        )

    def get_context_data(self, *args, **kwargs):
        context = ShownAnypart.get_context_data(self, *args, **kwargs)
        context.update(
            DeleteView.get_context_data(self, *args, **kwargs)
        )
        return context

    def delete(self, request, *args, **kwargs):
        pk = self.get_object().pk
        response = DeleteView.delete(self, request, *args, **kwargs)
        return (
            JsonResponse({'pk': pk})
            if self.request.is_ajax() else response
        )


class ShownDelPartner(ShownDelAnymodel):
    model = Partner


class ShownDelMaterial(ShownDelAnymodel):
    model = Material


# ###

class ShownError(TemplateView):
    template_name = 'parts/shown_bodie_error.html'
    tab_cmd = None
    pk = 0


# ###

def selected_view(request, tab_cmd, part_stage, *args, **kwargs):
    # unwrap urlconf's vals: request, tab_cmd and part_stage as simple vars
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
    # 3rd stage, could be done independent if reload an existing tab
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
        elif tab_cmd in ('new_material', 'pensil_material'):
            view_class = ShownMatrixNewMaterial if kwargs[
                'pk'] == 0 else ShownMatrixEditMaterial
        else:
            view_class = ShownError
    # to delete some model inst.
    elif part_stage == 'del':
        if tab_cmd == 'pensil_partner':
            view_class = ShownDelPartner 
        elif tab_cmd == 'pensil_material':
            view_class = ShownDelMaterial
        else:
            view_class = ShownError
    else:
        view_class = ShownError
    # return view of selected class
    return view_class.as_view(
        request=request,
        tab_cmd=tab_cmd,
        pk=kwargs['pk']
    )(request, *args, **kwargs)

