# primepage/lc_strings.py

import logging  # noqa 


class LcData:

    lc_num = 0
    LC_NAMES = {
        'brand': (
            'BasicFur - production, inventories, stock',
        ),
        # models
        # account chart names
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
        # hot entries list
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
        # ui
        # sidebar
        'sidebar_from_date': ('from', ),
        'sidebar_to_date': ('to', ),
        'sidebar_date_hint': ('date', ),
        'side_or_pensil_service_entry': ('Service entry', ),
        'side_or_pensil_settings': ('Settings', ),
        'side_or_pensil_money_entries_log': ('Transactions log', ),
        'side_or_pensil_partners_list': ('Partners list', ),
        'side_or_pensil_new_partner': ('New partner', ),
        'side_or_pensil_materials_list': ('Materials list', ),
        'side_or_pensil_new_material': ('New material', ),
        'side_or_pensil_killed_money_entries_log': ('Del.transations log', ),
        'side_or_pensil_analitics': ('Analitics', ),
        'side_or_pensil_acc_sum_card': ('Acc.summary card', ),
        'side_or_pensil_inventories': ('Inventories', ),
        'side_or_pensil_in_stock': ('In stock', ),
        'side_or_pensil_partners_balance': ('Balance by partners', ),
        'side_or_pensil_material_history': ('Material\'s history', ),
        'side_or_pensil_trial_balance': ('Trial balance', ),
        'side_or_pensil_trading': ('Trading', ),
        'side_or_pensil_shipping': ('Shipping', ),
        'side_or_pensil_make_invoice': ('Make invoice', ),
        'side_or_pensil_get_invoice': ('Get invoice', ),
        'side_or_pensil_production': ('Production', ),
        'side_or_pensil_materials_purchase': ('Buy goods/svc', ),
        'side_or_pensil_materials_to_production': ('Mater.to production', ),
        'side_or_pensil_consumables_purchase': ('Purch.of consum.mater.', ),
        'side_or_pensil_production_to_stock': ('Prod.to stock', ),
        'side_or_pensil_finance': ('Finance', ),
        'side_or_pensil_cache_in': ('Cash in', ),
        'side_or_pensil_cache_out': ('Cash out', ),
        'side_or_pensil_to_bank': ('To banc.acc.', ),
        'side_or_pensil_from_bank': ('From banc.acc.', ),
        'side_or_pensil_employees': ('Employees', ),
        'side_or_pensil_calc_salary': ('Calc.salary', ),
        'side_or_pensil_pay_salary': ('Pay salary', ),
        'side_or_pensil_accountable_cache_out': ('Accountable cache out', ),
        'side_or_pensil_accountable_cache_return': (
            'Accountable cache return', ),
        'side_or_pensil_accountable_cache_spent': ('Accountable cache spent', ),
        'side_or_pensil_admin': ('Admin.tasks', ),
        'side_or_pensil_wipe_entries': ('Wipe entries', ),
        # pensils
        'side_or_pensil_pensil_partner': ('Edit partner', ),
        'side_or_pensil_pensil_material': ('Edit material', ),
        'side_or_pensil_pensil_money_entry': ('Edit entry', ),
        # common tab bodie buttons
        'btn_f5': ('Reload', ),
        'btn_add': ('Add', ),
        'btn_close': ('Close', ),
        'btn_close_not_save': ('Close w/o save', ),
        'btn_delete': ('Delete', ),
        'btn_save_close_m_entry': ('Save and close', ),
        'btn_save_close': ('Save and close', ),
        # summary matrixx
        'summary_partner_name1': ('Name', ),
        'summary_partner_name2': ('Name2', ),
        'summary_partner_group': ('In group', ),
        'summary_material_name': ('Name', ),
        'summary_m_entry_humanid': ('ID', ),
        'summary_m_entry_date': ('Op.date', ),
        'summary_m_entry_partner': ('Partner', ),
        'summary_m_entry_hot_entry': ('Trans.type', ),
        'summary_m_entry_dr_acc': ('DebAcc', ),
        'summary_m_entry_cr_acc': ('CredAcc', ),
        'summary_m_entry_money': ('Sum', ),
        'summary_m_entry_comment': ('Comment', ),
        # edit matrixx
        'edit_partner_name1': ('Name', ),
        'edit_partner_name2': ('Name2', ),
        'edit_partner_group': ('Is in group', ),
        'edit_material_name': ('Name', ),
        'edit_m_entry_humanid': ('ID:', ),
        'edit_m_entry_date': ('Date:', ),
        'edit_m_entry_partner': ('Partner:', ),
        'edit_m_entry_hot_entry': ('Ent.type:', ),
        'edit_m_entry_money': ('Sum:', ),
        'edit_m_entry_comment': ('Comm.:', ),
        'edit_m_entry_dr_acc': ('DR Acc:', ),
        'edit_m_entry_cr_acc': ('CR Acc:', ),
        'edit_m_entry_details': ('Accounts...:', ),
        # 'edit_m_entry_has_goodslines': ('Cont.goods', ),
        # 'edit_m_entry_create_date': ('Chng.date', ),
        # 'edit_m_entry_created_by': ('Chng.by', ),
        # 'edit_m_entry_employee': ('Employee:', ),
        # 'edit_m_entry_details': ('Details...', ),
        # 'edit_m_entry_add_acc': ('Add acc.', ),
        # 'edit_m_entry_kill_date': ('Del.date', ),
        # 'edit_m_entry_killed_by': ('Del.by', ),
        # yes-no screen
        'yesno_sure_question': ('Are you sure?', ),
        'yesno_no_answer': ('No, cansel', ),
        'yesno_yes_answer': ('Yes, continue', ),
    }

    def lc(name):
        return (
            LcData.LC_NAMES[name][LcData.lc_num]
            if name else ''
        )

    def get_context_data(self, *args, **kwargs):
        context = {}
        for the_key in self.label_keys_to_localize:
            context.update({the_key: LcData.lc(the_key)})
        for the_key in self.tabclick_keys_to_localize:
            context.update(
                {the_key: LcData.lc('side_or_pensil_' + self.tab_cmd)}
            )
        return context

