# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _
# import frappe
from frappe.model.document import Document

class Ticket(Document):
    @frappe.whitelist()
    def validate(self):
        self.calculate_total()

    @frappe.whitelist()
    def on_submit(self):
        self.check_mandatory_fields()

    @frappe.whitelist()
    def calculate_total(self):
        totals = 0
        for x in self.items:
            totals += x.cost
        self.total_cost = totals

    @frappe.whitelist()
    def check_mandatory_fields(self):
        for x in self.items:
            if not x.warranty:
                frappe.throw("Row #" + str(x.idx) + ": Please Select The Warranty Status")
            if not x.issue_description:
                frappe.throw("Row #" + str(x.idx) + ": Please Mention The Issue Description")

    @frappe.whitelist()
    def get_serial_details(self):
        if not self.serial_no:
            frappe.throw(" Please Enter A Serial Number")

        check = frappe.db.sql(""" select serial, idx
                                  from `tabTicket Items` 
                                  where parent = '{parent}' and serial = '{serial}' 
                              """.format(parent=self.name, serial=self.serial_no), as_dict=1)
        for z in check:
            if z.serial:
                frappe.throw("Duplicated Entry: Serial " + z.serial + " Has Been Added In Row #" + str(z.idx))
        else:
            details = frappe.db.sql(""" select `tabDelivery Note`.name as delivery_note, 
                                                `tabDelivery Note`.posting_date as dn_date,
                                                `tabDelivery Note`.customer as customer,
                                                `tabDelivery Note`.sales_person as sales_person,
                                                `tabDelivery Note Item`.item_code as item_code, 
                                                `tabDelivery Note Item`.name as dn_item_name, 
                                                `tabDelivery Note Item`.item_name as item_name,
                                                `tabDelivery Note Item`.brand as brand
                                                
                                        from `tabDelivery Note Item` join `tabDelivery Note` 
                                        on `tabDelivery Note Item`.parent = `tabDelivery Note`.name
                                        where `tabDelivery Note`.docstatus = 1 
                                        and `tabDelivery Note Item`.serials like '%{serial}%'
                                        """.format(serial=self.serial_no, parent=self.name), as_dict=1)

            for x in details:
                y = self.append("items", {})
                y.customer = x.customer
                y.delivery_note = x.delivery_note
                y.dn_item_name = x.dn_item_name
                y.dn_date = x.dn_date
                y.sales_person = x.sales_person
                y.item_code = x.item_code
                y.item_name = x.item_name
                y.brand = x.brand
                y.serial = self.serial_no
                y.cost = 0

            #self.save()

    @frappe.whitelist()
    def create_invoice(self):
        items = [
            {
                "doctype": "Sales Invoice Item",
                "item_code": "9053",
                "qty": 1,
                "rate": self.total_cost,
                "uom": "Unit",
                "description": self.general_notes,
                "conversion_factor": 1,
                "income_account": "ايرادات الصيانه - IBC",
                "cost_center": "فرع الصيانه -Maintenance - IBC",
            }
        ]

        new_doc = frappe.get_doc({
            "doctype": "Sales Invoice",
            "ticket": self.name,
            "sales_person": "Maintenance",
            "sales_person_1": "Maintenance",
            "c_sales_person_1": "Maintenance",
            "customer": self.customer,
            "due_date": self.posting_date,
            "posting_date": self.posting_date,
            "currency": "EGP",
            "items": items,
        })
        new_doc.insert(ignore_permissions=True)
        self.sales_invoice = new_doc.name
        self.save()
        self.reload()
        frappe.msgprint(" Sales Invoice " + "<a href=/app/sales-invoice/" + new_doc.name + ">" + new_doc.name + "</a>" + " Created Successfully ")
