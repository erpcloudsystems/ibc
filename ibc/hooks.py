# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "ibc"
app_title = "Ibc"
app_publisher = "erpcloud.systems"
app_description = "ibc customization"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "mg@erpcloud.systems"
app_license = "MIT"

doc_events = {
	"Quotation": {
		"before_insert": "ibc.trigers.quot_before_insert",
		"after_insert": "ibc.trigers.quot_after_insert",
		"onload": "ibc.trigers.quot_onload",
		"before_validate": "ibc.trigers.quot_before_validate",
		"validate": "ibc.trigers.quot_validate",
		"on_submit": "ibc.trigers.quot_on_submit",
		"on_cancel": "ibc.trigers.quot_on_cancel",
		"on_update_after_submit": "ibc.trigers.quot_on_update_after_submit",
		"before_save": "ibc.trigers.quot_before_save",
		"before_cancel": "ibc.trigers.quot_before_cancel",
		"on_update": "ibc.trigers.quot_on_update",
	},
	"Sales Invoice": {
		"before_insert": "ibc.trigers.siv_before_insert",
		"after_insert": "ibc.trigers.siv_after_insert",
		"onload": "ibc.trigers.siv_onload",
		"before_validate": "ibc.trigers.siv_before_validate",
		"validate": "ibc.trigers.siv_validate",
		"on_submit": "ibc.trigers.siv_on_submit",
		"on_cancel": "ibc.trigers.siv_on_cancel",
		"on_update_after_submit": "ibc.trigers.siv_on_update_after_submit",
		"before_save": "ibc.trigers.siv_before_save",
		"before_cancel": "ibc.trigers.siv_before_cancel",
		"on_update": "ibc.trigers.siv_on_update",
	},
	"Sales Order": {
		"before_insert": "ibc.trigers.so_before_insert",
		"after_insert": "ibc.trigers.so_after_insert",
		"onload": "ibc.trigers.so_onload",
		"before_validate": "ibc.trigers.so_before_validate",
		"validate": "ibc.trigers.so_validate",
		"on_submit": "ibc.trigers.so_on_submit",
		"on_cancel": "ibc.trigers.so_on_cancel",
		"on_update_after_submit": "ibc.trigers.so_on_update_after_submit",
		"before_save": "ibc.trigers.so_before_save",
		"before_cancel": "ibc.trigers.so_before_cancel",
		"on_update": "ibc.trigers.so_on_update",
	},
	"Material Request": {
		"before_insert": "ibc.trigers.mr_before_insert",
		"after_insert": "ibc.trigers.mr_after_insert",
		"onload": "ibc.trigers.mr_onload",
		"before_validate": "ibc.trigers.mr_before_validate",
		"validate": "ibc.trigers.mr_validate",
		"on_submit": "ibc.trigers.mr_on_submit",
		"on_cancel": "ibc.trigers.mr_on_cancel",
		"on_update_after_submit": "ibc.trigers.mr_on_update_after_submit",
		"before_save": "ibc.trigers.mr_before_save",
		"before_cancel": "ibc.trigers.mr_before_cancel",
		"on_update": "ibc.trigers.mr_on_update",
	},
	"Stock Entry": {
		"before_insert": "ibc.trigers.ste_before_insert",
		"after_insert": "ibc.trigers.ste_after_insert",
		"onload": "ibc.trigers.ste_onload",
		"before_validate": "ibc.trigers.ste_before_validate",
		"validate": "ibc.trigers.ste_validate",
		"on_submit": "ibc.trigers.ste_on_submit",
		"on_cancel": "ibc.trigers.ste_on_cancel",
		"on_update_after_submit": "ibc.trigers.ste_on_update_after_submit",
		"before_save": "ibc.trigers.ste_before_save",
		"before_cancel": "ibc.trigers.ste_before_cancel",
		"on_update": "ibc.trigers.ste_on_update",
	},
	"Delivery Note": {
		"before_insert": "ibc.trigers.dn_before_insert",
		"after_insert": "ibc.trigers.dn_after_insert",
		"onload": "ibc.trigers.dn_onload",
		"before_validate": "ibc.trigers.dn_before_validate",
		"validate": "ibc.trigers.dn_validate",
		"on_submit": "ibc.trigers.dn_on_submit",
		"on_cancel": "ibc.trigers.dn_on_cancel",
		"on_update_after_submit": "ibc.trigers.dn_on_update_after_submit",
		"before_save": "ibc.trigers.dn_before_save",
		"before_cancel": "ibc.trigers.dn_before_cancel",
		"on_update": "ibc.trigers.dn_on_update",
	},
	"Purchase Order": {
		"before_insert": "ibc.trigers.po_before_insert",
		"after_insert": "ibc.trigers.po_after_insert",
		"onload": "ibc.trigers.po_onload",
		"before_validate": "ibc.trigers.po_before_validate",
		"validate": "ibc.trigers.po_validate",
		"on_submit": "ibc.trigers.po_on_submit",
		"on_cancel": "ibc.trigers.po_on_cancel",
		"on_update_after_submit": "ibc.trigers.po_on_update_after_submit",
		"before_save": "ibc.trigers.po_before_save",
		"before_cancel": "ibc.trigers.po_before_cancel",
		"on_update": "ibc.trigers.po_on_update",
	},
	"Purchase Receipt": {
		"before_insert": "ibc.trigers.pr_before_insert",
		"after_insert": "ibc.trigers.pr_after_insert",
		"onload": "ibc.trigers.pr_onload",
		"before_validate": "ibc.trigers.pr_before_validate",
		"validate": "ibc.trigers.pr_validate",
		"on_submit": "ibc.trigers.pr_on_submit",
		"on_cancel": "ibc.trigers.pr_on_cancel",
		"on_update_after_submit": "ibc.trigers.pr_on_update_after_submit",
		"before_save": "ibc.trigers.pr_before_save",
		"before_cancel": "ibc.trigers.pr_before_cancel",
		"on_update": "ibc.trigers.pr_on_update",
	},
	"Purchase Invoice": {
		"before_insert": "ibc.trigers.piv_before_insert",
		"after_insert": "ibc.trigers.piv_after_insert",
		"onload": "ibc.trigers.piv_onload",
		"before_validate": "ibc.trigers.piv_before_validate",
		"validate": "ibc.trigers.piv_validate",
		"on_submit": "ibc.trigers.piv_on_submit",
		"on_cancel": "ibc.trigers.piv_on_cancel",
		"on_update_after_submit": "ibc.trigers.piv_on_update_after_submit",
		"before_save": "ibc.trigers.piv_before_save",
		"before_cancel": "ibc.trigers.piv_before_cancel",
		"on_update": "ibc.trigers.piv_on_update",
	},
	"Payment Entry": {
		"before_insert": "ibc.trigers.pe_before_insert",
		"after_insert": "ibc.trigers.pe_after_insert",
		"onload": "ibc.trigers.pe_onload",
		"before_validate": "ibc.trigers.pe_before_validate",
		"validate": "ibc.trigers.pe_validate",
		"on_submit": "ibc.trigers.pe_on_submit",
		"on_cancel": "ibc.trigers.pe_on_cancel",
		"on_update_after_submit": "ibc.trigers.pe_on_update_after_submit",
		"before_save": "ibc.trigers.pe_before_save",
		"before_cancel": "ibc.trigers.pe_before_cancel",
		"on_update": "ibc.trigers.pe_on_update",
	},
	"Journal Entry": {
		"before_insert": "ibc.trigers.je_before_insert",
		"after_insert": "ibc.trigers.je_after_insert",
		"onload": "ibc.trigers.je_onload",
		"before_validate": "ibc.trigers.je_before_validate",
		"validate": "ibc.trigers.je_validate",
		"on_submit": "ibc.trigers.je_on_submit",
		"on_cancel": "ibc.trigers.je_on_cancel",
		"on_update_after_submit": "ibc.trigers.je_on_update_after_submit",
		"before_save": "ibc.trigers.je_before_save",
		"before_cancel": "ibc.trigers.je_before_cancel",
		"on_update": "ibc.trigers.je_on_update",
	},
	"Blanket Order": {
		"before_insert": "ibc.trigers.blank_before_insert",
		"after_insert": "ibc.trigers.blank_after_insert",
		"onload": "ibc.trigers.blank_onload",
		"before_validate": "ibc.trigers.blank_before_validate",
		"validate": "ibc.trigers.blank_validate",
		"on_submit": "ibc.trigers.blank_on_submit",
		"on_cancel": "ibc.trigers.blank_on_cancel",
		"on_update_after_submit": "ibc.trigers.blank_on_update_after_submit",
		"before_save": "ibc.trigers.blank_before_save",
		"before_cancel": "ibc.trigers.blank_before_cancel",
		"on_update": "ibc.trigers.blank_on_update",
	},
	"Expense Claim": {
		"before_insert": "ibc.trigers.excl_before_insert",
		"after_insert": "ibc.trigers.excl_after_insert",
		"onload": "ibc.trigers.excl_onload",
		"before_validate": "ibc.trigers.excl_before_validate",
		"validate": "ibc.trigers.excl_validate",
		"on_submit": "ibc.trigers.excl_on_submit",
		"on_cancel": "ibc.trigers.excl_on_cancel",
		"on_update_after_submit": "ibc.trigers.excl_on_update_after_submit",
		"before_save": "ibc.trigers.excl_before_save",
		"before_cancel": "ibc.trigers.excl_before_cancel",
		"on_update": "ibc.trigers.excl_on_update",
	},
	"Employee Advance": {
		"before_insert": "ibc.trigers.emad_before_insert",
		"after_insert": "ibc.trigers.emad_after_insert",
		"onload": "ibc.trigers.emad_onload",
		"before_validate": "ibc.trigers.emad_before_validate",
		"validate": "ibc.trigers.emad_validate",
		"on_submit": "ibc.trigers.emad_on_submit",
		"on_cancel": "ibc.trigers.emad_on_cancel",
		"on_update_after_submit": "ibc.trigers.emad_on_update_after_submit",
		"before_save": "ibc.trigers.emad_before_save",
		"before_cancel": "ibc.trigers.emad_before_cancel",
		"on_update": "ibc.trigers.emad_on_update",
	},
}

scheduler_events = {
 	"hourly": [
 		"ibc.trigers.hourly"
	 ],
	 "daily": [
 		"ibc.trigers.daily"
	 ]
}


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ibc/css/ibc.css"
# app_include_js = "/assets/ibc/js/ibc.js"

# include js, css files in header of web template
# web_include_css = "/assets/ibc/css/ibc.css"
# web_include_js = "/assets/ibc/js/ibc.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ibc/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "ibc.install.before_install"
# after_install = "ibc.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ibc.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ibc.tasks.all"
# 	],
# 	"daily": [
# 		"ibc.tasks.daily"
# 	],
# 	"hourly": [
# 		"ibc.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ibc.tasks.weekly"
# 	]
# 	"monthly": [
# 		"ibc.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "ibc.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ibc.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ibc.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"ibc.auth.validate"
# ]

