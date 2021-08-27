// Copyright (c) 2016, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Stock Items Report"] = {
		"filters": [
		{
			"fieldname": "date",
			"label": __("Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
	]
}