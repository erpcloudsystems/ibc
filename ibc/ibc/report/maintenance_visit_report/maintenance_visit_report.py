# Copyright (c) 2013, erpcloud.systems and contributors
# For license information, please see license.txt

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
			"label": "Maintenance Visit",
			"fieldname": "name",
			"fieldtype": "Link",
            "options": "Maintenance Visit",
			"width": 180
		},
        {
            "label": "Request Type",
            "fieldname": "request_type",
            "fieldtype": "Select",
            "width": 110
        },
        {
            "label": "Customer",
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 250
        },
        {
            "label": "Customer Name",
            "fieldname": "customer_name1",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": "Maintenance Date",
            "fieldname": "mntc_date",
            "fieldtype": "Date",
            "width": 150
        },
        {
            "label": "Sales Person",
            "fieldname": "sales_Person",
            "fieldtype": "Link",
            "options": "Sales Person",
            "width": 150
        },
        {
            "label": "Responsible Engineer",
            "fieldname": "eng",
            "fieldtype": "Link",
            "options": "User",
            "width": 300
        },
        {
            "label": "Responsible Engineer Name",
            "fieldname": "eng_name",
            "fieldtype": "Data",
            "width": 300
        }

    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " and `tabMaintenance Visit`.mntc_date>=%(from_date)s"
    if filters.get("to_date"):
        conditions += " and `tabMaintenance Visit`.mntc_date<=%(to_date)s"
    if filters.get("eng"):
        conditions += " and `tabMaintenance Visit`.eng =%(eng)s"
    result = []
    item_results = frappe.db.sql("""
            SELECT
                `tabMaintenance Visit`.name as name,
                `tabMaintenance Visit`.request_type as request_type,
                `tabMaintenance Visit`.customer as customer,
                `tabMaintenance Visit`.customer_name1 as customer_name1,
                `tabMaintenance Visit`.mntc_date as mntc_date,
                `tabMaintenance Visit`.sales_Person as sales_Person,
                `tabMaintenance Visit`.eng as eng,
                `tabMaintenance Visit`.eng_name as eng_name

                
            FROM
                `tabMaintenance Visit`
            WHERE
                `tabMaintenance Visit`.docstatus != 2
            {conditions}
                
            """.format(conditions=conditions), filters, as_dict=1)
    if item_results:
        for item_dict in item_results:
            data = {
                'request_type': item_dict.request_type,
                'name': item_dict.name,
                'customer': item_dict.customer,
                'customer_name1': item_dict.customer_name1,
                'mntc_date': item_dict.mntc_date,
                'sales_Person': item_dict.sales_Person,
                'eng': item_dict.eng,
                'eng_name': item_dict.eng_name,
                'employee': item_dict.employee,
                'employee_name': item_dict.employee_name,
                'department': item_dict.department,
                'designation': item_dict.designation
            }
            result.append(data)
    return result