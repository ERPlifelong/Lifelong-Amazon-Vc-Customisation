import frappe
import json
from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note

def get_customer(customer):
    df_settings = frappe.get_cached_doc("Lifelong Amazon DF Settings")
    for c in df_settings.customers:
        if c.df_site_customer == customer:
            return c.customer

def get_warehouse(warehouse):
    df_settings = frappe.get_cached_doc("Lifelong Amazon DF Settings")
    for w in df_settings.warehouse:
        if w.df_site_warehouse == warehouse:
            return w.warehouse

def get_location(warehouse):
    df_settings = frappe.get_cached_doc("Lifelong Amazon DF Settings")
    for w in df_settings.warehouse:
        if w.warehouse == warehouse:
            return w.location

def get_customer_address(warehouse):
    df_settings = frappe.get_cached_doc("Lifelong Amazon DF Settings")
    for w in df_settings.warehouse:
        if w.warehouse == warehouse:
            return w.customer_address

def get_shipping_address(warehouse):
    df_settings = frappe.get_cached_doc("Lifelong Amazon DF Settings")
    for w in df_settings.warehouse:
        if w.warehouse == warehouse:
            return w.shipping_address

def get_company_address(warehouse):
    filters = [
        ["Dynamic Link","link_doctype","=","Warehouse"],
        ["Dynamic Link","link_name","=",warehouse],
    ]
    return frappe.db.get_value("Address", filters=filters)

def set_child_tax_template_and_map(child_item, parent_doc):
    def is_within_valid_range(args, tax):
        if not frappe.utils.flt(tax.maximum_net_rate):
            # No range specified, just ignore
            return True
        elif frappe.utils.flt(tax.minimum_net_rate) <= frappe.utils.flt(args.get("net_rate")) <= frappe.utils.flt(tax.maximum_net_rate):
            return True

        return False


    def get_item_tax_template_parent(args, taxes, out=None, for_validate=False):
        if out is None:
            out = {}
        taxes_with_validity = []
        taxes_with_no_validity = []

        for tax in taxes:
            tax_company = frappe.db.get_value("Item Tax Template", tax.item_tax_template, "company")
            if tax_company == args["company"]:
                if tax.valid_from or tax.maximum_net_rate:
                    # In purchase Invoice first preference will be given to supplier invoice date
                    # if supplier date is not present then posting date
                    validation_date = args.get("bill_date") or args.get("transaction_date")

                    if frappe.utils.getdate(tax.valid_from) <= frappe.utils.getdate(validation_date) and is_within_valid_range(args, tax):
                        taxes_with_validity.append(tax)
                else:
                    taxes_with_no_validity.append(tax)

        if taxes_with_validity:
            taxes = sorted(
                taxes_with_validity, key=lambda i: i.valid_from or tax.maximum_net_rate, reverse=True
            )
        else:
            taxes = taxes_with_no_validity

        if for_validate:
            return [
                tax.item_tax_template
                for tax in taxes
                if (
                    frappe.utils.cstr(tax.tax_category) == frappe.utils.cstr(args.get("tax_category"))
                    and (tax.item_tax_template not in taxes)
                )
            ]

        # all templates have validity and no template is valid
        if not taxes_with_validity and (not taxes_with_no_validity):
            return None

        # do not change if already a valid template
        if args.get("item_tax_template") in {t.item_tax_template for t in taxes}:
            out["item_tax_template"] = args.get("item_tax_template")
            return args.get("item_tax_template")

        for tax in taxes:
            if frappe.utils.cstr(tax.tax_category) == frappe.utils.cstr(args.get("tax_category")):
                out["item_tax_template"] = tax.item_tax_template
                return tax.item_tax_template
        return None

    def get_item_tax_map(company, item_tax_template, as_json=True):
        item_tax_map = {}
        if item_tax_template:
            template = frappe.get_cached_doc("Item Tax Template", item_tax_template)
            for d in template.taxes:
                if frappe.db.get_value("Account", d.tax_type, "company") == company:
                    item_tax_map[d.tax_type] = d.tax_rate

        return json.dumps(item_tax_map) if as_json else item_tax_map


    item = frappe.get_doc("Item", child_item.item_code)
    args = {
        "item_code": item.item_code,
        "posting_date": parent_doc.transaction_date,
        "tax_category": parent_doc.get("tax_category"),
        "company": parent_doc.get("company"),
    }

    child_item.item_tax_template = get_item_tax_template_parent(args, item.taxes)
    if child_item.get("item_tax_template"):
        child_item.item_tax_rate = get_item_tax_map(
            parent_doc.get("company"), child_item.item_tax_template, as_json=True
        )

def add_taxes_from_tax_template(child_item, parent_doc):
    add_taxes_from_item_tax_template = frappe.db.get_single_value(
        "Accounts Settings", "add_taxes_from_item_tax_template"
    )

    if child_item.get("item_tax_rate") and add_taxes_from_item_tax_template:
        tax_map = json.loads(child_item.get("item_tax_rate"))
        for tax_type in tax_map:
            tax_rate = frappe.utils.flt(tax_map[tax_type])
            taxes = parent_doc.get("taxes") or []
            # add new row for tax head only if missing
            found = any(tax.account_head == tax_type for tax in taxes)
            if not found:
                tax_row = parent_doc.append("taxes", {})
                tax_row.update(
                    {
                        "description": str(tax_type).split(" - ")[0],
                        "charge_type": "On Net Total",
                        "account_head": tax_type,
                        "rate": tax_rate,
                    }
                )
                if parent_doc.doctype == "Purchase Order":
                    tax_row.update({"category": "Total", "add_deduct_tax": "Add"})

@frappe.whitelist(allow_guest=True)
def create_amazon_vc_so(amazon_vc_sales_order):
    frappe.session.user = "Administrator"
    try:
        so=json.loads(amazon_vc_sales_order)
        sales_order = frappe.new_doc("Sales Order")
        sales_order.customer = get_customer(so["customer"])
        sales_order.company = "Lifelong Online Retail Private Limited"
        sales_order.set_warehouse = get_warehouse(so["set_warehouse"])
        sales_order.location = get_location(sales_order.set_warehouse)
        sales_order.main_warehouse = frappe.db.get_value("Warehouse", sales_order.set_warehouse, "parent_warehouse")
        sales_order.company_address = get_company_address(sales_order.set_warehouse)
        customer_address = get_customer_address(sales_order.set_warehouse)
        shipping_address = get_shipping_address(sales_order.set_warehouse)
        if customer_address:
            sales_order.customer_address = customer_address
        if shipping_address:
            sales_order.shipping_address_name = shipping_address
        sales_order.transaction_date = so["transaction_date"]
        sales_order.delivery_date = so["delivery_date"]
        sales_order.po_no = so["po_no"]
        sales_order.po_date = so["po_date"]
        sales_order.custom_load_type = "Part Truck"
        for item in so["items"]:
            if frappe.db.exists("Item", item["item_code"]):
                item_code = item["item_code"]
            else:
                item_code = "invalid"
            item_details = {
                "item_code": item_code,
                "customer_item_code": item["customer_item_code"],
                "qty": item["qty"],
                "uom": "Nos",
                "rate": item["rate"],
                "conversion_factor": 1.0,
                "warehouse": sales_order.set_warehouse
            }
            sales_order.append("items", item_details)
        sales_order.run_method("set_missing_lead_customer_details")
        sales_order.run_method("set_price_list_and_item_details")
        if sales_order.customer_gst_state_number != sales_order.company_gst_state_number:
            sales_order.tax_category = "S-Out State"
        else:
            sales_order.tax_category = "S-In State"
        sales_order.set("taxes", [])
        for item in sales_order.items:
            set_child_tax_template_and_map(item, sales_order)
            add_taxes_from_tax_template(item, sales_order)
        sales_order.run_method("calculate_taxes_and_totals")
        sales_order.payment_schedule = []
        sales_order.flags.ignore_permissions = True
        sales_order.insert(ignore_permissions=True)
        # sales_order.submit(ignore_permissions=True)
        frappe.response["message"] = {so["name"]:sales_order.name}
    except Exception:
        frappe.log_error("Amazon VC Sales Order Sync Error")

@frappe.whitelist(allow_guest=True)
def cancel_amazon_vc_so(sales_order):
    frappe.session.user = "Administrator"
    try:
        sales_order = frappe.get_doc("Sales Order", sales_order)
        sales_order.cancel()
    except Exception:
        frappe.log_error("Amazon VC Sales Order Cancel Error")

@frappe.whitelist(allow_guest=True)
def create_amazon_vc_dn(sales_order, amazon_vc_delivery_note):
    frappe.session.user = "Administrator"
    try:
        amazon_vc_delivery_note = json.loads(amazon_vc_delivery_note)
        delivery_note = frappe.get_doc(make_delivery_note(sales_order))
        delivery_note.total_packet = 1.0
        for item in amazon_vc_delivery_note["items"]:
            for i in delivery_note.items:
                if i.item_code == item["item_code"]:
                    i.qty = item["qty"]
                    i.batch_no = item["batch_no"]
                    i.shelf = item["shelf"]
                    i.material_state = item["material_state"]
        delivery_note.insert()
            
    except Exception:
        frappe.log_error("Amazon VC Delivery Note Sync Error")
