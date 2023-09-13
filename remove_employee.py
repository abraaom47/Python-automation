from common import *

employees_to_be_removed = ['EMPLOYEE 2', 'EMPLOYEE 2', 'EMPLOYEE 3']

website1 = Website('url', 'search_page_url')
website1.login_page.set_user_box("element's XPATH")
website1.login_page.set_password_box("element's XPATH")
website1.login_page.set_login_button("element's XPATH")

website1.search_page.set_search_box("element's XPATH")
website1.search_page.set_search_button("element's XPATH")
website1.search_page.set_result("element's XPATH")

website1.user_page.set_enable_box("element's XPATH")
website1.user_page.set_no_button("element's XPATH")
website1.user_page.set_supervisor_box("element's XPATH")
website1.user_page.set_supervisor_box_list("element's XPATH")
website1.user_page.set_save_button("element's XPATH")
website1.user_page.set_save_yes_button("element's XPATH")


website2 = Website('url', 'search_page_url')
website2.login_page.set_user_box("element's XPATH")
website2.login_page.set_password_box("element's XPATH")
website2.login_page.set_login_button("element's XPATH")

website2.search_page.set_sidebar("element's XPATH")
website2.search_page.set_search_box("element's XPATH")
website2.search_page.set_search_button("element's XPATH")
website2.search_page.set_result("element's XPATH")

website2.user_page.set_enable_box("element's XPATH")
website2.user_page.set_no_button("element's XPATH")
website2.user_page.set_supervisor_box("element's XPATH")
website2.user_page.set_supervisor_box_list("element's XPATH")
website2.user_page.set_save_button("element's XPATH")
website2.user_page.set_save_yes_button("element's XPATH")


db = Database("host", "root", 'db_name')
db.connect()

try_this(website1.remove_employees(employees_to_be_removed))
try_this(website2.remove_employees(employees_to_be_removed))
db.remove_employees(employees_to_be_removed)
