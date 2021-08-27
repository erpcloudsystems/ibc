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
			"label": _("Brand"),
			"fieldname": "brand",
			"fieldtype": "Link",
			"options": "Brand",
			"width": 150
		},
		{
			"label": _("Opening"),
			"fieldname": "opening",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": _("Purchases"),
			"fieldname": "purchases",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": _("Total In"),
			"fieldname": "total_in",
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
			"label": _("COGS"),
			"fieldname": "cogs",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": _("Sales Value"),
			"fieldname": "sales_value",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": _("Added Value"),
			"fieldname": "added_value",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": _("COGS/Sales Value"),
			"fieldname": "cogs_sales_value",
			"fieldtype": "Percent",
			"width": 150
		},
		{
			"label": _("Added Value/Sales Value"),
			"fieldname": "added_sales_value",
			"fieldtype": "Percent",
			"width": 150
		},
		{
			"label": _("Added Value / COGS"),
			"fieldname": "added_cogs",
			"fieldtype": "Percent",
			"width": 150
		}
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
			name as name
			from
			`tabBrand`
		""", filters , as_dict=1)

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
			s = 0
			s1 = 0
			s2 = 0


			#///////////////////////////////////////////////////////////////////////////////////////////////////////////
			opening = frappe.db.sql("""select
									ifnull(sum(stock_value_difference),0) as res
									from `tabStock Ledger Entry` 
									where
									`tabStock Ledger Entry`.brand =%s
									and `tabStock Ledger Entry`.posting_date < %s
									and `tabStock Ledger Entry`.is_cancelled = 0
									""",
									(brands, from_date), as_dict=1)
			for tqty in opening:
				s += tqty.res
			data['opening'] = s

			# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
			purchase = frappe.db.sql("""select
									ifnull(sum(stock_value_difference),0) as res
									from `tabStock Ledger Entry` 
									where
									voucher_type = "Purchase Invoice"
									and `tabStock Ledger Entry`.brand =%s
									and `tabStock Ledger Entry`.posting_date between %s and %s
									and `tabStock Ledger Entry`.is_cancelled = 0
									""",
									(brands, from_date, to_date), as_dict=1)
			for tqty in purchase:
				s1 += tqty.res
			data['purchases'] = s1

			# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
			totalin = s + s1
			data['total_in'] = totalin

			# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
			cur_val = frappe.db.sql("""select
									ifnull(sum(stock_value_difference),0) as res
									from `tabStock Ledger Entry` 
									where
									`tabStock Ledger Entry`.brand =%s
									and `tabStock Ledger Entry`.posting_date <= %s
									and `tabStock Ledger Entry`.is_cancelled = 0
									""",
									 (brands, to_date), as_dict=1)
			for tqty in cur_val:
				s2 += tqty.res
			data['current_value'] = s2
			# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
			cogsdn=0
			cogsinv=0
			cogs_dn = frappe.db.sql("""select
									ifnull(sum(stock_value_difference),0) as res
									from `tabStock Ledger Entry` 
									where
									voucher_type = "Delivery Note"
									and `tabStock Ledger Entry`.brand =%s
									and `tabStock Ledger Entry`.posting_date between %s and %s
									and `tabStock Ledger Entry`.is_cancelled = 0
														""",
									(brands, from_date, to_date), as_dict=1)
			for tqty in cogs_dn:
				cogsdn += tqty.res

			cogs_inv = frappe.db.sql("""select
									ifnull(sum(stock_value_difference),0) as res
									from `tabStock Ledger Entry` 
									where
									voucher_type = "Sales Invoice"
									and actual_qty >0
									and `tabStock Ledger Entry`.brand =%s
									and `tabStock Ledger Entry`.posting_date between %s and %s
									and `tabStock Ledger Entry`.is_cancelled = 0
														""",
									(brands, from_date, to_date), as_dict=1)
			for tqty in cogs_inv:
				cogsinv += tqty.res

			cogsss = cogsdn + cogsinv

			data['cogs'] = cogsss

			# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
			sinv = 0
			ssinv = frappe.db.sql("""select
									ifnull(sum(net_amount),0) as res
									from `tabSales Invoice Item` join `tabSales Invoice` on  `tabSales Invoice Item`.parent = `tabSales Invoice`.name
									where
									`tabSales Invoice Item`.brand =%s
									and `tabSales Invoice`.posting_date between %s and %s
									and `tabSales Invoice`.docstatus = 1
															""",
									(brands, from_date, to_date), as_dict=1)
			for tqty in ssinv:
				sinv += tqty.res

			data['sales_value'] = sinv

			addedv = sinv + cogsss

			if cogsss != 0 and sinv !=0:
				cogs_sales_value = ((cogsss*(-1)) / sinv)*100
				data['cogs_sales_value'] = cogs_sales_value
			else:
				data['cogs_sales_value'] = 0

			if addedv != 0 and sinv !=0:
				added_sales_value = addedv / sinv * 100
				data['added_sales_value'] = added_sales_value
			else:
				data['added_sales_value'] = 0


			if cogsss != 0 and addedv !=0:
				added_cogs_value = addedv / cogsss * 100
				data['added_cogs'] = added_cogs_value
			else:
				data['added_cogs']  = 0

			#added_sales_value = addedv / sinv
			#added_cogs_value = addedv / cogsdn

			data['added_value'] = addedv

			#data['added_sales_value'] = added_sales_value
			#data['added_cogs'] = added_cogs_value






			result.append(data)

	return result



