from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def before_insert(doc, method=None):
    pass
@frappe.whitelist()
def after_insert(doc, method=None):
    pass
@frappe.whitelist()
def onload(doc, method=None):
    pass
@frappe.whitelist()
def before_validate(doc, method=None):
    pass
@frappe.whitelist()
def validate(doc, method=None):
    pass
@frappe.whitelist()
def on_submit(doc, method=None):
    new_doc = frappe.get_doc({
        "doctype": "Purchase Invoice",
        "posting_date": doc.posting_date,
        "supplier": doc.supplier,
        "purchase_receipt": doc.name,

    })
    is_items = frappe.db.sql(""" select a.item_code, a.item_name, a.item_group, a.qty, a.uom , a.qty, a.rate
        		                                                           from `tabPurchase Receipt Item` a join `tabPurchase Receipt` b
        		                                                           on a.parent = b.name
        		                                                           where b.name = '{name}'
        		                                                       """.format(name=doc.name), as_dict=1)

    for c in is_items:
        items = new_doc.append("items", {})
        items.item_code = c.item_code
        items.item_name = c.item_name
        items.qty = c.qty
        items.uom = c.uom
        items.rate = c.rate

    new_doc.insert(ignore_permissions=True)
    frappe.msgprint("  تم إنشاء فاتورة مشتريات بحالة مسودة رقم " + new_doc.name)

@frappe.whitelist()
def on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
