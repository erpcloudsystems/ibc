# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    item_results = frappe.db.sql("""
        SELECT distinct
                name as name
                from
                `tabBrand`
            """, filters, as_dict=1)

    result = []
    if item_results:
        for item_dict in item_results:

            data = {
                'brand': (item_dict.name),
            }
            to_date = filters.get("to_date")
            from_date = filters.get("from_date")
            brands = item_dict.name

            # Start getting all qty
            s1 = 0
            s2 = 0
            s3 = 0
            s4 = 0
            s5 = 0
            s6 = 0
            s7 = 0
            s8 = 0
            s9 = 0
            s10 = 0
            s11 = 0
            s12 = 0

            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
            jan = frappe.db.sql("""select
                                            ifnull(sum(stock_value_difference),0) as res
                                            from `tabStock Ledger Entry` 
                                            where
                                            `tabStock Ledger Entry`.brand =%s
                                            and `tabStock Ledger Entry`.posting_date <= "2021-01-31"
                                            and `tabStock Ledger Entry`.is_cancelled = 0
                                            """, brands, as_dict=1)
            for tqty in jan:
                s1 += tqty.res
            data['jan'] = s1

            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
            feb = frappe.db.sql("""select
                                            ifnull(sum(stock_value_difference),0) as res
                                            from `tabStock Ledger Entry` 
                                            where
                                            `tabStock Ledger Entry`.brand =%s
                                            and `tabStock Ledger Entry`.posting_date <= "2021-02-28"
                                            and `tabStock Ledger Entry`.is_cancelled = 0
                                            """, brands, as_dict=1)
            for tqty in feb:
                s2 += tqty.res
            data['feb'] = s2

            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
            mar = frappe.db.sql("""select
                                            ifnull(sum(stock_value_difference),0) as res
                                            from `tabStock Ledger Entry` 
                                            where
                                            `tabStock Ledger Entry`.brand =%s
                                            and `tabStock Ledger Entry`.posting_date <= "2021-03-31"
                                            and `tabStock Ledger Entry`.is_cancelled = 0
                                            """, brands, as_dict=1)
            for tqty in mar:
                s3 += tqty.res
            data['mar'] = s3

            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
            apr = frappe.db.sql("""select
                                            ifnull(sum(stock_value_difference),0) as res
                                            from `tabStock Ledger Entry` 
                                            where
                                            `tabStock Ledger Entry`.brand =%s
                                            and `tabStock Ledger Entry`.posting_date <= "2021-04-30"
                                            and `tabStock Ledger Entry`.is_cancelled = 0
                                            """, brands, as_dict=1)
            for tqty in apr:
                s4 += tqty.res
            data['apr'] = s4

            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
            may = frappe.db.sql("""select
                                            ifnull(sum(stock_value_difference),0) as res
                                            from `tabStock Ledger Entry` 
                                            where
                                            `tabStock Ledger Entry`.brand =%s
                                            and `tabStock Ledger Entry`.posting_date <= "2021-05-31"
                                            and `tabStock Ledger Entry`.is_cancelled = 0
                                            """, brands, as_dict=1)
            for tqty in may:
                s5 += tqty.res
            data['may'] = s5

            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
            jun = frappe.db.sql("""select
                                            ifnull(sum(stock_value_difference),0) as res
                                            from `tabStock Ledger Entry` 
                                            where
                                            `tabStock Ledger Entry`.brand =%s
                                            and `tabStock Ledger Entry`.posting_date <= "2021-06-30"
                                            and `tabStock Ledger Entry`.is_cancelled = 0
                                            """, brands, as_dict=1)
            for tqty in jun:
                s6 += tqty.res
            data['jun'] = s6

            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
            jul = frappe.db.sql("""select
                                            ifnull(sum(stock_value_difference),0) as res
                                            from `tabStock Ledger Entry` 
                                            where
                                            `tabStock Ledger Entry`.brand =%s
                                            and `tabStock Ledger Entry`.posting_date <= "2021-07-31"
                                            and `tabStock Ledger Entry`.is_cancelled = 0
                                            """, brands, as_dict=1)
            for tqty in jul:
                s7 += tqty.res
            data['jul'] = s7

            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
            aug = frappe.db.sql("""select
                                            ifnull(sum(stock_value_difference),0) as res
                                            from `tabStock Ledger Entry` 
                                            where
                                            `tabStock Ledger Entry`.brand =%s
                                            and `tabStock Ledger Entry`.posting_date <= "2021-08-31"
                                            and `tabStock Ledger Entry`.is_cancelled = 0
                                            """, brands, as_dict=1)
            for tqty in aug:
                s8 += tqty.res
            data['aug'] = s8

            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
            sep = frappe.db.sql("""select
                                            ifnull(sum(stock_value_difference),0) as res
                                            from `tabStock Ledger Entry` 
                                            where
                                            `tabStock Ledger Entry`.brand =%s
                                            and `tabStock Ledger Entry`.posting_date <= "2021-09-30"
                                            and `tabStock Ledger Entry`.is_cancelled = 0
                                            """, brands, as_dict=1)
            for tqty in sep:
                s9 += tqty.res
            data['sep'] = s9

            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
            oct = frappe.db.sql("""select
                                            ifnull(sum(stock_value_difference),0) as res
                                            from `tabStock Ledger Entry` 
                                            where
                                            `tabStock Ledger Entry`.brand =%s
                                            and `tabStock Ledger Entry`.posting_date <= "2021-10-31"
                                            and `tabStock Ledger Entry`.is_cancelled = 0
                                            """, brands, as_dict=1)
            for tqty in oct:
                s10 += tqty.res
            data['oct'] = s10

            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
            nov = frappe.db.sql("""select
                                            ifnull(sum(stock_value_difference),0) as res
                                            from `tabStock Ledger Entry` 
                                            where
                                            `tabStock Ledger Entry`.brand =%s
                                            and `tabStock Ledger Entry`.posting_date <= "2021-11-30"
                                            and `tabStock Ledger Entry`.is_cancelled = 0
                                            """, brands, as_dict=1)
            for tqty in nov:
                s11 += tqty.res
            data['nov'] = s11

            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
            dec = frappe.db.sql("""select
                                            ifnull(sum(stock_value_difference),0) as res
                                            from `tabStock Ledger Entry` 
                                            where
                                            `tabStock Ledger Entry`.brand =%s
                                            and `tabStock Ledger Entry`.posting_date <= "2021-12-31"
                                            and `tabStock Ledger Entry`.is_cancelled = 0
                                            """, brands, as_dict=1)
            for tqty in dec:
                s12 += tqty.res
            data['dec'] = s12

            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////

            result.append(data)

            chart = get_chart_data(data)

        return columns, result, chart

def get_columns():
    return [
        {
            "label": _("Brand"),
            "fieldname": "brand",
            "fieldtype": "Link",
            "options": "Brand",
            "width": 150
        },
        {
            "label": _("Jan 2021"),
            "fieldname": "jan",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Feb 2021"),
            "fieldname": "feb",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Mar 2021"),
            "fieldname": "mar",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Apr 2021"),
            "fieldname": "apr",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("May 2021"),
            "fieldname": "may",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Jun 2021"),
            "fieldname": "jun",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Jul 2021"),
            "fieldname": "jul",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Aug 2021"),
            "fieldname": "aug",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Sep 2021"),
            "fieldname": "sep",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Oct 2021"),
            "fieldname": "oct",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Nov 2021"),
            "fieldname": "nov",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Dec 2021"),
            "fieldname": "dec",
            "fieldtype": "Currency",
            "width": 150
        }
    ]

def get_chart_data(item_results):
    labels = []
    january = []
    february = []
    march = []
    #for y in item_results:
    #    labels.append(y.name)
    #for x in result:
    #    january.append(x.data['jan'])
    #    february.append(x.data['feb'])
    #    march.append(x.data['mar'])

    return {
        "data": {
            'labels': ["A","B","C"],
            'datasets': [
                {
                    "name": "JAN21",
                    "values": "12"
                },
                {
                    "name": "FEB21",
                    "values": "15"
                },
                {
                    "name": "MAR21",
                    "values": "50"
                },
            ]
        },
        "type": "bar",
        "colors": ["green", "blue", "red"],
        "barOptions": {
            "stacked": False
        }
    }
