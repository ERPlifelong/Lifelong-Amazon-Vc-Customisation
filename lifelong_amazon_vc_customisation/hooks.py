app_name = "lifelong_amazon_vc_customisation"
app_title = "Lifelong Amazon Vc Customisation"
app_publisher = "plifelong"
app_description = "Lifelong Amazon VC Customisation"
app_email = "contact@pwctech.in"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/lifelong_amazon_vc_customisation/css/lifelong_amazon_vc_customisation.css"
# app_include_js = "/assets/lifelong_amazon_vc_customisation/js/lifelong_amazon_vc_customisation.js"

# include js, css files in header of web template
# web_include_css = "/assets/lifelong_amazon_vc_customisation/css/lifelong_amazon_vc_customisation.css"
# web_include_js = "/assets/lifelong_amazon_vc_customisation/js/lifelong_amazon_vc_customisation.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "lifelong_amazon_vc_customisation/public/scss/website"

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

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "lifelong_amazon_vc_customisation/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "lifelong_amazon_vc_customisation.utils.jinja_methods",
# 	"filters": "lifelong_amazon_vc_customisation.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "lifelong_amazon_vc_customisation.install.before_install"
# after_install = "lifelong_amazon_vc_customisation.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "lifelong_amazon_vc_customisation.uninstall.before_uninstall"
# after_uninstall = "lifelong_amazon_vc_customisation.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "lifelong_amazon_vc_customisation.utils.before_app_install"
# after_app_install = "lifelong_amazon_vc_customisation.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "lifelong_amazon_vc_customisation.utils.before_app_uninstall"
# after_app_uninstall = "lifelong_amazon_vc_customisation.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "lifelong_amazon_vc_customisation.notifications.get_notification_config"

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

doc_events = {
	"Stock Ledger Entry": {
		"before_submit": "lifelong_amazon_vc_customisation.doctype_events.stock_ledger_entry.before_submit"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"lifelong_amazon_vc_customisation.tasks.all"
# 	],
# 	"daily": [
# 		"lifelong_amazon_vc_customisation.tasks.daily"
# 	],
# 	"hourly": [
# 		"lifelong_amazon_vc_customisation.tasks.hourly"
# 	],
# 	"weekly": [
# 		"lifelong_amazon_vc_customisation.tasks.weekly"
# 	],
# 	"monthly": [
# 		"lifelong_amazon_vc_customisation.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "lifelong_amazon_vc_customisation.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"create_amazon_vc_so": "lifelong_amazon_vc_customisation.wrapper.create_amazon_vc_so",
    "cancel_amazon_vc_so": "lifelong_amazon_vc_customisation.wrapper.cancel_amazon_vc_so",
    "create_amazon_vc_dn": "lifelong_amazon_vc_customisation.wrapper.create_amazon_vc_dn",
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "lifelong_amazon_vc_customisation.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["lifelong_amazon_vc_customisation.utils.before_request"]
# after_request = ["lifelong_amazon_vc_customisation.utils.after_request"]

# Job Events
# ----------
# before_job = ["lifelong_amazon_vc_customisation.utils.before_job"]
# after_job = ["lifelong_amazon_vc_customisation.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"lifelong_amazon_vc_customisation.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

