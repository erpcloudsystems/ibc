from __future__ import unicode_literals
import frappe
from frappe import _

frappe.whitelist()
def hourly():
    frappe.db.sql(
        """update tabItem set tabItem.summary_stock = (select sum(tabBin.actual_qty) from tabBin join tabWarehouse on tabBin.warehouse = tabWarehouse.name where tabWarehouse.summery_stock = 1 and tabBin.item_code = tabItem.name)""")
    frappe.db.sql(
        """update tabItem inner join tabBin on tabItem.item_code = tabBin.item_code set tabItem.valuation_rate = tabBin.valuation_rate where tabBin.warehouse = "المخزن الرئيسي - IBC" and tabItem.valuation_rate != tabBin.valuation_rate""")
    frappe.db.sql(
        """ update tabItem join `tabWebsite Item` on tabItem.name = `tabWebsite Item`.item_code set `tabWebsite Item`.web_long_description = `tabItem`.discription_ar where tabItem.website_ar =1""")

    update_woocommerce()

frappe.whitelist()
def update_woocommerce():
        ## Get Single Values from Ecs Woocommerce seetings page
        price_list = frappe.db.get_single_value('Ecs Woocommerce', 'price_list')
        woocommerce_user_key = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_user_key')
        erpnext_user_key = frappe.db.get_single_value('Ecs Woocommerce', 'erpnext_user_key')
        woocommerce_link = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_link')
        woocommerce_user_secret = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_user_secret')
        erpnext_user_secret = frappe.db.get_single_value('Ecs Woocommerce', 'erpnext_user_secret')
        woocommerce_create = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_create')

        ## Get Values From Website Item and Item
        website_item_list = frappe.db.get_list('Website Item', filters={'published': 1},
                                               fields=['name',
                                                       'item_code',
                                                       'web_item_name',
                                                       'woocommerce_id',
                                                       'brand',
                                                       'item_group',
                                                       'website_image',
                                                       'creation',
                                                       'published',
                                                       'web_long_description',
                                                       'description'
                                                       ])
        for x in website_item_list:
            sku = x.item_code
            item_name = x.web_item_name
            permalink = "https://example.com/product" + x.web_item_name
            brand = x.brand
            item_group = x.item_group
            image = "https://ibc.erpcloud.systems" + x.website_image
            date_created = x.creation
            description = x.web_long_description
            short_description = x.description
            price = frappe.db.get_value('Item Price', {'item_code': sku, 'price_list': price_list}, ['price_list_rate'])
            category_id = frappe.db.get_value('Item Group', x.item_group, 'category_id')
            if x.published == 1:
                status = "publish"
            else:
                status = "draft"

            ## Create Data Structure
            data = {}
            data["name"] = item_name
            data["sku"] = sku
            data["type"] = "simple"
            data["status"] = status
            data["regular_price"] = str(price)
            data["description"] = x.web_long_description
            data["short_description"] = x.web_long_description
            images = []
            images.append({"src": image})
            data["images"] = images
            categories = []
            categories.append({"id": category_id})
            data["categories"] = categories
            woocommerce_id = x.woocommerce_id
            # frappe.msgprint(json.dumps(data))

            headeroauth = OAuth1(woocommerce_user_key, woocommerce_user_secret, None, None,
                                 signature_method='HMAC-SHA1')
            headers = {'content-type': 'application/json;charset=utf-8',
                       "Content-Length": "376"
                       }
            response = requests.post(
                url="https://demo.nv-host.com/ibcegypt/wp-json/wc/v3/products/" + str(woocommerce_id),
                data=json.dumps(data), auth=headeroauth, headers=headers)
