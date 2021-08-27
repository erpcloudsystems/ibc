# Copyright (c) 2013, erpcloud.systems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters, columns)
    return columns, data


def get_columns():
    return [
        {
            "label": _("Item Code"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 150
        },
        {
            "label": _("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "label": _("Item Group"),
            "fieldname": "item_group",
            "fieldtype": "Data",
            "width": 160
        },
        {
            "label": _("Brand"),
            "fieldname": "brand",
            "fieldtype": "Data",
            "width": 160
        },
        {
            "label": _("Summary Stock Qty"),
            "fieldname": "summary_stock",
            "fieldtype": "float",
            "width": 160
        },
        {
            "label": _("Not Summary Stock Qty"),
            "fieldname": "not_summary_stock",
            "fieldtype": "float",
            "width": 160
        },
        {
            "label": _("Total Stock"),
            "fieldname": "total_stock",
            "fieldtype": "float",
            "width": 160
        },
        {
            "label": _("Price List Rate"),
            "fieldname": "price_list_rate",
            "fieldtype": "Currency",
            "width": 160
        },
        {
            "label": _("Valuation Rate"),
            "fieldname": "valuation_rate",
            "fieldtype": "Currency",
            "width": 160
        },
        {
            "label": _("Added Value"),
            "fieldname": "added_value",
            "fieldtype": "Currency",
            "width": 160
        },
        {
            "label": _("Added Value / Cost"),
            "fieldname": "added_value_cost",
            "fieldtype": "Currency",
            "width": 160
        },
        {
            "label": _("Added Value / Price List Rate"),
            "fieldname": "added_value_pricelist",
            "fieldtype": "Currency",
            "width": 160
        }
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("date"):
        conditions += " and `tabStock Ledger Entry`.posting_date=%(date)s"

    item_results = frappe.db.sql("""
                                select distinct
                                        `tabItem`.name as item_code,
                                        `tabItem`.item_name as item_name,
                                        `tabItem`.item_group as item_group,   
                                        `tabItem`.brand as brand
                                from							
                                    `tabItem`
                                where
                                    `tabItem`.is_stock_item = 1
                                    and `tabItem`.disabled = 0
                
                                """, as_dict=1)

    result = []
    if item_results:
        for item_dict in item_results:
            data = {
                'item_code': item_dict.item_code,
                'item_name': item_dict.item_name,
                'item_group': item_dict.item_group,
                'brand': item_dict.brand,
            }
            result.append(data)
            itemo = item_dict.item_code
            dateo = filters.get("date")
            summary_stock_qty = 0
            not_summary_stock_qty = 0
            valuation_rts = 0
            price_lsts = 0
            valuation_rt = frappe.db.sql("""
                                            select
                                                 ifnull(valuation_rate,0) as value
                                                 from `tabStock Ledger Entry`
                                                 where
                                                 `tabStock Ledger Entry`.item_code = '{itemo}'
                                                 and `tabStock Ledger Entry`.warehouse = 'المخزن الرئيسي - IBC'
                                                 and `tabStock Ledger Entry`.posting_date <= '{dateo}'
                                                 and `tabStock Ledger Entry`.is_cancelled = 0
                                                 ORDER BY `tabStock Ledger Entry`.posting_date DESC, `tabStock Ledger Entry`.posting_time DESC, `tabStock Ledger Entry`.creation DESC LIMIT 1
                                        """.format(itemo=itemo, dateo=dateo),as_dict=1)
            price_lst = frappe.db.sql("""
                                           select
                                                ifnull(price_list_rate,0) as prices
                                                from `tabItem Price`
                                                where
                                                `tabItem Price`.item_code = '{itemo}'
                                                and `tabItem Price`.selling = 1
                                                and '{dateo}' between `tabItem Price`.valid_from and `tabItem Price`.valid_upto
                                               
                                       """.format(itemo=itemo, dateo=dateo), as_dict=1)
            for va in valuation_rt:
                valuation_rts = va.value
            data['valuation_rate'] = valuation_rts

            for pr in price_lst:
                price_lsts = pr.prices
            data['price_list_rate'] = price_lsts
            data['added_value'] = (price_lsts - valuation_rts)
            if valuation_rts>0:
                data['added_value_cost'] = ((price_lsts - valuation_rts)/valuation_rts*100)
            if price_lsts>0:
                data['added_value_pricelist'] = ((price_lsts - valuation_rts)/price_lsts*100)

            warehouses = frappe.db.sql("""select name as name from `tabWarehouse` where disabled = 0""", as_dict=1)
            for x in warehouses:

                warehouseo = x.name

                summary_stock_sql = frappe.db.sql("""
                                                    select
                                                         qty_after_transaction as summary_stock_
                                                         from `tabStock Ledger Entry` join `tabWarehouse` on `tabStock Ledger Entry`.warehouse = `tabWarehouse`.name
                                                         where
                                                         `tabStock Ledger Entry`.item_code = '{itemo}'
                                                         and `tabStock Ledger Entry`.warehouse = '{warehouseo}'
                                                         and `tabStock Ledger Entry`.posting_date <= '{dateo}'
                                                         and `tabStock Ledger Entry`.is_cancelled = 0
                                                         and `tabWarehouse`.summery_stock = 1
                                                         ORDER BY `tabStock Ledger Entry`.posting_date DESC, `tabStock Ledger Entry`.posting_time DESC, `tabStock Ledger Entry`.creation DESC LIMIT 1
                                                """.format(itemo=itemo, warehouseo=warehouseo, dateo=dateo), as_dict=1)
                for y in summary_stock_sql:
                    summary_stock_qty += y.summary_stock_

                not_summary_stock_sql = frappe.db.sql("""
                                                    select
                                                         qty_after_transaction as not_summary_stock_
                                                         from `tabStock Ledger Entry` join `tabWarehouse` on `tabStock Ledger Entry`.warehouse = `tabWarehouse`.name
                                                         where
                                                         `tabStock Ledger Entry`.item_code = '{itemo}'
                                                         and `tabStock Ledger Entry`.warehouse = '{warehouseo}'
                                                         and `tabStock Ledger Entry`.posting_date <= '{dateo}'
                                                         and `tabStock Ledger Entry`.is_cancelled = 0
                                                         and `tabWarehouse`.summery_stock = 0
                                                         ORDER BY `tabStock Ledger Entry`.posting_date DESC, `tabStock Ledger Entry`.posting_time DESC, `tabStock Ledger Entry`.creation DESC LIMIT 1
                                                """.format(itemo=itemo, warehouseo=warehouseo, dateo=dateo), as_dict=1)

                for z in not_summary_stock_sql:
                    not_summary_stock_qty += z.not_summary_stock_
            data['summary_stock'] = summary_stock_qty
            data['not_summary_stock'] = not_summary_stock_qty
            data['total_stock'] = summary_stock_qty + not_summary_stock_qty





    return result

def get_price_map(price_list_names, buying=0, selling=0):
    price_map = {}

    if not price_list_names:
        return price_map

    rate_key = "Buying Rate" if buying else "Selling Rate"
    price_list_key = "Buying Price List" if buying else "Selling Price List"

    filters = {"name": ("in", price_list_names)}
    if buying:
        filters["buying"] = 1
    else:
        filters["selling"] = 1

    pricing_details = frappe.get_all("Item Price",
        fields = ["name", "price_list", "price_list_rate"], filters=filters)

    for d in pricing_details:
        name = d["name"]
        price_map[name] = {
            price_list_key :d["price_list"],
            rate_key :d["price_list_rate"]
        }

    return price_map