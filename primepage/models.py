# primepage/models.py

import logging  # noqa 
from django.db import models
from users.models import CustomUser
# from datetime import date
from datetime import datetime
# from misc import common_classes
from misc import lc_strings
from misc.common_classes import Initable
from misc.common_classes import ClassNameGetter
from misc.common_functions import dict_list_search
from misc.common_functions import lc
# shortnames
name_from_model = ClassNameGetter.name_from_model
LC_NAMES = lc_strings.LC_NAMES
lc_num = lc_strings.lc_num


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


class Partner(models.Model, ClassNameGetter):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    last_name = models.CharField(
        max_length=50,
        default='',
        null=True,
        blank=True,
    )
    create_date = models.DateTimeField(
        default=datetime(1970, 1, 1, 0, 0, 0, 0))
    partner_group = models.ForeignKey(
        PartnerGroup,
        related_name='partner_partner_group',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        # 'users.CustomUser',
        CustomUser,
        related_name='partner_created_by',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Material(models.Model, ClassNameGetter):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
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


class MoneyEntry(models.Model, ClassNameGetter):
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


class KilledMoneyEntry(models.Model, ClassNameGetter):
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


class GoodsEntry(models.Model, ClassNameGetter):
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


class KilledGoodsEntry(models.Model, ClassNameGetter):
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


class DataForAnypart:
    tabmaking_items_to_context_keys = (
        'tab_cmd',
        'matrix_type',
        'model',
        'pensil_tab_cmd',
    )

    def get_extra_context(self, *args, **kwargs):
        extra_context = {}
        # fill context with values from tabmaking constants' dictlist
        for the_key in DataForAnypart.tabmaking_items_to_context_keys:
            extra_context.update({
                the_key:
                dict_list_search(
                    TabmakingItems.items_dictlist(),
                    'tab_cmd',
                    self.tab_cmd,
                    the_key
                ) if the_key != 'model' else
                # for 'model' field get short classname
                name_from_model(
                    dict_list_search(
                        TabmakingItems.items_dictlist(),
                        'tab_cmd',
                        self.tab_cmd,
                        the_key
                    )
                )
            })
        # add  manually
        extra_context.update({
            'pk': self.pk,
        })
        return extra_context


class DataForSimplepartAnymodel:
    extra_context_keys = ()

    def get_extra_context(self, *arr_x_masks, **kwargs):
        extra_context = {}
        for the_key in self.__class__.extra_context_keys:
            extra_context.update({the_key: lc(the_key)})
        # add  manually
        extra_context.update({
            'lc_tab_title':
            lc('side_or_pensil_' + self.tab_cmd)
        })
        return extra_context


class DataForBodieSummaryAnymodel(DataForSimplepartAnymodel):
    extra_context_keys = (
        'btn_f5',
        'btn_close',
    )


class DataForBodieEditAnymodel(DataForSimplepartAnymodel):
    extra_context_keys = (
        'btn_close_not_save',
        'btn_save_close',
        'btn_delete',
    )


class DataForMatrixSummaryAnymodel:

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

                        cls,
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


class DataForMatrixEditAnymodel:

    def get_context_data(self, *args, **kwargs):
        object_keyvals = kwargs['object_keyvals']
        context = {}
        # upd.context with selected object's keyvalues 
        context.update({
            'headers_cells_zip':
            zip(
                # object_keyvals_and_cls
                [
                    [
                        getattr(object_keyvals, shown_key)
                        if ( hasattr(object_keyvals, shown_key)
                            and getattr(object_keyvals, shown_key)
                        ) else
                        self.model._meta.get_field(f'{shown_key}_id')
                            .related_model
                            .objects.get(id=getattr(
                                object_keyvals, f'{shown_key}_id'))
                        if ( hasattr(object_keyvals, f'{shown_key}_id')
                            and getattr(object_keyvals, f'{shown_key}_id')
                        ) else
                        '',

                        cls
                    ]
                    for shown_key, cls in zip(
                        MATRIX_CONSTS['edit']['shown_keys'][
                            self.model],
                        MATRIX_CONSTS['edit']['cell_html_classes'][
                            self.model]
                    )
                ],
                # headers_names_and_cls
                [
                    [ lc(name_key), cls]
                    for name_key, cls in zip(
                        MATRIX_CONSTS['edit'][
                            'header_names_keys'][self.model],
                        MATRIX_CONSTS['edit'][
                            'header_html_classes'][self.model]
                    )
                ]
            )
        })
        return context


# Class for all tabmaking elements(which can call a new tab)


class TabmakingItems:
    TABMAKING_ITEM_KEYS = (
        'level0_parent_name',  # added in loop list
        'tab_cmd',
        'matrix_type',
        'model',
        'pensil_tab_cmd',
    )
    TABMAKING_ITEMS_CONSTS = (
        [['settings'] + i for i in [
            ['service_entry', 'edit', MoneyEntry, '', ],
            ['money_entries_log', 'summary', MoneyEntry, 'pensil_money_entry', '', ],
            ['partners_list', 'summary', Partner, 'pensil_partner', '', ],
            ['new_partner', 'edit', Partner, '', ],
            ['materials_list', 'summary', Material, 'pensil_material', '', ],
            ['new_material', 'edit', Material, '', ],
            ['killed_money_entries_log', 'summary', MoneyEntry, '', ],
        ]]
        + [['analitics'] + i for i in [
            ['acc_sum_card', 'acc_sum_card', MoneyEntry, '', ],
            ['inventories', 'inventories', GoodsEntry, '', ],
            ['in_stock', 'in_stock', GoodsEntry, '', ],
            ['partners_balance', 'partners_balance', Partner, '', ],
            ['material_history', 'material_history', GoodsEntry, '', ],
        ]]
        + [['trading'] + i for i in [
            ['shipping', 'edit', MoneyEntry, '', ],
            ['make_invoice', 'edit', MoneyEntry, '', ],
            ['get_invoice', 'edit', MoneyEntry, '', ],
        ]]
        + [['production'] + i for i in [
            ['materials_purchase', 'edit', MoneyEntry, '', ],
            ['materials_to_production', 'edit', MoneyEntry, '', ],
            ['consumables_purchase', 'edit', MoneyEntry, '', ],
            ['production_to_stock', 'edit', MoneyEntry, '', ],
        ]]
        + [['finance'] + i for i in [
            ['cache_in', 'edit', MoneyEntry, '', ],
            ['cache_out', 'edit', MoneyEntry, '', ],
            ['to_bank', 'edit', MoneyEntry, '', ],
            ['from_bank', 'edit', MoneyEntry, '', ],
        ]]
        + [['employees'] + i for i in [
            ['calc_salary', 'edit', MoneyEntry, '', ],
            ['pay_salary', 'edit', MoneyEntry, '', ],
            ['accountable_cache_out', 'edit', MoneyEntry, '', ],
            ['accountable_cache_return', 'edit', MoneyEntry, '', ],
            ['accountable_cache_spent', 'edit', MoneyEntry, '', ],
        ]]
        + [['admin'] + i for i in [
            ['wipe_entries', 'wipe_entries', '', '', ],
        ]]
        + [['nosidebar'] + i for i in [
            ['pensil_partner', 'edit', Partner, '', ],
        ]]
    )

    @staticmethod
    def items_dictlist():
        named_items = []
        for consts_line in TabmakingItems.TABMAKING_ITEMS_CONSTS:
            the_dict = {}
            for the_key, the_val in zip(
                TabmakingItems.TABMAKING_ITEM_KEYS,
                consts_line
            ):
                the_dict.update({the_key: the_val})
            named_items.append(the_dict)
        return named_items

    @staticmethod
    def get_data_classname(tab_cmd, data_classname):
        return dict_list_search(TabmakingItems.items_dictlist(),
                                'tab_cmd',
                                tab_cmd,
                                data_classname)


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
            # TABMAKING_ITEM_KEYS: level0_parent_name, name,
            #   matrix_type, model, ...
            tabmaking_items_dictlist = TabmakingItems.items_dictlist()
            for the_tabmaking_item_dict in list(filter(
                None,
                [
                    tabmaking_item_dict
                    if tabmaking_item_dict[
                        'level0_parent_name'] == level0_item_line['name']
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
                'edit_partner_name1',
                'edit_partner_name2',
                'edit_partner_group',
            ),
            Material: (
                'edit_material_name',
                '',
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
