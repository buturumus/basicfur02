# parts/views.py

import logging  # noqa
from django.http import JsonResponse
from django.http import Http404
"""
# from django.http import HttpResponse
from django.views.defaults import page_not_found
from datetime import datetime
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import DetailView
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
from primepage.models import MoneyEntriesBunch
from primepage.models import TabStarterViewData

# from primepage.models import MultimodelMatrixSummary
# from primepage.models import MultimodelMatrixNewOrEdit

from primepage.models import MultimodelMethods
from .forms import EditPartnerForm
from .forms import EditMaterialForm
# from .forms import EditMoneyEntryForm
from .forms import EditMoneyEntriesBunchForm
from primepage.lc_data import LcData


# Class for all kinds of tab parts
class ShownAnypart(TabStarterViewData, LcData):
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
        TabStarterViewData.__init__(self, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = {}
        context.update(TabStarterViewData.tabstarter_get_context_data(self))
        context.update(LcData.get_context_data(self))
        # add  manually
        context.update({'pk': self.pk})
        #
        # logging.warning(context)
        #
        return context


# ######################################################
#
# Classes for simpliest tab parts: bodies and tab headers
#
# ######################################################


#
# All based on Template view


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


class ShownBodieSummaryAnymodel(ShownBodieOrHeaderAnymodel):
    template_name = 'parts/shown_bodie_summary_anymodel.html'

    def __init__(self, *args, **kwargs):
        ShownBodieOrHeaderAnymodel.__init__(self, *args, **kwargs)
        self.label_keys_to_localize = ('btn_f5', 'btn_close', )


class ShownBodieNewOrEditAnymodel(ShownBodieOrHeaderAnymodel):
    template_name = 'parts/shown_bodie_new_or_edit_anymodel.html'

    def __init__(self, *args, **kwargs):
        ShownBodieOrHeaderAnymodel.__init__(self, *args, **kwargs)
        self.label_keys_to_localize = ('btn_close_not_save', )


# ######################################################
#
# More complex classes - for matrixx tab part
#
# ######################################################


class ShownMatrixAnymodel(ShownAnypart):
    pass


#
# Summary-like matrixx, based on list view
#

class ShownMatrixSummaryAnymodel(ListView,
                                 ShownMatrixAnymodel):
    template_name = 'parts/shown_matrix_summary_anymodel.html'

    def __init__(self, *args, **kwargs):
        self.queryset = self.model.objects.order_by(
            'name')  # for most models
        ListView.__init__(self, *args, **kwargs)
        ShownMatrixAnymodel.__init__(self, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = ListView.get_context_data(self, *args, **kwargs)
        context.update(
            ShownMatrixAnymodel.get_context_data(self, *args, **kwargs)
        )
        context.update(
            MultimodelMethods.summary_get_context_data(
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

    def __init__(self, *args, **kwargs):
        self.queryset = self.model.objects.order_by('humanid')
        ListView.__init__(self, *args, **kwargs)
        ShownMatrixAnymodel.__init__(self, *args, **kwargs)


#
# Edit and New case's matrixx
#

# Common classes for both New-s and Edit-s

class ShownMatrixNewOrEditAnymodel(ShownMatrixAnymodel):

    def __init__(self, *args, **kwargs):
        ShownMatrixAnymodel.__init__(self, *args, **kwargs)
        self.template_name = 'parts/shown_matrix_new_or_edit_anymodel.html'
        self.model_get_context_method = (
            MultimodelMethods
            .new_or_edit_get_context_data
        )
        # move bottom buttons from bodie to form ( == localize them in matrix)
        self.label_keys_to_localize = ('btn_save_close', 'btn_delete', )
        # get common New-/Edit- initial values from the model
        self.initial = self.model.forms_new_or_edit_initials(self)

    # inner part of get_object_keyvals to overwrite in New-/Edit- cases
    def get_object_keyvals(self, context):
        pass

    def get_context_data(self, *args, **kwargs):
        context = ShownMatrixAnymodel.get_context_data(self, *args, **kwargs)
        context.update(
            self.super_generic_class.get_context_data(self, *args, **kwargs)
        )
        # re-check if form exists in context
        form_kwargs = {}
        form_kwargs.update(kwargs)
        if 'form' not in form_kwargs:
            form_kwargs.update({'form': context['form']})
        # update context with model's common new-/edit- method
        context.update(
            self.model_get_context_method(
                self, *args,
                object_keyvals=self.get_object_keyvals(context),
                form=context['form'],
                **kwargs
            )
        )
        return context

    def extra_form_valid_jobs(self):
        pass

    def new_or_edit_form_valid(self, form):
        if not self.request.is_ajax():
            return Http404
        # add keyvals written on backend side
        written_by_backend = self.model.get_backend_written_new(self)
        for field in written_by_backend:
            setattr(form.instance, field, written_by_backend[field])
        # save instance, return HttpResponse
        super_response = self.super_generic_class.form_valid(self, form)
        result = (
            JsonResponse({'pk': self.object.pk})
            if super_response.status_code < 400 else super_response
        )
        # hook to do some extra jobs
        # (for money entries bunch it means
        # to write money entries instead of bunch)
        self.extra_form_valid_jobs()
        return result

    def new_or_edit_form_invalid(self, form):
        #
        logging.warning('form_invalid')
        logging.warning(form.errors)
        #
        return (
            JsonResponse({'pk': '-1'})
        )


class ShownMatrixNewOrEditPartner:
    model = Partner
    form_class = EditPartnerForm


class ShownMatrixNewOrEditMaterial:
    model = Material
    form_class = EditMaterialForm


class ShownMatrixNewOrEditMoneyEntriesBunch:
    model = MoneyEntriesBunch
    form_class = EditMoneyEntriesBunchForm
    new_money_entries_bunch = None

    # new_money_entries_bunch_pk = 0  # for money bunch/entry pk mockery

    humanid = 0  # for money bunch/entry-related stuff

    def __init__(self, *args, **kwargs):
        # extra button to localize
        self.label_keys_to_localize += ('edit_m_entry_details', )

    # save entered to money entries bunch data to simple money entries
    def extra_form_valid_jobs(self):
        # an extra check
        if not self.object.pk:
            return
        for money_entry, dr_acc, cr_acc in zip(
            # iterate over new or existing money entry instance
            self.get_new_or_exist_money_entries(),
            # and the bunch's acc.pairs
            self.get_new_or_exist_money_entries_accs('dr_accs'),
            self.get_new_or_exist_money_entries_accs('cr_accs'),
        ):
            # don't process accs.pair if any of them is empty
            # or they are equal
            if (not dr_acc) or (not cr_acc) or (dr_acc == cr_acc):
                continue
            # copy bunch's vals to new separate money entries
            for the_field in MoneyEntry.MATRIX_CONSTS['edit']['shown_keys']:
                if the_field == 'dr_acc':
                    setattr(money_entry, the_field, dr_acc)
                elif the_field == 'cr_acc':
                    setattr(money_entry, the_field, cr_acc)
                else:
                    setattr(money_entry,
                            the_field,
                            getattr(self.object, the_field))
            money_entry.save()
        # delete bunch object
        self.object.delete()


#
# 'New' cases - based on Create view


class ShownMatrixNewAnymodel(CreateView,
                             ShownMatrixNewOrEditAnymodel):

    def __init__(self, *args, **kwargs):
        ShownMatrixNewOrEditAnymodel.__init__(self, *args, **kwargs)
        CreateView.__init__(self, *args, **kwargs)
        self.super_generic_class = CreateView
        # get New-only initial values from the model
        self.initial.update(self.model.forms_new_initials(self))

    # inner part of -NewOrEditAnymodel's get_object_keyvals
    def get_object_keyvals(self, context):
        return {}  # empty for New

    def get_context_data(self, *args, **kwargs):
        return ShownMatrixNewOrEditAnymodel.get_context_data(
            self, *args, **kwargs)

    # rewrite CreateView's form_valid's stuff
    def form_valid(self, form):
        return self.new_or_edit_form_valid(form)

    def form_invalid(self, form):
        return self.new_or_edit_form_invalid(form)


class ShownMatrixNewPartner(ShownMatrixNewOrEditPartner,
                            ShownMatrixNewAnymodel):

    def __init__(self, *args, **kwargs):
        ShownMatrixNewAnymodel.__init__(self, *args, **kwargs)


class ShownMatrixNewMaterial(ShownMatrixNewOrEditMaterial,
                             ShownMatrixNewAnymodel):

    def __init__(self, *args, **kwargs):
        ShownMatrixNewAnymodel.__init__(self, *args, **kwargs)


class ShownMatrixNewMoneyEntriesBunch(ShownMatrixNewOrEditMoneyEntriesBunch,
                                      ShownMatrixNewAnymodel):

    def __init__(self, *args, **kwargs):
        ShownMatrixNewAnymodel.__init__(self, *args, **kwargs)
        # rewrite for non-looped template
        self.model_get_context_method = (
            MoneyEntriesBunch
            .new_or_edit_get_context_data
        )
        ShownMatrixNewOrEditMoneyEntriesBunch.__init__(self, *args, **kwargs)
        self.template_name = (
            'parts/shown_matrix_edit_money_entries_bunch.html')

    def get_context_data(self, *args, **kwargs):
        return ShownMatrixNewOrEditAnymodel.get_context_data(
            self, *args, **kwargs)

    # parts of extra_form_valid_jobs()
    # create 3 new entries
    def get_new_or_exist_money_entries(self):
        return [MoneyEntry() for i in range(2)]

    # get accs from hot entry
    def get_new_or_exist_money_entries_accs(self, accs_type):
        return (
            MoneyEntriesBunch
            .get_hot_entries_accs(self.hot_entry_name)
            [accs_type]
        )

#
# 'Edit' cases - based on Update view


class ShownMatrixEditAnymodel(UpdateView,
                              ShownMatrixNewOrEditAnymodel):

    def __init__(self, *args, **kwargs):

        # kwargs['pk'] = self.new_money_entries_bunch_pk

        kwargs['pk'] = self.new_money_entries_bunch.id
        ShownMatrixNewOrEditAnymodel.__init__(self, *args, **kwargs)
        UpdateView.__init__(self, *args, **kwargs)
        self.super_generic_class = UpdateView
        # common initial values already gotten in ShownMatrixNewOrEditAnymodel

    # inner part of -NewOrEditAnymodel's get_object_keyvals
    def get_object_keyvals(self, context):
        return context['object']

    def get_context_data(self, *args, **kwargs):
        return ShownMatrixNewOrEditAnymodel.get_context_data(
            self, *args, **kwargs)

    # rewrite UpdateView's form_valid's stuff
    def form_valid(self, form):
        return self.new_or_edit_form_valid(form)

    def form_invalid(self, form):
        return self.new_or_edit_form_invalid(form)


class ShownMatrixEditPartner(ShownMatrixNewOrEditPartner,
                             ShownMatrixEditAnymodel):

    def __init__(self, *args, **kwargs):
        ShownMatrixEditAnymodel.__init__(self, *args, **kwargs)


class ShownMatrixEditMaterial(ShownMatrixNewOrEditMaterial,
                              ShownMatrixEditAnymodel):

    def __init__(self, *args, **kwargs):
        ShownMatrixEditAnymodel.__init__(self, *args, **kwargs)


# special case: create new bunch and fill it with db data
class ShownMatrixEditMoneyEntriesBunch(ShownMatrixNewOrEditMoneyEntriesBunch,
                                       ShownMatrixEditAnymodel):

    def __init__(self, *args, **kwargs):
        #
        # mock pk to create new money entries'bunch instance
        # and fill it with data from money entries with same humanid
        #
        # get entrie's pk
        pensil_pk = kwargs['pk']
        # create bunch instance
        new_bunch = MoneyEntriesBunch()
        # find entries[0-2] with same humanid by pensil_pk
        head_money_entry = MoneyEntry.objects.filter(
            id=pensil_pk)[:1].get()
        money_entries = MoneyEntry.objects.filter(
            humanid=head_money_entry.humanid)[:3]
        # copy entry's non-acc.fields to bunch inst.
        for the_key in MoneyEntry.MATRIX_CONSTS['edit']['shown_keys']:
            if the_key not in ('dr_acc', 'cr_acc'):
                setattr(new_bunch,
                        the_key,
                        getattr(money_entries[0], the_key))
        for idx, money_entry in enumerate(money_entries):
            setattr(new_bunch,
                    'dr_acc' + str(idx),
                    getattr(money_entry, 'dr_acc'))
            setattr(new_bunch,
                    'cr_acc' + str(idx),
                    getattr(money_entry, 'cr_acc'))
        new_bunch.save()
        self.new_money_entries_bunch = new_bunch

        # self.new_money_entries_bunch_pk = new_bunch.id

        self.humanid = new_bunch.humanid

        ShownMatrixEditAnymodel.__init__(self, *args, **kwargs)
        # rewrite for non-looped template
        self.model_get_context_method = (
            MoneyEntriesBunch
            .new_or_edit_get_context_data
        )
        ShownMatrixNewOrEditMoneyEntriesBunch.__init__(self, *args, **kwargs)
        #
        self.template_name = (
            'parts/shown_matrix_edit_money_entries_bunch.html')

    # get-related parts

    # key point to mock pk for update view
    def get_object(self, *args, **kwargs):
        return self.model.objects.get(id=self.pk)

    def get_context_data(self, *args, **kwargs):
        context = ShownMatrixEditAnymodel.get_context_data(
            self, *args, **kwargs)
        logging.warning(context['pk'])
        # logging.warning(context)
        # add new_money_entries_bunch_pk to template(hidden field in yes/no)
        return context

    # save-related part

    # parts of extra_form_valid_jobs()
    # get entries with same humanid
    def get_new_or_exist_money_entries(self):
        return MoneyEntry.objects.filter(humanid=self.humanid)[:3]

    # get accs from current money entries bunch
    def get_new_or_exist_money_entries_accs(self, accs_type):
        return (
            [
                getattr(self.new_money_entries_bunch, acc_keyname)
                for acc_keyname in ('dr_acc0', 'dr_acc1', 'dr_acc2')
            ]
            if accs_type == 'dr_accs' else
            [
                getattr(self.new_money_entries_bunch, acc_keyname)
                for acc_keyname in ('cr_acc0', 'cr_acc1', 'cr_acc2')
            ]
            if accs_type == 'cr_accs' else
            []
        )

#
# 'Delete' cases - based of Delete view


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

    # rewritable part of delete()
    def get_super_response(self, request, *args, **kwargs):
        return DeleteView.delete(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not self.request.is_ajax():
            return Http404
        self.money_entries_bunch_pk = request.POST['money_entries_bunch_pk']
        pk = self.get_object().pk
        super_response = self.get_super_response(
            self, request, *args, **kwargs)
        return (
            JsonResponse({'pk': pk})
            if super_response.status_code < 400 else super_response
        )


class ShownDelPartner(ShownDelAnymodel):
    model = Partner


class ShownDelMaterial(ShownDelAnymodel):
    model = Material


class ShownDelMoneyEntry(ShownDelAnymodel):
    model = MoneyEntry
    money_entries_bunch_pk = ''

    # rewrite generic's method: pick at money entry instance
    def get_object(self, *args, **kwargs):
        return MoneyEntry.objects.get(id=self.pk)

    # rewrite part of delete()
    def get_super_response(self, request, *args, **kwargs):
        # delete now opened money entries bunch
        logging.warning('money_entries_bunch to del:')
        logging.warning(self.money_entries_bunch_pk)
        MoneyEntriesBunch.objects.get(id=self.money_entries_bunch_pk).delete()
        # delete all money entries with same humanid
        for money_entry in MoneyEntry.objects.filter(
            humanid=self.get_object().humanid
        ):
            if money_entry.id != self.get_object().id:
                logging.warning('extra money_entry.id to del:')
                logging.warning(money_entry.id)
                MoneyEntry.objects.get(id=money_entry.id).delete()
        # delete money entry under pensil
        return DeleteView.delete(self, request, *args, **kwargs)


# ###

class ShownError(TemplateView):
    template_name = 'parts/shown_bodie_error.html'
    tab_cmd = None
    pk = 0


# ######################################################
#
#  View selection
#
# ######################################################

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
            'pensil_partner',
            'pensil_material',
            'pensil_money_entry',
            'new_partner',
            'new_material',
            'cache_in',
            'cache_out',
        ):
            view_class = ShownBodieNewOrEditAnymodel
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
        elif tab_cmd in ('pensil_partner', 'new_partner'):
            view_class = ShownMatrixNewPartner if kwargs[
                'pk'] == 0 else ShownMatrixEditPartner
        elif tab_cmd in ('pensil_material', 'new_material'):
            view_class = ShownMatrixNewMaterial if kwargs[
                'pk'] == 0 else ShownMatrixEditMaterial
        elif tab_cmd in (
            'pensil_money_entry',
            'cache_in',
            'cache_out',
        ):
            view_class = ShownMatrixNewMoneyEntriesBunch if kwargs[
                'pk'] == 0 else ShownMatrixEditMoneyEntriesBunch
        else:
            view_class = ShownError
    # to delete some model inst.
    elif part_stage == 'del':
        if tab_cmd == 'pensil_partner':
            view_class = ShownDelPartner
        elif tab_cmd == 'pensil_material':
            view_class = ShownDelMaterial
        elif tab_cmd == 'pensil_money_entry':
            view_class = ShownDelMoneyEntry
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

