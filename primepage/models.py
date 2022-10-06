# primepage/models.py

from django.db import models
from users.models import CustomUser
# from datetime import date
from datetime import datetime
from misc import common_classes
from misc import lc_strings
import logging  # noqa 


class Account(models.Model, common_classes.Initable):
    DEFAULT_KEYS = ('number', )
    DEFAULT_VALS = (
        '00', '05', '06', '20', '41', '46', '50/1',
        '51', '62', '71', '72/1', '80', '80/1',
    )

    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=8)

    def __str__(self):
        return ('acc_'
                + f'{lc_strings.LC_NAMES[self.name][lc_strings.lc_id]}')


class PartnerGroup(models.Model, common_classes.Initable):
    DEFAULT_KEYS = ('name', )
    DEFAULT_VALS = ('employees', )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='')

    def __str__(self):
        return ('partner_group_'
                + f'{lc_strings.LC_NAMES[self.name][lc_strings.lc_id]}')


class Partner(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
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


class Material(models.Model):
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


class HotEntry(models.Model, common_classes.Initable):
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
                + f'{lc_strings.LC_NAMES[self.name][lc_strings.lc_id]}')


class MoneyEntry(models.Model):
    id = models.AutoField(primary_key=True)
    human_id = models.CharField(
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
        return self.human_id


class KilledMoneyEntry(models.Model):
    id = models.AutoField(primary_key=True)
    human_id = models.CharField(
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
        return self.human_id


class GoodsEntry(models.Model):
    id = models.AutoField(primary_key=True)
    human_id = models.CharField(
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
        return self.human_id
        # return str(self.comment)


class KilledGoodsEntry(models.Model):
    id = models.AutoField(primary_key=True)
    human_id = models.CharField(
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
        return self.human_id
        # return str(self.comment)


# sidebar collapsable menus

# dbaseless class
class SideMenu:
    SIDEMENU_ITEMS = (
        # (name, legal_user, (level1_items))
        (
            'settings',
            '',
            (
                # name, matrix_type, model
                ('service_entry', 'edit', MoneyEntry),
                ('money_entries_log', 'summary', MoneyEntry),
                ('partners_list', 'summary', Partner),
                ('new_partner', 'edit', Partner),
                ('materials_list', 'summary', Material),
                ('new_material', 'edit', Material),
                ('killed_money_entries_log', 'summary', MoneyEntry),
            ),
        ),
        (
            'analitics',
            '',
            (
                ('acc_sum_card', 'acc_sum_card', MoneyEntry),
                ('inventories', 'inventories', GoodsEntry),
                ('in_stock', 'in_stock', GoodsEntry),
                ('partners_balance', 'partners_balance', Partner),
                ('material_history', 'material_history', GoodsEntry),
                ('trial_balance', 'trial_balance', Account),
            ),
        ),
        (
            'trading',
            '',
            (
                ('shipping', 'edit', MoneyEntry),
                ('make_invoice', 'edit', MoneyEntry),
                ('get_invoice', 'edit', MoneyEntry),
            ),
        ),
        (
            'production',
            '',
            (
                ('materials_purchase', 'edit', MoneyEntry),
                ('materials_to_production', 'edit', MoneyEntry),
                ('consumables_purchase', 'edit', MoneyEntry),
                ('production_to_stock', 'edit', MoneyEntry),
            ),
        ),
        (
            'finance',
            '',
            (
                ('cache_in', 'edit', MoneyEntry),
                ('cache_out', 'edit', MoneyEntry),
                ('to_bank', 'edit', MoneyEntry),
                ('from_bank', 'edit', MoneyEntry),
            ),
        ),
        (
            'employees',
            '',
            (
                ('calc_salary', 'edit', MoneyEntry),
                ('pay_salary', 'edit', MoneyEntry),
                ('accountable_cache_out', 'edit', MoneyEntry),
                ('accountable_cache_return', 'edit', MoneyEntry),
                ('accountable_cache_spent', 'edit', MoneyEntry),
            ),
        ),
        (
            'admin',
            # CustomUser.objects.get(username='b3admin'),
            '',
            (
                ('wipe_entries', 'wipe_entries', ''),
            ),
        ),
    )

    @staticmethod
    def get_template_items():
        sidemenu_items = []
        for old_level0_items in SideMenu.SIDEMENU_ITEMS:
            # [name, lc_name, [level1_items]]
            new_level1_items = []
            for old_level1_items in old_level0_items[2]:
                # [name, lc_name, matrix_type, model__name__]
                new_level1_items.append([
                    old_level1_items[0],
                    lc_strings.LC_NAMES[
                        'sidemenu_' + old_level1_items[0]][lc_strings.lc_id],
                    old_level1_items[1],
                    str(old_level1_items[2]).split('.')[-1].split('\'')[0],
                ])
            sidemenu_items.append([
                old_level0_items[0],
                lc_strings.LC_NAMES[
                    'sidemenu_' + old_level0_items[0]][lc_strings.lc_id],
                new_level1_items,
            ])
        return sidemenu_items

