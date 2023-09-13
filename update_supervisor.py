from common import *

# NEW SUPERVISOR: EMPLOYEE
employees_to_be_updated = {
    'SUPERVISOR 1': ['EMPLOYEE 1', 'EMPLOYEE 2'],
    'SUPERVISOR 2': ['EMPLOYEE 3'],
    'SUPERVISOR 3': ['EMPLOYEE 4', 'EMPLOYEE 5', 'EMPLOYEE 6']
}


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

try_this(website1.update_employees_supervisor(employees_to_be_updated))
try_this(website2.update_employees_supervisor(employees_to_be_updated))
db.update_supervisors(employees_to_be_updated)
