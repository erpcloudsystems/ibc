# Copyright (c) 2013, erpcloud.systems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns=get_columns()
	data=get_data(filters,columns)
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
			"label": _("Customer"),
			"fieldname": "customer",
			"fieldtype": "Data",
			"width": 300
		},
		{
			"label": _("Total Sales Amount"),
			"fieldname": "total_sales_amount",
			"fieldtype": "Currency",
			"width": 160
		},
		{
			"label": _("Total Return Amount"),
			"fieldname": "total_return_amount",
			"fieldtype": "Currency",
			"width": 160
		},
		{
			"label": _("Total"),
			"fieldname": "total",
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
	if filters.get("brand"):
		conditions += " and brand=%(brand)s"
	if filters.get("from_date"):
		conditions += " and posting_date>=%(from_date)s"
	if filters.get("to_date"):
		conditions += " and posting_date<=%(to_date)s"

	from_dates = filters.get("from_date")
	to_dates = filters.get("to_date")
	item_results = frappe.db.sql("""
				select distinct
						`tabSales Invoice Item`.brand as brand,
						`tabSales Invoice`.customer_name as customer_name,						
						`tabSales Invoice`.customer as customer						
				from							
				`tabSales Invoice` JOIN `tabSales Invoice Item` ON `tabSales Invoice`.name = `tabSales Invoice Item`.parent
				where
					 `tabSales Invoice`.docstatus = 1
					 					 
					{conditions}
				
				""".format(conditions=conditions), filters, as_dict=1)


	#price_list_names = list(set([item.price_list_name for item in item_results]))

	#buying_price_map = get_price_map(price_list_names, buying=1)
	#selling_price_map = get_price_map(price_list_names, selling=1)

	result = []
	if item_results:
		for item_dict in item_results:

			data = {
				'brand': item_dict.brand,
				'customer': item_dict.customer_name,

			}
			result.append(data)

			brando = item_dict.brand
			customero = item_dict.customer
			to_dateo = filters.get("to_date")
			from_dateo = filters.get("from_date")

			sales = frappe.db.sql("""
							select 
								ifnull(sum(`tabSales Invoice Item`.net_amount),0) as total_sales_amount
								from 
								`tabSales Invoice Item` JOIN `tabSales Invoice` ON `tabSales Invoice`.name = `tabSales Invoice Item`.parent
								where
								`tabSales Invoice`.docstatus = 1
								and `tabSales Invoice`.customer='{customero}'
								and `tabSales Invoice Item`.net_amount>0 
								and `tabSales Invoice Item`.brand = '{brando}'
								and `tabSales Invoice`.posting_date between '{from_dateo}' and '{to_dateo}'
							""".format(conditions=conditions, customero=customero, brando=brando, from_dateo=from_dateo, to_dateo=to_dateo))

			data['total_sales_amount'] = sales[0][0]
			returns = frappe.db.sql("""
										select 
											ifnull(sum(`tabSales Invoice Item`.net_amount),0) as total_return_amount
											from 
											`tabSales Invoice Item` JOIN `tabSales Invoice` ON `tabSales Invoice`.name = `tabSales Invoice Item`.parent
											where
											`tabSales Invoice`.docstatus = 1
											and `tabSales Invoice`.customer='{customero}'
											and `tabSales Invoice Item`.net_amount<0 
											and `tabSales Invoice Item`.brand = '{brando}'
											and `tabSales Invoice`.posting_date between '{from_dateo}' and '{to_dateo}'
										""".format(conditions=conditions, customero=customero, brando=brando,
												   from_dateo=from_dateo, to_dateo=to_dateo))

			data['total_return_amount'] = returns[0][0]
			data['total'] = sales[0][0] + returns[0][0]



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
