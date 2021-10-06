# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
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
			"label": _("Item"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150
		},
		{
			"label": _("Item Name"),
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Brand"),
			"fieldname": "brand",
			"fieldtype": "Link",
			"options": "Brand",
			"width": 150
		},
		{
			"label": _("Opening Value"),
			"fieldname": "opening_value",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": _("Current Value"),
			"fieldname": "current_value",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": _("Percent"),
			"fieldname": "percent",
			"fieldtype": "Float",
			"width": 150
		},

	]


def get_data(filters, columns):
	item_price_qty_data = []
	item_price_qty_data = get_item_price_qty_data(filters)
	return item_price_qty_data



def get_item_price_qty_data(filters):
	conditions = ""
	conditions1 = ""
#vals = [filters.get("metal_ws") , filters.get("leather_ws") , filters.get("natural_ws") , filters.get("artificial_ws") , filters.get("metal_ws") , filters.get("supplier_ws") , filters.get("imported_ws")]


	item_results = frappe.db.sql("""
    SELECT distinct
			ifnull(`tabItem`.name,0) as item_code,
			ifnull(`tabItem`.item_name,0) as item_name,
			ifnull(`tabItem`.brand,0) as brand,
			(select valuation_rate from `tabStock Ledger Entry` where item_code =`tabItem`.name and is_cancelled = 0 ORDER BY `tabStock Ledger Entry`.posting_date ASC, `tabStock Ledger Entry`.posting_time ASC , `tabStock Ledger Entry`.creation ASC LIMIT 1 ) as opening_value,
			(select valuation_rate from tabBin where item_code =`tabItem`.name and warehouse = 'المخزن الرئيسي - IBC') as current_value
			from
			`tabItem`
		""", filters , as_dict=1)

	result = []
	if item_results:

		for item_dict in item_results:
			data = {}
			if item_dict.current_value and item_dict.opening_value:
				if item_dict.current_value > item_dict.opening_value:
					data = {
						'item_code': item_dict.item_code,
						'brand': (item_dict.brand),
						'item_name': (item_dict.item_name),
						'opening_value': (item_dict.opening_value),
						'current_value': (item_dict.current_value),
						'percent': (((item_dict.current_value/item_dict.opening_value)-1)*100)
					}
			result.append(data)

	return result



