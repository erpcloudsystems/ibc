

# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
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
			"label": _("Sales Invoice"),
			"fieldname": "sales_invoice",
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 180
		},
		{
			"label": _("Customer"),
			"fieldname": "customer",
			"fieldtype": "Data",
			"width": 195
		},
		{
			"label": _("Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 95
		},
		{
			"label": _("Territory"),
			"fieldname": "territory",
			"fieldtype": "Link",
			"options": "Territory",
			"width": 145
		},
		{
			"label": _("Sales Person"),
			"fieldname": "sales_person",
			"fieldtype": "Link",
			"options": "Sales Person",
			"width": 145
		},
		{
			"label": _("Brand"),
			"fieldname": "brand",
			"fieldtype": "data",
			"width": 145
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
			"width": 155
		},
		{
			"label": _("Qty"),
			"fieldname": "qty",
			"fieldtype": "Float",
			"width": 60
		},
		{
			"label": _("Disc (%)"),
			"fieldname": "discount_percentage",
			"fieldtype": "Percent",
			"width": 80
		},
		{
			"label": _("Amount"),
			"fieldname": "amount",
			"fieldtype": "Currency",
			"width": 100
		}
	]

def get_data(filters, columns):
	item_price_qty_data = []
	item_price_qty_data = get_item_price_qty_data(filters)
	return item_price_qty_data

def get_item_price_qty_data(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += " and a.posting_date>=%(from_date)s"
	if filters.get("to_date"):
		conditions += " and a.posting_date<=%(to_date)s"
	if filters.get("customer"):
		conditions += " and a.customer=%(customer)s"
	if filters.get("territory"):
		conditions += " and a.territory=%(territory)s"
	if filters.get("sales_person"):
		conditions += " and a.sales_person=%(sales_person)s"
	if filters.get("without_service_items"):
		conditions += " and b.item_group not in  ('2-Service','ID Printed','Maintenance contracts','Services1') "
	item_results = frappe.db.sql("""
									select
										a.name as sales_invoice,
										a.customer_name as customer,
										a.posting_date as posting_date,
										a.territory as territory,
										a.sales_person as sales_person,
										b.item_code as item_code,
										b.item_name as item_name,
										b.brand as brand,
										b.qty as qty,
										b.discount_percentage as discount_percentage,
										b.amount as amount
									from
									`tabSales Invoice` a JOIN `tabSales Invoice Item` b ON a.name = b.parent JOIN `tabSales Person` ON a.sales_person = `tabSales Person`.name
									where
									 a.docstatus =1
									 and `tabSales Person`.parent != "Projects Sales"
										{conditions}
								"""
		.format(conditions=conditions), filters, as_dict=1)



	#price_list_names = list(set([item.price_list_name for item in item_results]))

	#buying_price_map = get_price_map(price_list_names, buying=1)
	#selling_price_map = get_price_map(price_list_names, selling=1)

	result = []
	if item_results:
		for item_dict in item_results:
			data = {
				'sales_invoice': item_dict.sales_invoice,
				'customer': item_dict.customer,
				'posting_date': item_dict.posting_date,
				'territory': item_dict.territory,
				'sales_person': item_dict.sales_person,
				'item_code': item_dict.item_code,
				'item_name': item_dict.item_name,
				'brand': item_dict.brand,
				'qty': item_dict.qty,
				'discount_percentage': item_dict.discount_percentage,
				'amount': item_dict.amount
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
		fields = ["name", "price_list", "price_list_rate"], filters=filters)

	for d in pricing_details:
		name = d["name"]
		price_map[name] = {
			price_list_key :d["price_list"],
			rate_key :d["price_list_rate"]
		}

	return price_map


