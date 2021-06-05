// Copyright (c) 2016, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["New Stocks Brand"] = {
	"filters": [
		{
			"fieldname":"brand",
			"label": __("Brand"),
			"fieldtype": "Link",
			"reqd": 1,
			"options": "Brand",
			"default": "Unknown"
		},
				{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.get_today()
		},

	]
};
