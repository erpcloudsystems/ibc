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
            "label": _("Sales Invoice"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 180
        },
        {
            "label": _("Posting Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 110
        },
        {
            "label": _("Customer"),
            "fieldname": "customer_name",
            "fieldtype": "Data",
            "width": 175
        },

        {
            "label": _("Item Code"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 90
        },
        {
            "label": _("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Qty"),
            "fieldname": "qty",
            "fieldtype": "float",
            "width": 80
        },
        {
            "label": _("UOM"),
            "fieldname": "stock_uom",
            "fieldtype": "Data",
            "width": 80
        },
        {
            "label": _("SINV Rate"),
            "fieldname": "sinv_rate",
            "fieldtype": "Currency",
            "width": 110
        },
        {
            "label": _("SINV Total"),
            "fieldname": "sinv_total",
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "label": _("SLE Rate"),
            "fieldname": "sle_rate",
            "fieldtype": "Currency",
            "width": 110
        },
        {
            "label": _("SLE Total"),
            "fieldname": "sle_total",
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "label": _("BIN Rate"),
            "fieldname": "bin_rate",
            "fieldtype": "Currency",
            "width": 110
        },
        {
            "label": _("BIN Total"),
            "fieldname": "bin_total",
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "label": _("Rate Diff"),
            "fieldname": "rate_diff",
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "label": _("Total Diff"),
            "fieldname": "total_diff",
            "fieldtype": "Currency",
            "width": 130
        }
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " and `tabSales Invoice`.posting_date>=%(from_date)s"
    if filters.get("to_date"):
        conditions += " and `tabSales Invoice`.posting_date<=%(to_date)s"

    result = []
    item_results = frappe.db.sql("""
            SELECT 
                `tabSales Invoice`.name as name,
                `tabSales Invoice`.posting_date as posting_date,
                `tabSales Invoice`.customer_name as customer_name,
                `tabSales Invoice Item`.item_code as item_code,
                `tabSales Invoice Item`.item_name as item_name,
                `tabSales Invoice Item`.qty as qty,
                `tabSales Invoice Item`.stock_uom as stock_uom,
                `tabSales Invoice Item`.rate as sinv_rate,
                `tabSales Invoice Item`.amount as sinv_total,
                
                ifnull((Select `tabStock Ledger Entry`.valuation_rate from `tabStock Ledger Entry`
                Where `tabStock Ledger Entry`.item_code = `tabSales Invoice Item`.item_code
                and `tabStock Ledger Entry`.voucher_detail_no = `tabSales Invoice Item`.name),0) as sle_rate,
                
                ifnull((Select `tabBin`.valuation_rate from `tabBin`
                Where `tabBin`.item_code = `tabSales Invoice Item`.item_code
                and `tabBin`.warehouse = `tabSales Invoice Item`.warehouse),0) as bin_rate
                


            FROM
                `tabSales Invoice` join `tabSales Invoice Item`
            ON `tabSales Invoice`.name = `tabSales Invoice Item`.parent
            WHERE
                `tabSales Invoice`.docstatus = 1
                and `tabSales Invoice`.is_return = 1
                {conditions}

            ORDER BY `tabSales Invoice`.posting_date desc
            """.format(conditions=conditions), filters, as_dict=1)

    if item_results:
        for item_dict in item_results:
            data = {
                'name': item_dict.name,
                'posting_date': item_dict.posting_date,
                'customer_name': item_dict.customer_name,
                'item_code': item_dict.item_code,
                'item_name': item_dict.item_name,
                'qty': -1 * item_dict.qty,
                'stock_uom': item_dict.stock_uom,
                'sinv_rate': item_dict.sinv_rate,
                'sinv_total': -1 * item_dict.sinv_total,
                'sle_rate': item_dict.sle_rate,
                'sle_total': -1 * item_dict.qty * item_dict.sle_rate,
                'bin_rate': item_dict.bin_rate,
                'bin_total': -1 * item_dict.qty * item_dict.bin_rate,
                'rate_diff': item_dict.bin_rate - item_dict.sle_rate,
                'total_diff': (-1 * item_dict.qty * item_dict.bin_rate) - (-1 * item_dict.qty * item_dict.sle_rate),
            }
            result.append(data)
    return result
