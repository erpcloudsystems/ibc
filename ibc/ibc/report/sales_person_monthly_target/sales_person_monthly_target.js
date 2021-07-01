// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */
var d = new Date();

frappe.query_reports["Sales Person Monthly Target"] = {
	"filters": [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: new Date(d.getFullYear(),d.getMonth(),1),
			reqd: 1
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: new Date(d.getFullYear(),d.getMonth(),30),
			reqd: 1
		},
	],
}


