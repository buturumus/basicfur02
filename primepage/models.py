# primepage/models.py

import logging  # noqa
from django.db import models
from users.models import CustomUser
# from datetime import date
from datetime import datetime
# from misc import common_classes
from misc.common_classes import Initable
from misc.common_classes import ClassNameGetter
from misc.common_functions import make_humanid
from .lc_data import LcData

# shortnames
name_from_model = ClassNameGetter.name_from_model
lc = LcData.lc
lc_num = LcData.lc_num
LC_NAMES = LcData.LC_NAMES


class MultimodelMethods:

    @staticmethod
    def summary_get_context_data(view, *args, **kwargs):
        context = {}
        # upd.context with disassembled instances' keyvalues
        context.update({
            'object_list_values_pks':
            zip(
                # object_list_values and html classes
                [{
                    shown_key:
                    [
                        # key
                        shown_key,
                        # value
                        a_dict[shown_key]
                        if (
                            shown_key in a_dict
                            and a_dict[shown_key]
                        ) else
                        view.model._meta.get_field(f'{shown_key}_id')
                            .related_model
                            .objects.get(id=a_dict[f'{shown_key}_id'])
                        if (
                            (f'{shown_key}_id') in a_dict
                            and a_dict[f'{shown_key}_id']
                        ) else
                        '',
                        # cell html class
                        cls,
                        # row pk
                        view.pk,
                    ]
                    for shown_key, cls in zip(
                        view.model.MATRIX_CONSTS['summary']['shown_keys'],
                        view.model.MATRIX_CONSTS['summary']['cell_html_classes']
                    )
                } for a_dict in kwargs['object_list'].values()],
                # pks
                [obj.id for obj in kwargs['object_list']],
            )
        })
        # with header names and html classes
        context.update({
            'headers_data':
            zip(
                [
                    lc(name_key) for name_key in
                    view.model.MATRIX_CONSTS['summary']['header_names_keys']
                ],
                [
                    cls for cls in
                    view.model.MATRIX_CONSTS['summary']['header_html_classes']
                ],
            )
        })
        return context

    # part of the class' new_or_edit_get_context_data()
    # returns nothing
    @staticmethod
    def new_or_edit_get_context_common(view, *args, **kwargs):
        object_keyvals = kwargs['object_keyvals']
        form = kwargs['form']
        # upd.context with selected object's keyvalues
        view.object_keyvals_and_cls = [
            [
                # key
                shown_key,
                # value which can be
                #   - fixed date for usage in a form
                object_keyvals.date.strftime('%Y-%m-%d')
                if (
                    shown_key == 'date'
                    and hasattr(object_keyvals, 'date')
                ) else
                #   - val if shown_key exist in object's keyvals dict
                getattr(object_keyvals, shown_key)
                if (
                    hasattr(object_keyvals, shown_key)
                    and getattr(object_keyvals, shown_key)
                ) else
                #   - val if shown_key_id exists i.e. the field is pk
                view.model._meta.get_field(f'{shown_key}_id')
                    .related_model
                    .objects.get(id=getattr(
                        object_keyvals, f'{shown_key}_id'))
                if (
                    hasattr(object_keyvals, f'{shown_key}_id')
                    and getattr(object_keyvals, f'{shown_key}_id')
                ) else
                #   - empty val for any other case
                '',
                # cell html class
                cls,
                # # is_hidden flag
                # 1 if shown_key in MATRIX_CONSTS['edit'][
                #     'hidden_keys'][view.model] else 0
            ]
            for shown_key, cls in zip(
                view.model.MATRIX_CONSTS['edit']['shown_keys'],
                view.model.MATRIX_CONSTS['edit']['cell_html_classes']
            )
        ]
        view.headers_names_and_cls = [
            [lc(name_key), cls]
            for name_key, cls in zip(
                view.model.MATRIX_CONSTS['edit']['header_names_keys'],
                view.model.MATRIX_CONSTS['edit']['header_html_classes']
            )
        ]
        view.form = form

    # for most cases == for looped template, returns zip
    def new_or_edit_get_context_data(view, *args, **kwargs):
        MultimodelMethods.new_or_edit_get_context_common(
            view, *args, **kwargs)
        return {
            'headers_cells_form_zip':
            zip(
                view.object_keyvals_and_cls,
                view.headers_names_and_cls,
                view.form,
            ),
        }


class SaveDataKeeper:

    # initial data for forms
    @staticmethod
    def forms_new_or_edit_initials(view):
        return {
            'created_by': view.request.user,
            'create_date': datetime.now(),
        }

    @staticmethod
    def forms_new_initials(self):
        return {}

    # (re)written on backend side
    @staticmethod
    def get_backend_written_new_or_edit(view):
        return {
            'created_by': view.request.user,
            'create_date': datetime.now(),
        }

    @staticmethod
    def get_backend_written_new(view):
        return {}

    def get_absolute_url(self):  # don't really need it because of ajax
        return ''


# not editable models

class Account(models.Model, Initable, ClassNameGetter):
    DEFAULT_KEYSET = (('number'), ())
    DEFAULT_KEYVALS = {
        '00': (), '05': (), '06': (), '20': (), '41': (),
        '46': (), '50/1': (), '51': (), '62': (),
        '71': (), '72/1': (), '80': (), '80/1': ()
    }

    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=8)

    def __str__(self):
        return self.number + ' - ' + LC_NAMES[f'acc_{self.number}'][lc_num]


# class AccPair(models.Model, Initable, ClassNameGetter):
#     id = models.AutoField(primary_key=True)
#     dr_acc = models.ForeignKey(
#         Account,
#         related_name='%(app_label)s_%(class)s_dr_acc',
#         default=None,
#         null=True,
#         blank=True,
#         on_delete=models.CASCADE)
#     cr_acc = models.ForeignKey(
#         Account,
#         related_name='%(app_label)s_%(class)s_cr_acc',
#         default=None,
#         null=True,
#         blank=True,
#         on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{str(self.dr_acc)}__{str(self.dr_acc)}'


class PartnerGroup(models.Model, Initable, ClassNameGetter):
    DEFAULT_KEYSET = (('name'), ())
    DEFAULT_KEYVALS = {'employees': (), }

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


# Editable models

class Partner(models.Model, ClassNameGetter, SaveDataKeeper):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    last_name = models.CharField(
        max_length=50,
        default='', null=True, blank=True,
    )
    partner_group = models.ForeignKey(
        PartnerGroup,
        related_name='%(app_label)s_%(class)s_partner_group',
        default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )
    create_date = models.DateTimeField(
        default=datetime(1970, 1, 1, 0, 0, 0, 0)
    )
    created_by = models.ForeignKey(
        CustomUser,
        related_name='%(app_label)s_%(class)s_created_by',
        default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )

    MATRIX_CONSTS = {
        'summary': {
            'shown_keys': (
                'name',
                'last_name',
                'partner_group',
                # pensil,
            ),
            'header_names_keys': (
                'summary_partner_name1',
                'summary_partner_name2',
                'summary_partner_group',
            ),
            'header_html_classes': (
                'col-5 text-left',
                'col-4 text-left',
                'col-2 text-left',
            ),
            'cell_html_classes': (
                'text-left',
                'text-left',
                'text-left',
            ),
        },
        'edit': {
            'shown_keys': (
                'name',
                'last_name',
                'partner_group',
                # pensil,
            ),
            'header_names_keys': (
                'edit_partner_name1',
                'edit_partner_name2',
                'edit_partner_group',
            ),
            'header_html_classes': (
                'col-4 text-left',
                'col-4 text-left',
                'col-4 text-left',
            ),
            'cell_html_classes': (
                'text-left',
                'text-left',
                'text-left',
            ),
        },
    }

    def __str__(self):
        return self.name


class Material(models.Model, ClassNameGetter, SaveDataKeeper):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    create_date = models.DateTimeField(
        default=datetime(1970, 1, 1, 0, 0, 0, 0))
    created_by = models.ForeignKey(
        CustomUser,
        related_name='%(app_label)s_%(class)s_created_by',
        default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )

    MATRIX_CONSTS = {
        'summary': {
            'shown_keys': (
                'name',
                '',
                # pensil,
            ),
            'header_names_keys': (
                'summary_material_name',
                '',
            ),
            'header_html_classes': (
                'col-7 text-left',
                'col-4',
            ),
            'cell_html_classes': (
                'text-left',
                '',
            ),
        },
        'edit': {
            'shown_keys': (
                'name',
            ),
            'header_names_keys': (
                'edit_material_name',
            ),
            'header_html_classes': (
                'col-4 text-left',
            ),
            'cell_html_classes': (
                'text-left',
            ),
        },
    }

    def __str__(self):
        return self.name


class HotEntry(models.Model, Initable, ClassNameGetter):
    DEFAULT_KEYSET = (
        ('name'),
        ('dr_acc0', 'cr_acc0', 'dr_acc1', 'cr_acc1', 'dr_acc2', 'cr_acc2', )
    )
    DEFAULT_KEYVALS = {
        'service': ('00', '00', '', '', '', ''),
        'shipping': ('62', '46', '', '', '', ''),
        'mat_to_prod': ('20', '05', '', '', '', ''),
        'get_invoice': ('80', '62', '', '', '', ''),
        'make_invoice': ('62', '80', '', '', '', ''),
        'from_bank': ('62', '51', '', '', '', ''),
        'to_bank': ('51', '62', '', '', '', ''),
        'to_stock': ('41', '20', '', '', '', ''),
        'consumable_purchase': ('06', '62', '', '', '', ''),
        'mat_purchase': ('05', '62', '', '', '', ''),
        'pay_salary': ('71', '50/1', '', '', '', ''),
        'calc_salary': ('80', '71', '', '', '', ''),
        'accountable_cache_out': ('72/1', '50/1', '', '', '', ''),
        'accountable_cache_return': ('50/1', '72/1', '', '', '', ''),
        'accountable_cache_spent': ('62', '72/1', '', '', '', ''),
        'cache_out': ('62', '50/1', '', '', '', ''),
        'cache_in': ('50/1', '62', '', '', '', ''),
    }
#           ('hot_tr_service',              '00', '00', 0, 0 ),
#           ('hot_tr_shipping',             '62', '46', 1, 0 ),
#           ('hot_tr_mat_to_prod',          '20', '05', 1, 0 ),
#           ('hot_tr_get_invoice',          '80', '62', 0, 0 ),
#           ('hot_tr_make_invoice',         '62', '80', 0, 0 ),
#           ('hot_tr_from_bank',            '62', '51', 0, 0 ),
#           ('hot_tr_to_bank',              '51', '62', 0, 0 ),
#           ('hot_tr_to_stock',             '41', '20', 1, 0 ),
#           ('hot_tr_consumable_purchase',  '06', '62', 1, 0 ),
#           ('hot_tr_mat_purchase',         '05', '62', 1, 0 ),
#           ('hot_tr_pay_salary',           '71', '50/1', 0, 1 ),
#           ('hot_tr_calc_salary',          '80', '71', 0, 1 ),
#           ('hot_tr_accountable_cache_out',    '72/1', '50/1', 0, 1 ),
#           ('hot_tr_accountable_cache_return', '50/1', '72/1', 0, 1 ),
#           ('hot_tr_accountable_cache_spent',  '62', '72/1', 0, 1 ),
#           ('hot_tr_cache_out',            '62', '50/1', 0, 0 ),
#           ('hot_tr_cache_in',             '50/1', '62', 0, 0 ),
#           ('hot_tr_empty',                '00', '00', 0, 0 ),

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, default='')
    dr_acc0 = models.ForeignKey(
        Account,
        related_name='%(app_label)s_%(class)s_dr0',
        # default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )
    cr_acc0 = models.ForeignKey(
        Account,
        related_name='%(app_label)s_%(class)s_cr0',
        # default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )
    dr_acc1 = models.ForeignKey(
        Account,
        related_name='%(app_label)s_%(class)s_dr1',
        default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )
    cr_acc1 = models.ForeignKey(
        Account,
        related_name='%(app_label)s_%(class)s_cr1',
        default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )
    dr_acc2 = models.ForeignKey(
        Account,
        related_name='%(app_label)s_%(class)s_dr2',
        default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )
    cr_acc2 = models.ForeignKey(
        Account,
        related_name='%(app_label)s_%(class)s_cr2',
        default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return LC_NAMES[f'hot_entry_{self.name}'][lc_num]

    @staticmethod
    def second_defaults_init_method(obj, the_key, the_val):
        setattr(obj, the_key, the_val)


class MoneyEntryBase(models.Model, ClassNameGetter, SaveDataKeeper):
    humanid = models.CharField(
        max_length=32,
        blank=True,
        default='')
    # parent_money_entry = models.ForeignKey(
    #     'self',
    #     related_name='%(app_label)s_%(class)s_parent_entry',
    #     default=None,
    #     null=True,
    #     blank=True,
    #     on_delete=models.CASCADE)
    money = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.0)
    hot_entry = models.ForeignKey(
        HotEntry,
        related_name='%(app_label)s_%(class)s_hot_entry',
        # default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )
    date = models.DateField()
    # date = models.DateField(
    #     #
    #     default=None,
    #     null=True,
    #     blank=True,
    #     #
    # )
    partner = models.ForeignKey(
        Partner,
        related_name='%(app_label)s_%(class)s_entry_partner',
        default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )
    employee = models.ForeignKey(
        Partner,
        related_name='%(app_label)s_%(class)s_employee',
        default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )
    comment = models.CharField(max_length=256, blank=True)
    create_date = models.DateTimeField(
        default=datetime(1970, 1, 1, 0, 0, 0, 0))
    created_by = models.ForeignKey(
        CustomUser,
        related_name='%(app_label)s_%(class)s_created_by',
        default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )
    # has_goodslines = models.SmallIntegerField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return self.humanid


class MoneyEntry(MoneyEntryBase):
    id = models.AutoField(primary_key=True)
    parent_money_entry = models.ForeignKey(
        'self',
        related_name='%(app_label)s_%(class)s_parent_entry',
        default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )
    dr_acc = models.ForeignKey(
        Account,
        related_name='%(app_label)s_%(class)s_dr',
        # default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )
    cr_acc = models.ForeignKey(
        Account,
        related_name='%(app_label)s_%(class)s_cr',
        # default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )

    MATRIX_CONSTS = {
        'summary': {
            'shown_keys': (
                'humanid',
                'date',
                'partner',
                'hot_entry',
                'dr_acc',
                'cr_acc',
                'money',
                'comment',
                # pensil,
            ),
            'header_names_keys': (
                'summary_m_entry_humanid',
                'summary_m_entry_date',
                'summary_m_entry_partner',
                'summary_m_entry_hot_entry',
                'summary_m_entry_dr_acc',
                'summary_m_entry_cr_acc',
                'summary_m_entry_money',
                'summary_m_entry_comment',
            ),
            'header_html_classes': (
                'col-1',
                'col-1 text-right',
                'col-2',
                'col-1',
                'col-1 text-center',
                'col-1 text-center',
                'col-1 text-right',
                'col-3',
            ),
            'cell_html_classes': (
                '',
                'text-right',
                '',
                '',
                'text-center',
                'text-center',
                'text-right',
                '',
            ),
        },
        'edit': {
            'shown_keys': (
                'humanid',
                'date',
                'partner',
                'hot_entry',
                'dr_acc',
                'cr_acc',
                'money',
                'comment',
                'create_date',
                'created_by',
                # pensil,
            ),
            'header_names_keys': (
                'edit_m_entry_humanid',
                'edit_m_entry_date',
                'edit_m_entry_partner',
                'edit_m_entry_hot_entry',
                'edit_m_entry_dr_acc',
                'edit_m_entry_cr_acc',
                'edit_m_entry_money',
                'edit_m_entry_comment',
                '',
                '',
            ),
            'header_html_classes': (
                '',
                'text-right',
                '',
                '',
                'text-center',
                'text-center',
                'text-right',
                '',
                '',
                '',
            ),
            'cell_html_classes': (
                '',
                'text-right',
                '',
                '',
                'text-center',
                'text-center',
                'text-right',
                '',
                '',
                '',
            ),
        },
    }


class MoneyEntriesBunch(MoneyEntryBase, MultimodelMethods):
    id = models.AutoField(primary_key=True)
    parent_money_entry = models.ForeignKey(
        'primepage.MoneyEntry',
        related_name='%(app_label)s_%(class)s_parent_entry',
        default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )
    dr_acc0 = models.ForeignKey(
        Account,
        related_name='%(app_label)s_%(class)s_dr0',
        # default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )
    cr_acc0 = models.ForeignKey(
        Account,
        related_name='%(app_label)s_%(class)s_cr0',
        # default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )
    dr_acc1 = models.ForeignKey(
        Account,
        related_name='%(app_label)s_%(class)s_dr1',
        default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )
    cr_acc1 = models.ForeignKey(
        Account,
        related_name='%(app_label)s_%(class)s_cr1',
        default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )
    dr_acc2 = models.ForeignKey(
        Account,
        related_name='%(app_label)s_%(class)s_dr2',
        default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )
    cr_acc2 = models.ForeignKey(
        Account,
        related_name='%(app_label)s_%(class)s_cr2',
        default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )

    MATRIX_CONSTS = {
        'summary': {
            'shown_keys': (
                'humanid',
                'date',
                'partner',
                'hot_entry',
                'dr_acc0',
                'cr_acc0',
                'money',
                'comment',
                'dr_acc1',
                'cr_acc1',
                'dr_acc2',
                'cr_acc2',
                # pensil,
            ),
            'header_names_keys': (
                'summary_m_entry_humanid',
                'summary_m_entry_date',
                'summary_m_entry_partner',
                'summary_m_entry_hot_entry',
                'summary_m_entry_dr_acc',
                'summary_m_entry_cr_acc',
                'summary_m_entry_money',
                'summary_m_entry_comment',
                'summary_m_entry_dr_acc',
                'summary_m_entry_cr_acc',
                'summary_m_entry_dr_acc',
                'summary_m_entry_cr_acc',
            ),
            'header_html_classes': (
                'col-1',
                'col-1 text-right',
                'col-2',
                'col-1',
                'col-1 text-center',
                'col-1 text-center',
                'col-1 text-right',
                'col-1 text-center',
                'col-1 text-center',
                'col-1 text-center',
                'col-1 text-center',
                'col-3',
            ),
            'cell_html_classes': (
                '',
                'text-right',
                '',
                '',
                'text-center',
                'text-center',
                'text-right',
                'text-center',
                'text-center',
                'text-center',
                'text-center',
                '',
            ),
        },
        'edit': {
            'shown_keys': (
                'humanid',
                'date',
                'partner',
                'hot_entry',
                'dr_acc0',
                'cr_acc0',
                'dr_acc1',
                'cr_acc1',
                'dr_acc2',
                'cr_acc2',
                'money',
                'comment',
                'create_date',
                'created_by',
                # pensil,
            ),
            'header_names_keys': (
                'edit_m_entry_humanid',
                'edit_m_entry_date',
                'edit_m_entry_dr_acc',
                'edit_m_entry_cr_acc',
                'edit_m_entry_dr_acc',
                'edit_m_entry_cr_acc',
                'edit_m_entry_dr_acc',
                'edit_m_entry_cr_acc',
                'edit_m_entry_money',
                'edit_m_entry_comment',
                '',
                '',
            ),
            'header_html_classes': (
                '',
                'text-right',
                '',
                '',
                'text-center',
                'text-center',
                'text-center',
                'text-center',
                'text-center',
                'text-center',
                'text-right',
                '',
                '',
                '',
            ),
            'cell_html_classes': (
                '',
                'text-right',
                '',
                '',
                'text-center',
                'text-center',
                'text-center',
                'text-center',
                'text-center',
                'text-center',
                'text-right',
                '',
                '',
                '',
            ),
        },
    }

    # initial data for forms
    @staticmethod
    def forms_new_or_edit_initials(view):
        initials = SaveDataKeeper.forms_new_or_edit_initials(view)
        # if hot_entry (== it's exists in prev.entry, i.e. Edit case)
        if view.hot_entry_name:
            initials.update(
                {'hot_entry': HotEntry.objects.get(name=view.hot_entry_name)}
            )
        return initials

    @staticmethod
    def forms_new_initials(view):
        initials = {
            'date': datetime.today().strftime('%Y-%m-%d'),
            # 'humanid': make_humanid(),
        }
        for the_acc in ('dr_acc0', 'cr_acc0', 'dr_acc1',
                        'cr_acc1', 'dr_acc2', 'cr_acc2'):
            the_hot_entry_acc = getattr(
                HotEntry.objects.get(name=view.hot_entry_name),
                the_acc
            )
            if the_hot_entry_acc:
                initials.update({the_acc: the_hot_entry_acc})
        return initials

    # (re)written on backend side
    @staticmethod
    def get_backend_written_new(view):
        backend_written = SaveDataKeeper.get_backend_written_new(view)
        backend_written.update({'humanid': make_humanid()})
        return backend_written

    # rewritten multimodels' method
    # the template needs separate lists not zip on return
    @staticmethod
    def new_or_edit_get_context_data(view, *args, **kwargs):
        MultimodelMethods.new_or_edit_get_context_common(
            view, *args, **kwargs)
        # for the_field in view.form:
        #     the_field.disabled = True
        return {
            'object_keyvals_and_cls': view.object_keyvals_and_cls,
            'headers_names_and_cls': view.headers_names_and_cls,
            'form_fields': [field for field in view.form],
        }

    @staticmethod
    def get_hot_entries_accs(hot_entry_name):
        money_entries_accs = {'dr_accs': [], 'cr_accs': []}
        for dr_acc_key, cr_acc_key in zip(
            ('dr_acc0', 'dr_acc1', 'dr_acc2'),
            ('cr_acc0', 'cr_acc1', 'cr_acc2')
        ):
            money_entries_accs['dr_accs'].append(
                getattr(
                    HotEntry.objects.get(name=hot_entry_name),
                    dr_acc_key
                )
            )
            money_entries_accs['cr_accs'].append(
                getattr(
                    HotEntry.objects.get(name=hot_entry_name),
                    cr_acc_key
                )
            )
        return money_entries_accs


class KilledMoneyEntry(models.Model, ClassNameGetter, SaveDataKeeper):
    id = models.AutoField(primary_key=True)
    humanid = models.CharField(
        max_length=32,
        blank=True,
        default='')
    parent_money_entry = models.ForeignKey(
        'self',
        related_name='killed_money_entry_parent_entry',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    money = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.0)
    hot_entry = models.ForeignKey(
        HotEntry,
        related_name='killed_money_entry_hot_entry',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    date = models.DateField()
    partner = models.ForeignKey(
        Partner,
        related_name='killed_money_entry_partner',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    employee = models.ForeignKey(
        Partner,
        related_name='killed_money_entry_employee',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    dr_acc = models.ForeignKey(
        Account,
        related_name='killed_money_entry_dr',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    cr_acc = models.ForeignKey(
        Account,
        related_name='killed_money_entry_cr',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    comment = models.CharField(max_length=256, blank=True)
    create_date = models.DateTimeField(
        default=datetime(1970, 1, 1, 0, 0, 0, 0))
    created_by = models.ForeignKey(
        CustomUser,
        related_name='%(app_label)s_%(class)s_created_by',
        default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )
    kill_date = models.DateTimeField(default='1970-01-01')
    killed_by = models.ForeignKey(
        # 'users.CustomUser',
        CustomUser,
        related_name='%(app_label)s_%(class)s_killed_by',
        default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )
    has_goods_entries = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.humanid


class GoodsEntry(models.Model, ClassNameGetter, SaveDataKeeper):
    id = models.AutoField(primary_key=True)
    humanid = models.CharField(
        max_length=32,
        blank=True,
        default='')
    parent_money_entry = models.ForeignKey(
        MoneyEntry,
        related_name='goods_entry_parent_entry',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    material = models.ForeignKey(
        Material,
        related_name='goods_entry_material',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    comment = models.CharField(max_length=256, blank=True)
    qty = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0)
    price = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        default=0.00)
    ship_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00)
    total = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00)
    ship_total = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00)
    create_date = models.DateTimeField(
        default=datetime(1970, 1, 1, 0, 0, 0, 0)
    )
    created_by = models.ForeignKey(
        CustomUser,
        related_name='%(app_label)s_%(class)s_created_by',
        default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.humanid
        # return str(self.comment)


class KilledGoodsEntry(models.Model, ClassNameGetter, SaveDataKeeper):
    id = models.AutoField(primary_key=True)
    humanid = models.CharField(
        max_length=32,
        blank=True,
        default='')
    parent_money_entry = models.ForeignKey(
        KilledMoneyEntry,
        related_name='killed_goods_entry_parent_entry',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    material = models.ForeignKey(
        Material,
        related_name='killed_goods_entry_material',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    comment = models.CharField(max_length=256, blank=True)
    qty = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0)
    price = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        default=0.00)
    ship_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00)
    total = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00)
    ship_total = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00)
    create_date = models.DateTimeField(
        default=datetime(1970, 1, 1, 0, 0, 0, 0))
    created_by = models.ForeignKey(
        CustomUser,
        related_name='%(app_label)s_%(class)s_created_by',
        default=None, null=True, blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.humanid
        # return str(self.comment)


# DB'less classes


class MultimodelMatrixSummary:

    @staticmethod
    def get_model_spec_context(view, *args, **kwargs):
        context = {}
        # upd.context with disassembled instances' keyvalues
        context.update({
            'object_list_values_pks':
            zip(
                # object_list_values and html classes
                [{
                    shown_key:
                    [
                        # key
                        shown_key,
                        # value
                        a_dict[shown_key]
                        if (
                            shown_key in a_dict
                            and a_dict[shown_key]
                        ) else
                        view.model._meta.get_field(f'{shown_key}_id')
                            .related_model
                            .objects.get(id=a_dict[f'{shown_key}_id'])
                        if (
                            (f'{shown_key}_id') in a_dict
                            and a_dict[f'{shown_key}_id']
                        ) else
                        '',
                        # cell html class
                        cls,
                        # row pk
                        view.pk,
                    ]
                    for shown_key, cls in zip(
                        view.model.MATRIX_CONSTS['summary']['shown_keys'],
                        view.model.MATRIX_CONSTS['summary']['cell_html_classes']
                    )
                } for a_dict in kwargs['object_list'].values()],
                # pks
                [obj.id for obj in kwargs['object_list']],
            )
        })
        # with header names and html classes
        context.update({
            'headers_data':
            zip(
                [
                    lc(name_key) for name_key in
                    view.model.MATRIX_CONSTS['summary']['header_names_keys']
                ],
                [
                    cls for cls in
                    view.model.MATRIX_CONSTS['summary']['header_html_classes']
                ],
            )
        })
        return context


class MultimodelMatrixNewOrEdit:

    # part of the class' get_model_spec_context
    # returns nothing
    def get_model_spec_context_common(view, *args, **kwargs):
        object_keyvals = kwargs['object_keyvals']
        form = kwargs['form']
        # upd.context with selected object's keyvalues
        view.object_keyvals_and_cls = [
            [
                # key
                shown_key,
                # value which can be
                #   - fixed date for usage in a form
                object_keyvals.date.strftime('%Y-%m-%d')
                if (
                    shown_key == 'date'
                    and hasattr(object_keyvals, 'date')
                ) else
                #   - val if shown_key exist in object's keyvals dict
                getattr(object_keyvals, shown_key)
                if (
                    hasattr(object_keyvals, shown_key)
                    and getattr(object_keyvals, shown_key)
                ) else
                #   - val if shown_key_id exists i.e. the field is pk
                view.model._meta.get_field(f'{shown_key}_id')
                    .related_model
                    .objects.get(id=getattr(
                        object_keyvals, f'{shown_key}_id'))
                if (
                    hasattr(object_keyvals, f'{shown_key}_id')
                    and getattr(object_keyvals, f'{shown_key}_id')
                ) else
                #   - empty val for any other case
                '',
                # cell html class
                cls,
                # # is_hidden flag
                # 1 if shown_key in MATRIX_CONSTS['edit'][
                #     'hidden_keys'][view.model] else 0
            ]
            for shown_key, cls in zip(
                view.model.MATRIX_CONSTS['edit']['shown_keys'],
                view.model.MATRIX_CONSTS['edit']['cell_html_classes']
            )
        ]
        view.headers_names_and_cls = [
            [lc(name_key), cls]
            for name_key, cls in zip(
                view.model.MATRIX_CONSTS['edit']['header_names_keys'],
                view.model.MATRIX_CONSTS['edit']['header_html_classes']
            )
        ]
        view.form = form

    # for most common cases
    # for looped template return zip
    def get_model_spec_context(view, *args, **kwargs):
        MultimodelMatrixNewOrEdit.get_model_spec_context_common(
            view, *args, **kwargs)
        return {
            'headers_cells_form_zip':
            zip(
                view.object_keyvals_and_cls,
                view.headers_names_and_cls,
                view.form,
            ),
        }


class MoneyEntriesBunchMatrixNewOrEdit(MultimodelMatrixNewOrEdit):

    # the template needs separate lists not zip
    def get_model_spec_context(view, *args, **kwargs):
        MultimodelMatrixNewOrEdit.get_model_spec_context_common(
            view, *args, **kwargs)
        # for the_field in view.form:
        #     the_field.disabled = True
        return {
            'object_keyvals_and_cls': view.object_keyvals_and_cls,
            'headers_names_and_cls': view.headers_names_and_cls,
            'form_fields': [field for field in view.form],
        }


# Class for all tab calling elements

class TabStarterViewData:
    TABSTARTER_KEYNAMES = (
        'level0_position',  # added in loop list
        'tab_cmd',
        'matrix_type',
        'model',
        'pensil_tab_cmd',
        'hot_entry_name',
    )
    TABSTARTER_CONSTS = (
        [['settings'] + i for i in [
            ['service_entry',
                'edit', MoneyEntry, '', 'service', ],
            ['money_entries_log',
                'summary', MoneyEntry, 'pensil_money_entry', '', ],
            ['partners_list',
                'summary', Partner, 'pensil_partner', '', ],
            ['new_partner',
                'edit', Partner, '', '', ],
            ['materials_list',
                'summary', Material, 'pensil_material', '', ],
            ['new_material',
                'edit', Material, '', '', ],
            ['killed_money_entries_log',
                'summary', MoneyEntry, '', '', ],
        ]]
        + [['analitics'] + i for i in [
            ['acc_sum_card',
                'acc_sum_card', MoneyEntry, '', '', ],
            ['inventories',
                'inventories', GoodsEntry, '', '', ],
            ['in_stock',
                'in_stock', GoodsEntry, '', '', ],
            ['partners_balance',
                'partners_balance', Partner, '', '', ],
            ['material_history',
                'material_history', GoodsEntry, '', '', ],
        ]]
        + [['trading'] + i for i in [
            ['shipping',
                'edit', MoneyEntriesBunch, '', 'shipping', ],
            ['make_invoice',
                'edit', MoneyEntriesBunch, '', 'make_invoice', ],
            ['get_invoice',
                'edit', MoneyEntriesBunch, '', 'get_invoice', ],
        ]]
        + [['production'] + i for i in [
            ['materials_purchase',
                'edit', MoneyEntriesBunch, '', 'mat_purchase', ],
            ['materials_to_production',
                'edit', MoneyEntriesBunch, '', 'mat_to_prod', ],
            ['consumables_purchase',
                'edit', MoneyEntriesBunch, '', 'consumable_purchase', ],
            ['production_to_stock',
                'edit', MoneyEntriesBunch, '', 'to_stock', ],
        ]]
        + [['finance'] + i for i in [
            ['cache_in',
                'edit', MoneyEntriesBunch, '', 'cache_in', ],
            ['cache_out',
                'edit', MoneyEntriesBunch, '', 'cache_out', ],
            ['to_bank',
                'edit', MoneyEntriesBunch, '', 'to_bank', ],
            ['from_bank',
                'edit', MoneyEntriesBunch, '', 'from_bank', ],
        ]]
        + [['employees'] + i for i in [
            ['calc_salary',
                'edit', MoneyEntriesBunch, '', 'calc_salary', ],
            ['pay_salary',
                'edit', MoneyEntriesBunch, '', 'pay_salary', ],
            ['accountable_cache_out',
                'edit', MoneyEntriesBunch, '', 'accountable_cache_out', ],
            ['accountable_cache_return',
                'edit', MoneyEntriesBunch, '', 'accountable_cache_return', ],
            ['accountable_cache_spent',
                'edit', MoneyEntriesBunch, '', 'accountable_cache_spent', ],
        ]]
        + [['admin'] + i for i in [
            ['wipe_entries',
                'wipe_entries', '', '', '', ],
        ]]
        + [['nosidebar'] + i for i in [
            ['pensil_partner',
                'edit', Partner, '', '', ],
            ['pensil_material',
                'edit', Material, '', '', ],
            # ['pensil_money_entry',
            #     'edit', MoneyEntry, '', '', ],
            ['pensil_money_entry',
                'edit', MoneyEntriesBunch, '', '', ],  # not MoneyEntry
            # ['pensil_money_entries_bunch',
            #     'edit', MoneyEntriesBunch, '', '', ],
        ]]
    )

    # make an instance by tab_cmd
    def __init__(self, *args, **kwargs):
        for consts_line in self.TABSTARTER_CONSTS:
            if consts_line[1] == self.tab_cmd:
                for the_key, the_val in zip(
                    self.TABSTARTER_KEYNAMES,
                    consts_line
                ):
                    if the_key not in ('level0_position', 'tab_cmd'):
                        setattr(self, the_key, the_val)

    @staticmethod
    def items_dictlist():
        named_items = []
        for consts_line in TabStarterViewData.TABSTARTER_CONSTS:
            the_dict = {}
            for the_key, the_val in zip(
                TabStarterViewData.TABSTARTER_KEYNAMES,
                consts_line
            ):
                the_dict.update({the_key: the_val})
            named_items.append(the_dict)
        return named_items

    # get std.tabstarter's context keyvals
    @staticmethod
    def tabstarter_get_context_data(view):
        TABSTARTER_CONTEXT_KEYS = (
            'tab_cmd',
            'matrix_type',
            'model',
            'pensil_tab_cmd',
            'hot_entry_name',
        )
        context = {}
        # fill context with values from tabmaking constants' dictlist
        # # for the_key in DataForAnypart.tabmaking_context_keys:
        for the_key in TABSTARTER_CONTEXT_KEYS:
            context.update({
                the_key:
                getattr(view, the_key)
                if the_key != 'model' else
                # for 'model' field get short classname
                name_from_model(view.model)
            })
        return context


# Sidebar collapsable menus


class SideMenu:
    LEVEL0_ITEM_KEYS = ('name', 'legal_user')
    LEVEL0_ITEM_CONSTS = (
        ('settings', None),
        ('analitics', None),
        ('trading', None),
        ('production', None),
        ('finance', None),
        ('employees', None),
        ('admin', CustomUser.objects.get(username='b3admin')),
    )

    def get_named_level0_items():
        named_items = []
        for consts_line in SideMenu.LEVEL0_ITEM_CONSTS:
            the_dict = {}
            for the_key, the_val in zip(
                SideMenu.LEVEL0_ITEM_KEYS,
                consts_line
            ):
                the_dict.update({the_key: the_val})
            named_items.append(the_dict)
        return named_items

    @staticmethod
    def get_sidemenu_items():
        sidemenu_items = []
        # LEVEL0_ITEMS_KEYS: name, legal_user
        for level0_item_line in SideMenu.get_named_level0_items():
            # level0_items = [name, lc_name, [level1_items]]
            level1_items = []
            # TABSTARTER_KEYNAMES: level0_position, name,
            #   matrix_type, model, ...
            tabmaking_items_dictlist = TabStarterViewData.items_dictlist()
            for the_tabmaking_item_dict in list(filter(
                None,
                [
                    tabmaking_item_dict
                    if tabmaking_item_dict[
                        'level0_position'] == level0_item_line['name']
                    else None
                    for tabmaking_item_dict in tabmaking_items_dictlist
                ]
            )):
                # level1_items = [name, lc_name, matrix_type, "model"]
                level1_items.append([
                    the_tabmaking_item_dict['tab_cmd'],
                    LC_NAMES[
                        'side_or_pensil_'
                        + the_tabmaking_item_dict['tab_cmd']
                    ][lc_num],
                    the_tabmaking_item_dict['matrix_type'],
                    name_from_model(the_tabmaking_item_dict['model'])
                ])
            sidemenu_items.append([
                level0_item_line['name'],
                LC_NAMES[
                    'side_or_pensil_' + level0_item_line['name']][lc_num],
                level1_items,
            ])
        return sidemenu_items
