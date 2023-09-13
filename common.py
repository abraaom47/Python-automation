from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time
import mysql.connector
from mysql.connector import Error

driver = webdriver
browser = driver.Chrome()
actions = ActionChains(browser)

user = 'USERNAME'
password = 'PASSWORD'


def try_this(function):
    try:
        function
    except Exception as e:
        print(e)


def await_element(command):
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
    wait = WebDriverWait(browser, 20, ignored_exceptions=ignored_exceptions)
    condition = expected_conditions.element_to_be_clickable(command)
    element = wait.until(condition) 
    return element


class LoginPage:
    def __init__(self, url):
        self.user_box = None
        self.password_box = None
        self.login_button = None
        self.url = url

    def set_user_box(self, xpath):
        self.user_box = xpath

    def set_password_box(self, xpath):
        self.password_box = xpath

    def set_login_button(self, xpath):
        self.login_button = xpath

    def login(self):
        browser.maximize_window()
        browser.set_window_position(-1920, 0)
        browser.get(self.url)

        user_box = browser.find_element(By.XPATH, self.user_box)
        password_box = browser.find_element(By.XPATH, self.password_box)
        login_button = browser.find_element(By.XPATH, self.login_button)

        user_box.send_keys(user)
        password_box.send_keys(password)
        login_button.click()


class SearchPage:

    def __init__(self, url):
        self.search_box = None
        self.search_button = None
        self.result = None
        self.sidebar = None
        self.url = url

    def set_search_box(self, xpath):
        self.search_box = xpath

    def set_search_button(self, xpath):
        self.search_button = xpath

    def set_result(self, xpath):
        self.result = xpath

    def set_sidebar(self, xpath):
        self.sidebar = xpath

    def remove_sidebar(self):
        sidebar = browser.find_element(By.XPATH, self.sidebar)
        browser.execute_script('''
        var element = arguments[0]
        element.parentNode.removeChild(element)
        ''', sidebar)

    def search_employee(self, employee):
        browser.get(self.url)

        try:
            self.remove_sidebar()
        except:
            pass

        search_box = await_element((By.XPATH, self.search_box))
        search_box.send_keys(employee)

        search_button = await_element((By.XPATH, self.search_button))
        search_button.click()

        actions.send_keys('ENTER')

        time.sleep(1)
        result = await_element((By.XPATH, self.result))
        actions.double_click(result).perform()


class UserPage:

    def __init__(self):
        self.enable_box = None
        self.no_button = None
        self.supervisor_box = None
        self.supervisor_box_list = None
        self.save_button = None
        self.save_yes_button = None

    def set_enable_box(self, xpath):
        self.enable_box = xpath

    def set_no_button(self, xpath):
        self.no_button = xpath

    def disable_user(self):
        enable_box = await_element((By.XPATH, self.enable_box))
        enable_box.click()

        no_button = await_element((By.XPATH, self.no_button))
        no_button.click()

    def set_supervisor_box(self, xpath):
        self.supervisor_box = xpath

    def set_supervisor_box_list(self, xpath):
        self.supervisor_box_list = xpath

    def remove_supervisor(self):
        supervisor_box = await_element((By.XPATH, self.supervisor_box))
        actions.move_to_element(supervisor_box).perform()
        supervisor_box.click()
        actions.move_by_offset(0, 20).perform()
        names = browser.find_elements(By.XPATH, self.supervisor_box_list)
        no_supervisor = ''
        for name in names:
            if name.text == 'NONE':
                no_supervisor = name

        actions.scroll_to_element(no_supervisor).perform()
        time.sleep(2)
        no_supervisor.click()

    def change_supervisor(self, desired_supervisor):
        supervisor_box = await_element((By.XPATH, self.supervisor_box))
        actions.move_to_element(supervisor_box).perform()
        supervisor_box.click()
        actions.move_by_offset(0, 20).perform()
        names = browser.find_elements(By.XPATH, self.supervisor_box_list)
        desired_supervisor_button = ''
        for name in names:
            if name.text == desired_supervisor:
                desired_supervisor_button = name

        actions.scroll_to_element(desired_supervisor_button).perform()
        time.sleep(2)
        desired_supervisor_button.click()

    def set_save_button(self, xpath):
        self.save_button = xpath

    def set_save_yes_button(self, xpath):
        self.save_yes_button = xpath

    def save_changes(self):
        save_button = browser.find_element(By.XPATH, self.save_button)
        save_button.click()

        save_yes_button = await_element((By.XPATH, self.save_yes_button))
        actions.double_click(save_yes_button).perform()


class Website:

    def __init__(self, login_url, search_url):
        self.login_page = LoginPage(login_url)
        self.search_page = SearchPage(search_url)
        self.user_page = UserPage()

    def __repr__(self) -> str:
        server = self.login_page.url.split('/')[2]
        website = server.split('.')[-1]
        return f'Website: {website}'

    def update_employees_supervisor(self, employees_to_be_updated):
        self.login_page.login()
        for supervisor in employees_to_be_updated:
            employees = employees_to_be_updated[supervisor]
            if len(employees) > 0:
                print(f"Updating {supervisor}'s team")
                for employee in employees:
                    try:
                        self.search_page.search_employee(employee)
                    except:
                        print(f"User {employee} not found on {self}")
                        continue
                    self.user_page.change_supervisor(supervisor)
                    try:
                        self.user_page.save_changes()
                    except:
                        pass
                    print(f"{employee}'s supervisor updated to {supervisor} "
                          f"on {self}")

    def remove_employees(self, employees_to_be_removed):
        self.login_page.login()
        for employee in employees_to_be_removed:
            try:
                self.search_page.search_employee(employee)
            except:
                print(f'User {employee} not found or already inactive')
                continue
            self.user_page.disable_user()
            self.user_page.remove_supervisor()
            self.user_page.save_changes()
            print(f'{employee} successfully removed from {self}')


class Database:

    def __init__(self, host, user, database):
        self.host = host
        self.user = user
        self.database = database

    def connect(self):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                database=self.database
            )
            print('Connection established')
        except Error as e:
            print(f'The following error occurred: {e}')

        self.connection = connection
        self.cursor = connection.cursor()

    def remove_employees(self, employees_to_be_removed):
        for employee in employees_to_be_removed:
            try:
                query = f"DELETE FROM employees_table WHERE employee = '{employee}'"
                self.cursor.execute(query)
                self.connection.commit()
                print(f'{employee} successfully removed from {self.database}')
            except Error as e:
                print(f'The following error occurred: {e}')

    def update_supervisors(self, employees_to_be_updated):
        supervisors_code_numbers = self.get_supervisors_code_numbers(employees_to_be_updated)
        for supervisor in employees_to_be_updated:
            employees = employees_to_be_updated[supervisor]
            for employee in employees:
                try:
                    query = f"UPDATE employees_table SET supervisor = '{supervisor}', supervisors_code_number = '{supervisors_code_numbers[supervisor]}' " \
                            f"WHERE employee = '{employee}'"
                    self.cursor.execute(query)
                    self.connection.commit()
                    print(f"{employee}'supervisor updated to {supervisor} on {self.database}")
                except Error as e:
                    print(f'The following error occurred: {e}')

    def get_supervisors_code_numbers(self, employees_to_be_updated):
        supervisors_code_numbers = {}
        for supervisor in employees_to_be_updated:
            try:
                query = f"SELECT DISTINCT supervisors_code_number FROM employees_table WHERE supervisor = '{supervisor}'"
                self.cursor.execute(query)
                code_number = self.cursor.fetchall()
                supervisors_code_numbers[supervisor] = code_number[0][0]
            except Error as e:
                print(f'The following error occurred: {e}')
        return supervisors_code_numbers
