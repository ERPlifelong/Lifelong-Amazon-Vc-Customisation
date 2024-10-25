import frappe
import requests
import json

def before_submit(doc, method=None):
    df_settings = frappe.get_cached_doc("Lifelong Amazon DF Settings")
    if any(w.warehouse == doc.warehouse for w in df_settings.warehouse):
        if check_item_code(doc.item_code):
            try:
                url = "http://65.0.138.58/api/method/update_stock_in_amazon"
                headers = {
                "Content-Type": "application/json"
                }
                data = doc.as_dict().copy()
                data["warehouse"] = get_df_site_warehouse(df_settings, doc.warehouse)
                response = requests.request("POST", url, data=json.dumps(data, default=str), headers=headers)
                if response.status_code == 200:
                    return
                else:
                    raise Exception(f"Error in updating stock in DF Site: {response.status_code} {response.json()}")
            except Exception:
                frappe.log_error("Error in updating stock in DF Site")
                frappe.throw("Error in updating stock in DF Site")


def check_item_code(item_code):
    try:
        url = "http://65.0.138.58/api/method/check_item_code"
        headers = {
        "Content-Type": "application/json"
        }
        response = requests.request("POST", url, data=json.dumps({"item_code": item_code}), headers=headers)
        result = response.json()
        if response.status_code == 200:
            if result.get("message") == True:
                return True
            else:
                raise Exception(f"Item Code not available in DF Site: {response.status_code} {result}")    
        else:
            raise Exception(f"Item Code not available in DF Site: {response.status_code} {result}")
    except Exception:
        frappe.log_error("Item Code not available in DF Site")
        frappe.throw("Item Code not available in DF Site")

def get_df_site_warehouse(df_settings, warehouse):
    for w in df_settings.warehouse:
        if w.warehouse == warehouse:
            return w.df_site_warehouse