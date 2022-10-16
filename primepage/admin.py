from django.contrib import admin
from .models import Account
from .models import PartnerGroup
from .models import Partner
from .models import Material
from .models import HotEntry
from .models import MoneyEntry
from .models import KilledMoneyEntry
from .models import GoodsEntry
from .models import KilledGoodsEntry


#
class AccountAdmin(admin.ModelAdmin):
    list_display = ('number', )


admin.site.register(Account, AccountAdmin)


#
class PartnerGroupAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(PartnerGroup, PartnerGroupAdmin)


#
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Partner, PartnerAdmin)


#
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Material, MaterialAdmin)


#
class HotEntryAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(HotEntry, HotEntryAdmin)


#
class MoneyEntryAdmin(admin.ModelAdmin):
    list_display = ('humanid', )


admin.site.register(MoneyEntry, MoneyEntryAdmin)


#
class KilledMoneyEntryAdmin(admin.ModelAdmin):
    list_display = ('humanid', )


admin.site.register(KilledMoneyEntry, KilledMoneyEntryAdmin)


#
class GoodsEntryAdmin(admin.ModelAdmin):
    list_display = ('humanid', )


admin.site.register(GoodsEntry, GoodsEntryAdmin)


#
class KilledGoodsEntryAdmin(admin.ModelAdmin):
    list_display = ('humanid', )


admin.site.register(KilledGoodsEntry, KilledGoodsEntryAdmin)

