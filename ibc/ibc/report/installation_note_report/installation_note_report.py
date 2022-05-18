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
			"label": _("Installation Note"),
			"fieldname": "name",
			"fieldtype": "Link",
            "options": "Installation Note",
            "width": 200
		},
		{
			"label": _("Customer"),
			"fieldname": "customer",
			"options": "Customer",
			"fieldtype": "Link",
			"width": 300
		},
        {
            "label": _("Customer Name"),
            "fieldname": "customer_name",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "label": _("Installation Date"),
            "fieldname": _("inst_date"),
            "fieldtype": "date",
            "width": 100
        },

        {
            "label": _("type"),
            "fieldname": _("type"),
            "fieldtype": "data",
            "width": 180
        },
		{
			"label": _("Responsible Engineer"),
			"fieldname": _("eng"),
			"options": "User",
			"fieldtype": "Link",
			"width": 180
		},
        {
            "label": _("Responsible Engineer Name"),
            "fieldname": _("eng_name"),
            "fieldtype": "Data",
            "width": 180
        },

        {
            "label": _("Sales Person"),
            "fieldname": _("sales_person"),
			"options": "Sales Person",
            "fieldtype": "Link",
            "width": 220
        }


    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " and `tabInstallation Note`.inst_date>=%(from_date)s"
    if filters.get("to_date"):
        conditions += " and `tabInstallation Note`.inst_date<=%(to_date)s"
    if filters.get("eng"):
        conditions += " and `tabInstallation Note`.eng =%(eng)s"
    item_results = frappe.db.sql("""
				select
                        `tabInstallation Note`.name as name,
                        `tabInstallation Note`.customer as customer,
                        `tabCustomer`.customer_name as customer_name,
                        `tabInstallation Note`.inst_date as inst_date,
                        `tabInstallation Note`.type as type,
                        `tabInstallation Note`.eng as eng,
                        `tabInstallation Note`.eng_name as eng_name,
                        `tabInstallation Note`.sales_person as sales_person
                                            				
				from
                        `tabInstallation Note` join `tabCustomer` on `tabInstallation Note`.customer = `tabCustomer`.name
				where
				        `tabInstallation Note`.docstatus != 2
				{conditions}

				ORDER BY `tabInstallation Note`.inst_date desc


				""".format(conditions=conditions), filters, as_dict=1)

    # price_list_names = list(set([item.price_list_name for item in item_results]))

    # buying_price_map = get_price_map(price_list_names, buying=1)
    # selling_price_map = get_price_map(price_list_names, selling=1)

    result = []
    if item_results:
        for item_dict in item_results:
            data = {
                'name': item_dict.name,
                'customer': item_dict.customer,
                'customer_name': item_dict.customer_name,
                'inst_date': item_dict.inst_date,
                'type': item_dict.type,
				'eng': item_dict.eng,
                'eng_name': item_dict.eng_name,
                'sales_person': _(item_dict.sales_person),
                'employee': _(item_dict.employee),
                'employee_name': _(item_dict.employee_name),

            }
            result.append(data)

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
                                     fields=["name", "price_list", "price_list_rate"], filters=filters)

    for d in pricing_details:
        name = d["name"]
        price_map[name] = {
            price_list_key: d["price_list"],
            rate_key: d["price_list_rate"]
        }

    return price_map
