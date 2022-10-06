# misc/lc_strings.py

lc_id = 0

LC_NAMES = {
    'brand': (
        'BasicFur - production, inventories, stock',
    ),
    'acc_00': ('Service', ),
    'acc_05': ('Inventories', ),
    'acc_06': ('Consumables', ),
    'acc_20': ('Production', ),
    'acc_41': ('Stock', ),
    'acc_46': ('Shipping', ),
    'acc_51': ('Bank account', ),
    'acc_62': ('Partners', ),
    'acc_50/1': ('Cash', ),
    'acc_71': ('Salaries', ),
    'acc_72/1': ('Petty cash', ),
    'acc_80': ('Profit', ),
    'acc_80/1': ('Owner1', ),
    'hot_entry_service': ('Srv.transaction', ),
    'hot_entry_shipping': ('Shipping', ),
    'hot_entry_mat_to_prod': ('Mater.to production', ),
    'hot_entry_get_invoice': ('Get invoice', ),
    'hot_entry_make_invoice': ('Make invoice', ),
    'hot_entry_from_bank': ('Transf.from account', ),
    'hot_entry_to_bank': ('Transf.to account', ),
    'hot_entry_to_stock': ('Prod.to stock', ),
    'hot_entry_consumable_purchase': ('Purch.of consumable', ),
    'hot_entry_mat_purchase': ('Buy goods/svc', ),
    'hot_entry_pay_salary': ('Pay salary', ),
    'hot_entry_calc_salary': ('Calc.salary', ),
    'hot_entry_accountable_cache_out': ('Accountable cache out', ),
    'hot_entry_accountable_cache_return': ('Accountable cache return', ),
    'hot_entry_accountable_cache_spent': ('Accountable cache spent', ),
    'hot_entry_cache_out': ('Cash out', ),
    'hot_entry_cache_in': ('Cash in', ),
    'partner_group_employees': ('Employees', ),
    'sidebar_from_date': ('from', ),
    'sidebar_to_date': ('to', ),
    'sidebar_date_hint': ('date', ),
    'sidemenu_service_entry': ('Service entry', ),
    'sidemenu_settings': ('Settings', ),
    'sidemenu_money_entries_log': ('Transactions log', ),
    'sidemenu_partners_list': ('Parnters list', ),
    'sidemenu_new_partner': ('New partner', ),
    'sidemenu_materials_list': ('Materials list', ),
    'sidemenu_new_material': ('New material', ),
    'sidemenu_killed_money_entries_log': ('Del.transations log', ),
    'sidemenu_analitics': ('Analitics', ),
    'sidemenu_acc_sum_card': ('Acc.summary card', ),
    'sidemenu_inventories': ('Inventories', ),
    'sidemenu_in_stock': ('In stock', ),
    'sidemenu_partners_balance': ('Balance by partners', ),
    'sidemenu_material_history': ('Material\'s history', ),
    'sidemenu_trial_balance': ('Trial balance', ),
    'sidemenu_trading': ('Trading', ),
    'sidemenu_shipping': ('Shipping', ),
    'sidemenu_make_invoice': ('Make invoice', ),
    'sidemenu_get_invoice': ('Get invoice', ),
    'sidemenu_production': ('Production', ),
    'sidemenu_materials_purchase': ('Buy goods/svc', ),
    'sidemenu_materials_to_production': ('Mater.to production', ),
    'sidemenu_consumables_purchase': ('Purch.of consum.mater.', ),
    'sidemenu_production_to_stock': ('Prod.to stock', ),
    'sidemenu_finance': ('Finance', ),
    'sidemenu_cache_in': ('Cash in', ),
    'sidemenu_cache_out': ('Cash out', ),
    'sidemenu_to_bank': ('To banc.acc.', ),
    'sidemenu_from_bank': ('From banc.acc.', ),
    'sidemenu_employees': ('Employees', ),
    'sidemenu_calc_salary': ('Calc.salary', ),
    'sidemenu_pay_salary': ('Pay salary', ),
    'sidemenu_accountable_cache_out': ('Accountable cache out', ),
    'sidemenu_accountable_cache_return': ('Accountable cache return', ),
    'sidemenu_accountable_cache_spent': ('Accountable cache spent', ),
    'sidemenu_admin': ('Admin.tasks', ),
    'sidemenu_wipe_entries': ('Wipe entries', ),
}