# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
class ItemRequest(Document):
	@frappe.whitelist()
	def on_submit(self):
		new_doc = frappe.get_doc({
			"doctype": "Material Request",
			"material_request_type": self.material_request_type,
			"transaction_date": self.transaction_date,
			"schedule_date": self.schedule_date,
			"item_request": self.name,

		})
		is_items = frappe.db.sql(""" select  a.item, a.description, a.quantity, a.rate
							                                                           from `tabItem Request Table` a join `tabItem Request` b
							                                                           on a.parent = b.name
							                                                           where b.name = '{name}'
							                                                       """.format(name=self.name),
								 as_dict=1)

		for c in is_items:
			items = new_doc.append("items", {})
			items.item_code = c.item
			items.description = c.description
			items.qty = c.quantity
			items.rate = c.rate

		new_doc.insert(ignore_permissions=True)
		frappe.msgprint("  تم إنشاء طلب مواد بحالة مسودة رقم " + new_doc.name)
