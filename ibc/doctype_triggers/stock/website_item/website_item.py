from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def before_insert(doc, method=None):
    pass
@frappe.whitelist()
def after_insert(doc, method=None):
    if not doc.website_image:
        frappe.throw(" Please Insert An Image For The Item ")

    ## Get Single Values from Ecs Woocommerce seetings page
    price_list = frappe.db.get_single_value('Ecs Woocommerce', 'price_list')
    woocommerce_user_key = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_user_key')
    erpnext_user_key = frappe.db.get_single_value('Ecs Woocommerce', 'erpnext_user_key')
    woocommerce_link = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_link')
    woocommerce_user_secret = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_user_secret')
    erpnext_user_secret = frappe.db.get_single_value('Ecs Woocommerce', 'erpnext_user_secret')
    woocommerce_create = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_create')

    ## Get Values From Website Item and Item
    sku = doc.item_code
    item1 = frappe.get_doc("Item", doc.item_code)
    doc.web_long_description = item1.woocommerce_description
    doc.short_description = item1.woocommerce_description
    doc.save()
    item_name = doc.web_item_name
    permalink = "https://example.com/product" + doc.web_item_name
    brand = doc.brand
    item_group = doc.item_group
    image = "https://ibc.erpcloud.systems" + doc.website_image
    date_created = doc.creation
    # status = doc.status
    description = doc.web_long_description
    short_description = doc.description
    price = frappe.db.get_value('Item Price', {'item_code': sku, 'price_list': price_list}, ['price_list_rate'])
    category_id = frappe.db.get_value('Item Group', doc.item_group, 'category_id')

    ## Create Data Structure
    data = {}
    data["name"] = item_name
    data["sku"] = sku
    data["type"] = "simple"
    data["regular_price"] = str(price)
    data["description"] = doc.web_long_description
    data["short_description"] = doc.web_long_description
    images = []
    images.append({"src": image})
    data["images"] = images
    categories = []
    categories.append({"id": category_id})
    data["categories"] = categories
    # frappe.msgprint(json.dumps(data))

    headeroauth = OAuth1(woocommerce_user_key, woocommerce_user_secret, None, None, signature_method='HMAC-SHA1')
    headers = {'content-type': 'application/json;charset=utf-8',
               "Content-Length": "376"
               }
    response = requests.post(url=woocommerce_create, data=json.dumps(data), auth=headeroauth, headers=headers)
    # frappe.msgprint(response.content)

    returned_data = json.loads(response.content)

    # item = frappe.get_doc("Item", sku)
    # item.woocommerce_id = returned_data["id"]
    doc.woocommerce_id = returned_data["id"]
    # item.save()
    doc.save()

@frappe.whitelist()
def onload(doc, method=None):
    pass
@frappe.whitelist()
def before_validate(doc, method=None):
    pass
@frappe.whitelist()
def validate(doc, method=None):
    if doc.woocommerce_id:
        if not doc.website_image:
            frappe.throw(" Please Insert An Image For The Item ")

        ## Get Single Values from Ecs Woocommerce seetings page
        price_list = frappe.db.get_single_value('Ecs Woocommerce', 'price_list')
        woocommerce_user_key = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_user_key')
        erpnext_user_key = frappe.db.get_single_value('Ecs Woocommerce', 'erpnext_user_key')
        woocommerce_link = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_link')
        woocommerce_user_secret = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_user_secret')
        erpnext_user_secret = frappe.db.get_single_value('Ecs Woocommerce', 'erpnext_user_secret')
        woocommerce_create = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_create')

        ## Get Values From Website Item and Item
        sku = doc.item_code
        item_name = doc.web_item_name
        permalink = "https://example.com/product" + doc.web_item_name
        brand = doc.brand
        item_group = doc.item_group
        image = "https://ibc.erpcloud.systems" + doc.website_image
        date_created = doc.creation
        description = doc.web_long_description
        short_description = doc.description
        price = frappe.db.get_value('Item Price', {'item_code': sku, 'price_list': price_list}, ['price_list_rate'])
        category_id = frappe.db.get_value('Item Group', doc.item_group, 'category_id')
        if doc.published == 1:
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
        data["description"] = doc.web_long_description
        data["short_description"] = doc.web_long_description
        images = []
        images.append({"src": image})
        data["images"] = images
        categories = []
        categories.append({"id": category_id})
        data["categories"] = categories
        woocommerce_id = doc.woocommerce_id
        # frappe.msgprint(json.dumps(data))

        headeroauth = OAuth1(woocommerce_user_key, woocommerce_user_secret, None, None, signature_method='HMAC-SHA1')
        headers = {'content-type': 'application/json;charset=utf-8',
                   "Content-Length": "376"
                   }
        response = requests.post(url="https://demo.nv-host.com/ibcegypt/wp-json/wc/v3/products/" + str(woocommerce_id),
                                 data=json.dumps(data), auth=headeroauth, headers=headers)
        
@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
