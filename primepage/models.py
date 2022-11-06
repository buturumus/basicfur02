# primepage/models.py

import logging  # noqa 
from django.db import models
from users.models import CustomUser
# from datetime import date
from datetime import datetime
# from misc import common_classes
from misc.common_classes import Initable
from misc.common_classes import ClassNameGetter
from .lc_data import LcData

# shortnames
name_from_model = ClassNameGetter.name_from_model
lc = LcData.lc
lc_num = LcData.lc_num
LC_NAMES = LcData.LC_NAMES


class SaveRememberer:

    @staticmethod
    def get_written_by_backend(request):
        return {
            'created_by': request.user,
            'create_date': datetime.now(),
        }

    def get_absolute_url(self):
        return '.'


class Account(models.Model, Initable, ClassNameGetter):
    DEFAULT_KEYS = ('number', )
    DEFAULT_VALS = (
        '00', '05', '06', '20', '41', '46', '50/1',
        '51', '62', '71', '72/1', '80', '80/1',
    )

    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=8)

    def __str__(self):
        return self.number + ' - ' + LC_NAMES[f'acc_{self.number}'][lc_num]


class PartnerGroup(models.Model, Initable, ClassNameGetter):
    DEFAULT_KEYS = ('name', )
    DEFAULT_VALS = ('employees', )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


class Partner(models.Model, ClassNameGetter, SaveRememberer):
    id = models.AutoField(primary_key=True)
    name = models.CharField('', max_length=50)
    last_name = models.CharField(
        '',
        max_length=50,
        default='',
        null=True,
        blank=True,
    )
    partner_group = models.ForeignKey(
        PartnerGroup,
        verbose_name='',
        related_name='partner_partner_group',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    create_date = models.DateTimeField(
        # default=datetime(1970, 1, 1, 0, 0, 0, 0)
    )
    created_by = models.ForeignKey(
        # 'users.CustomUser',
        CustomUser,
        related_name='partner_created_by',
        # default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    # initial data for forms
    @staticmethod
    def get_initials(request):
        return {
        }

    def __str__(self):
        return self.name


class Material(models.Model, ClassNameGetter, SaveRememberer):
    id = models.AutoField(primary_key=True)
    name = models.CharField('', max_length=256)
    create_date = models.DateTimeField(
        default=datetime(1970, 1, 1, 0, 0, 0, 0))
    created_by = models.ForeignKey(
        CustomUser,
        related_name='material_created_by',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class HotEntry(models.Model, Initable, ClassNameGetter):
    DEFAULT_KEYS = ('name', )
    DEFAULT_VALS = (
        'service',
        'shipping',
        'mat_to_prod',
        'get_invoice',
        'make_invoice',
        'from_bank',
        'to_bank',
        'to_stock',
        'consumable_purchase',
        'mat_purchase',
        'pay_salary',
        'calc_salary',
        'accountable_cache_out',
        'accountable_cache_return',
        'accountable_cache_spent',
        'cache_out',
        'cache_in',
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, default='')

    def __str__(self):
        return LC_NAMES[f'hot_entry_{self.name}'][lc_num]


class MoneyEntry(models.Model, ClassNameGetter, SaveRememberer):
    id = models.AutoField(primary_key=True)
    humanid = models.CharField(
        max_length=32,
        blank=True,
        default='')
    parent_money_entry = models.ForeignKey(
        'self',
        related_name='money_entry_parent_entry',
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
        related_name='money_entry_hot_entry',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    date = models.DateField()
    partner = models.ForeignKey(
        Partner,
        related_name='money_entry_partner',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    employee = models.ForeignKey(
        Partner,
        related_name='money_entry_employee',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    deb_account = models.ForeignKey(
        Account,
        related_name='money_entry_dr',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    cred_account = models.ForeignKey(
        Account,
        related_name='money_entry_cr',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    comment = models.CharField(max_length=256, blank=True)
    create_date = models.DateTimeField(
        default=datetime(1970, 1, 1, 0, 0, 0, 0))
    created_by = models.ForeignKey(
        # 'users.CustomUser',
        CustomUser,
        related_name='money_entry_created_by',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    # has_goodslines = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.humanid


class KilledMoneyEntry(models.Model, ClassNameGetter, SaveRememberer):
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
    deb_account = models.ForeignKey(
        Account,
        related_name='killed_money_entry_dr',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    cred_account = models.ForeignKey(
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
        related_name='killed_money_entry_created_by',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    kill_date = models.DateTimeField(default='1970-01-01')
    killed_by = models.ForeignKey(
        # 'users.CustomUser',
        CustomUser,
        related_name='killed_money_entry_killed_by',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    has_goods_entries = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.humanid


class GoodsEntry(models.Model, ClassNameGetter, SaveRememberer):
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
        related_name='goods_entry_created_by',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.humanid
        # return str(self.comment)


class KilledGoodsEntry(models.Model, ClassNameGetter, SaveRememberer):
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
        related_name='killed_goods_entry_created_by',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.humanid
        # return str(self.comment)


# DB'less classes


class MultimodelMatrixSummary:

    def get_context_data(self, *args, **kwargs):
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
                        self.model._meta.get_field(f'{shown_key}_id')
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
                        self.pk,
                    ]
                    for shown_key, cls in zip(
                        MATRIX_CONSTS['summary']['shown_keys'][
                            self.model],
                        MATRIX_CONSTS['summary']['cell_html_classes'][
                            self.model]
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
        return context


class MultimodelMatrixEdit:

    def get_context_data(self, *args, **kwargs):
        object_keyvals = kwargs['object_keyvals']
        form = kwargs['form']
        context = {}
        # upd.context with selected object's keyvalues
        context.update({
            'headers_cells_form_zip':
            zip(
                # object_keyvals_and_cls
                [
                    [
                        # key
                        shown_key,
                        # value
                        getattr(object_keyvals, shown_key)
                        if (
                            hasattr(object_keyvals, shown_key)
                            and getattr(object_keyvals, shown_key)
                        ) else
                        self.model._meta.get_field(f'{shown_key}_id')
                            .related_model
                            .objects.get(id=getattr(
                                object_keyvals, f'{shown_key}_id'))
                        if (
                            hasattr(object_keyvals, f'{shown_key}_id')
                            and getattr(object_keyvals, f'{shown_key}_id')
                        ) else
                        '',
                        # cell html class
                        cls,
                        # # is_hidden flag
                        # 1 if shown_key in MATRIX_CONSTS['edit'][
                        #     'hidden_keys'][self.model] else 0
                    ]
                    for shown_key, cls in zip(
                        (
                            MATRIX_CONSTS['edit']['shown_keys'][
                                self.model]
                        ),
                        MATRIX_CONSTS['edit']['cell_html_classes'][
                            self.model]
                    )
                ],
                # headers_names_and_cls
                [
                    [lc(name_key), cls]
                    for name_key, cls in zip(
                        MATRIX_CONSTS['edit'][
                            'header_names_keys'][self.model],
                        MATRIX_CONSTS['edit'][
                            'header_html_classes'][self.model]
                    )
                ],
                # form data
                form,
            )
        })
        return context


# Class for all tab calling elements


class TabStarter:
    TABSTARTER_KEYNAMES = (
        'level0_position',  # added in loop list
        'tab_cmd',
        'matrix_type',
        'model',
        'pensil_tab_cmd',
    )
    TABSTARTER_CONSTS = (
        [['settings'] + i for i in [
            ['service_entry',
                'edit', MoneyEntry, '', ],
            ['money_entries_log',
                'summary', MoneyEntry, 'pensil_money_entry', ],
            ['partners_list',
                'summary', Partner, 'pensil_partner', ],
            ['new_partner',
                'edit', Partner, '', ],
            ['materials_list',
                'summary', Material, 'pensil_material', ],
            ['new_material',
                'edit', Material, '', ],
            ['killed_money_entries_log',
                'summary', MoneyEntry, '', ],
        ]]
        + [['analitics'] + i for i in [
            ['acc_sum_card',
                'acc_sum_card', MoneyEntry, '', ],
            ['inventories',
                'inventories', GoodsEntry, '', ],
            ['in_stock',
                'in_stock', GoodsEntry, '', ],
            ['partners_balance',
                'partners_balance', Partner, '', ],
            ['material_history',
                'material_history', GoodsEntry, '', ],
        ]]
        + [['trading'] + i for i in [
            ['shipping',
                'edit', MoneyEntry, '', ],
            ['make_invoice',
                'edit', MoneyEntry, '', ],
            ['get_invoice',
                'edit', MoneyEntry, '', ],
        ]]
        + [['production'] + i for i in [
            ['materials_purchase',
                'edit', MoneyEntry, '', ],
            ['materials_to_production',
                'edit', MoneyEntry, '', ],
            ['consumables_purchase',
                'edit', MoneyEntry, '', ],
            ['production_to_stock',
                'edit', MoneyEntry, '', ],
        ]]
        + [['finance'] + i for i in [
            ['cache_in',
                'edit', MoneyEntry, '', ],
            ['cache_out',
                'edit', MoneyEntry, '', ],
            ['to_bank',
                'edit', MoneyEntry, '', ],
            ['from_bank',
                'edit', MoneyEntry, '', ],
        ]]
        + [['employees'] + i for i in [
            ['calc_salary',
                'edit', MoneyEntry, '', ],
            ['pay_salary',
                'edit', MoneyEntry, '', ],
            ['accountable_cache_out',
                'edit', MoneyEntry, '', ],
            ['accountable_cache_return',
                'edit', MoneyEntry, '', ],
            ['accountable_cache_spent',
                'edit', MoneyEntry, '', ],
        ]]
        + [['admin'] + i for i in [
            ['wipe_entries',
                'wipe_entries', '', '', ],
        ]]
        + [['nosidebar'] + i for i in [
            ['pensil_partner',
                'edit', Partner, '', ],
            ['pensil_material',
                'edit', Material, '', ],
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
        for consts_line in TabStarter.TABSTARTER_CONSTS:
            the_dict = {}
            for the_key, the_val in zip(
                TabStarter.TABSTARTER_KEYNAMES,
                consts_line
            ):
                the_dict.update({the_key: the_val})
            named_items.append(the_dict)
        return named_items

    # get std.tabstarter's context keyvals
    def get_context_data(self):
        TABSTARTER_CONTEXT_KEYS = (
            'tab_cmd',
            'matrix_type',
            'model',
            'pensil_tab_cmd',
        )
        context = {}
        # fill context with values from tabmaking constants' dictlist
        # # for the_key in DataForAnypart.tabmaking_context_keys:
        for the_key in TABSTARTER_CONTEXT_KEYS:
            context.update({
                the_key:
                getattr(self, the_key)
                if the_key != 'model' else
                # for 'model' field get short classname
                name_from_model(self.model)
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
            tabmaking_items_dictlist = TabStarter.items_dictlist()
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


# Pensil clicks


PENSIL_CONSTS = (
    ['pensil_partner', 'edit', Partner, ],
)


MATRIX_CONSTS = {
    'summary': {
        'shown_keys': {
            Partner: (
                'name',
                'last_name',
                'partner_group',
                # pensil,
            ),
            Material: (
                'name',
                '',
                # pensil,
            ),
            MoneyEntry: (
                'humanid',
                'date',
                'partner',
                'hot_entry',
                'deb_account',
                'cred_account',
                'money',
                'comment',
                # pensil,
            ),
        },
        'header_names_keys': {
            Partner: (
                'summary_partner_name1',
                'summary_partner_name2',
                'summary_partner_group',
            ),
            Material: (
                'summary_material_name',
                '',
            ),
            MoneyEntry: (
                'summary_m_entry_humanid',
                'summary_m_entry_date',
                'summary_m_entry_partner',
                'summary_m_entry_hot_entry',
                'summary_m_entry_deb_account',
                'summary_m_entry_cred_account',
                'summary_m_entry_money',
                'summary_m_entry_comment',
            ),
        },
        'header_html_classes': {
            Partner: (
                'col-5 text-left',
                'col-4 text-left',
                'col-2 text-left',
            ),
            Material: (
                'col-7 text-left',
                'col-4',
            ),
            MoneyEntry: (
                'col-1',
                'col-1 text-right',
                'col-2',
                'col-1',
                'col-1 text-center',
                'col-1 text-center',
                'col-1 text-right',
                'col-3',
            ),
        },
        'cell_html_classes': {
            Partner: (
                'text-left',
                'text-left',
                'text-left',
            ),
            Material: (
                'text-left',
                '',
            ),
            MoneyEntry: (
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
    },

    'edit': {
        'shown_keys': {
            Partner: (
                'name',
                'last_name',
                'partner_group',
                # pensil,
            ),
            Material: (
                'name',
                # '',
                # pensil,
            ),
            MoneyEntry: (
                'humanid',
                'date',
                'partner',
                'hot_entry',
                'deb_account',
                'cred_account',
                'money',
                'comment',
                # pensil,
            ),
        },
        'header_names_keys': {
            Partner: (
                'edit_partner_name1',
                'edit_partner_name2',
                'edit_partner_group',
            ),
            Material: (
                'edit_material_name',
                # '',
            ),
            MoneyEntry: (
                'edit_m_entry_humanid',
                'edit_m_entry_date',
                'edit_m_entry_partner',
                'edit_m_entry_hot_entry',
                'edit_m_entry_deb_account',
                'edit_m_entry_cred_account',
                'edit_m_entry_money',
                'edit_m_entry_comment',
            ),
        },
        'header_html_classes': {
            Partner: (
                'col-4 text-left',
                'col-4 text-left',
                'col-4 text-left',
            ),
            Material: (
                'col-4 text-left',
                # '',
            ),
            MoneyEntry: (
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
        'cell_html_classes': {
            Partner: (
                'text-left',
                'text-left',
                'text-left',
            ),
            Material: (
                'text-left',
                # '',
            ),
            MoneyEntry: (
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
    },
}


