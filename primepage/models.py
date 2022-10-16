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
name_from_model = ClassNameGetter.name_from_model   # shortname


class Account(models.Model, Initable, ClassNameGetter):
    DEFAULT_KEYS = ('number', )
    DEFAULT_VALS = (
        '00', '05', '06', '20', '41', '46', '50/1',
        '51', '62', '71', '72/1', '80', '80/1',
    )

    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=8)

    def __str__(self):
        return ('acc_'
                + f'{lc_strings.LC_NAMES[self.name][lc_strings.lc_num]}')


class PartnerGroup(models.Model, Initable, ClassNameGetter):
    DEFAULT_KEYS = ('name', )
    DEFAULT_VALS = ('employees', )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='')

    def __str__(self):
        return ('partner_group_'
                + f'{lc_strings.LC_NAMES[self.name][lc_strings.lc_num]}')


class Partner(models.Model, ClassNameGetter):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, default='')
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
        return ('hot_entry_'
                + f'{lc_strings.LC_NAMES[self.name][lc_strings.lc_num]}')


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
    has_goodslines = models.SmallIntegerField(default=0)

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


class DataForAnypart:
    extra_context_keys = (
        'tab_cmd',
        'matrix_type',
        'model',
        # bodie_data_classname'
    )

    def get_extra_context(self):
        extra_context = {}
        # fill context with values from tabmaking constants' dictlist
        for the_key in DataForAnypart.extra_context_keys:
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
        return extra_context


class DataForSimplepartAnymodel:
    extra_context_keys = (
        'btn_f5',
        'btn_close',
    )

    def get_extra_context(self):
        extra_context = {}
        for the_key in DataForSimplepartAnymodel.extra_context_keys:
            extra_context.update({the_key: lc(the_key)})
        # add  manually
        extra_context.update({
            'lc_tab_title':
            lc('sidemenu_' + self.tab_cmd)
        })
        return extra_context


# Class for all tabmaking elements(which can call a new tab)


class TabmakingItems:
    TABMAKING_ITEM_KEYS = (
        'level0_parent_name',  # added in loop list
        'tab_cmd',
        'matrix_type',
        'model',
        # 'bodie_data_classname',
        # 'matrix_data_classname',
    )
    TABMAKING_ITEMS_CONSTS = (
        [['settings'] + i for i in [
            ['service_entry', 'edit', MoneyEntry, ],
            ['money_entries_log', 'summary', MoneyEntry,
            #    '', DataForShownMatrixSummaryAnymodel
            ],
            ['partners_list', 'summary', Partner,
            #    '', DataForShownMatrixSummaryAnymodel
            ],
            ['new_partner', 'edit', Partner, ],
            ['materials_list', 'summary', Material,
            #   '', DataForShownMatrixSummaryAnymodel
            ],
            ['new_material', 'edit', Material, ],
            ['killed_money_entries_log', 'summary', MoneyEntry, ],
        ]]
        + [['analitics'] + i for i in [
            ['acc_sum_card', 'acc_sum_card', MoneyEntry, ],
            ['inventories', 'inventories', GoodsEntry, ],
            ['in_stock', 'in_stock', GoodsEntry, ],
            ['partners_balance', 'partners_balance', Partner, ],
            ['material_history', 'material_history', GoodsEntry, ],
        ]]
        + [['trading'] + i for i in [
            ['shipping', 'edit', MoneyEntry, ],
            ['make_invoice', 'edit', MoneyEntry, ],
            ['get_invoice', 'edit', MoneyEntry, ],
        ]]
        + [['production'] + i for i in [
            ['materials_purchase', 'edit', MoneyEntry, ],
            ['materials_to_production', 'edit', MoneyEntry, ],
            ['consumables_purchase', 'edit', MoneyEntry, ],
            ['production_to_stock', 'edit', MoneyEntry, ],
        ]]
        + [['finance'] + i for i in [
            ['cache_in', 'edit', MoneyEntry, ],
            ['cache_out', 'edit', MoneyEntry, ],
            ['to_bank', 'edit', MoneyEntry, ],
            ['from_bank', 'edit', MoneyEntry, ],
        ]]
        + [['employees'] + i for i in [
            ['calc_salary', 'edit', MoneyEntry, ],
            ['pay_salary', 'edit', MoneyEntry, ],
            ['accountable_cache_out', 'edit', MoneyEntry, ],
            ['accountable_cache_return', 'edit', MoneyEntry, ],
            ['accountable_cache_spent', 'edit', MoneyEntry, ],
        ]]
        + [['admin'] + i for i in [
            ['wipe_entries', 'wipe_entries', '', ],
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
                    lc_strings.LC_NAMES[
                        'sidemenu_'
                        + the_tabmaking_item_dict['tab_cmd']
                    ][lc_strings.lc_num],
                    the_tabmaking_item_dict['matrix_type'],
                    name_from_model(the_tabmaking_item_dict['model'])
                ])
            sidemenu_items.append([
                level0_item_line['name'],
                lc_strings.LC_NAMES[
                    'sidemenu_' + level0_item_line['name']][lc_strings.lc_num],
                level1_items,
            ])
        return sidemenu_items


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
                # pensil,
            ),
        },
        'header_names_keys': {
            Partner: (
                'summary_parter_name1',
                'summary_parter_name2',
                'summary_parter_group',
                '',
            ),
            Material: (
                'summary_material_name',
                '',
            ),
        },
        'header_html_classes': {
            Partner: (
                'col-5 text-left',
                'col-4 text-left',
                'col-2 text-left',
                'col-1',
            ),
            Material: (
                'col-10 text-left',
                'col-2',
            ),
        },
    },
    'edit': {
        'shown_keys': {
            Partner: (
            ),
        },
        'header_names_keys': {
            Partner: (
            ),
        },
        'header_html_classes': {
            Partner: (
            ),
        },
        'cell_html_classes': {
            Partner: (
            ),
        },
    },
}
