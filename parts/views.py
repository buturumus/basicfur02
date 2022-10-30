# parts/views.py

import logging  # noqa
from django.views.generic.list import ListView  # noqa
# from django.shortcuts import render
# from models import AsViewContainer
# from django.template.loader import render_to_string
from django.http import HttpResponse
"""
from django.http import JsonResponse
from django.http import Http404
from django.views.defaults import page_not_found
from django.views.generic.list import ListView
"""
from django.views.generic.base import TemplateView
# from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
# from misc.common_functions import lc
# from misc.common_functions import lc
from .forms import EditPartnerForm
from .forms import EditMaterialForm
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
    tab_cmd = None
    pk = 0

    def __init__(self, *args, **kwargs):
        self.tab_cmd = kwargs['tab_cmd']
        self.pk = kwargs['pk']
        self.label_keys_to_localize = ()
        self.tabclick_keys_to_localize = ()
        # fill std.fields width init.costs.data set
        TabStarter.__init__(self, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = {}
        context.update(
            TabStarter.get_context_data(self)
        )
        context.update(
            LcData.get_context_data(self)
        )
        # add  manually
        context.update({'pk': self.pk})
        #
        logging.warning(
            context
        )
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
        #
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
        # ('btn_save_close', 'btn_delete', )
        # 'ShownMatrixEditAnymodel':
        #     ('btn_save_close', 'btn_delete', ),


# More comples classes for matrixx tab part

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

    def get_context_data(self, *args, **kwargs):
        context = ShownMatrixAnymodel.get_context_data(self, *args, **kwargs)
        form = self.form_name()
        context.update({'form': form})
        return context

    def post(self, request, *args, **kwargs):
        form = EditPartnerForm(request.POST)
        if form.is_valid:
            partner = form.save()
            #
            logging.warning(partner)
            #
            # partner.save()
            return HttpResponse('')
        else:
            return HttpResponse('')


# anymodel class for new case only, based on create view
class ShownMatrixNewAnymodel(CreateView, ShownMatrixNewOrEditAnymodel):

    def __init__(self, *args, **kwargs):
        ShownMatrixNewOrEditAnymodel.__init__(self, *args, **kwargs)
        CreateView.__init__(self, *args, **kwargs)

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


# common data for edit case only, based on update view
class ShownMatrixEditAnymodel(UpdateView, ShownMatrixNewOrEditAnymodel):

    def __init__(self, *args, **kwargs):
        ShownMatrixNewOrEditAnymodel.__init__(self, *args, **kwargs)
        UpdateView.__init__(self, *args, **kwargs)

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


# new/edit Partner
class ShownMatrixNewOrEditPartner:
    model = Partner
    form_name = EditPartnerForm


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
    form_name = EditMaterialForm


class ShownMatrixNewMaterial(ShownMatrixNewOrEditMaterial,
                             ShownMatrixNewAnymodel):

    def __init__(self, *args, **kwargs):
        ShownMatrixNewAnymodel.__init__(self, *args, **kwargs)


class ShownMatrixEditMaterial(ShownMatrixNewOrEditPartner,
                              ShownMatrixEditAnymodel):

    def __init__(self, *args, **kwargs):
        ShownMatrixEditAnymodel.__init__(self, *args, **kwargs)


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
    else:
        view_class = ShownError
    # return view of selected class
    return view_class.as_view(
        tab_cmd=tab_cmd,
        pk=kwargs['pk']
    )(request, *args, **kwargs)

