from selenium.webdriver.remote.command import Command
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from pynput.keyboard import Controller, Key
from random_press.unit_data import Unit
import csv
from web_generators.generator_interface import MyGenerator
from web_generators.driver import get_driver
from settings import times_to_click
from settings import min_sleeping_time, middle_sleeping_time, max_sleeping_time, protonmails_filename, \
    jetbrains_filename
from web_generators.generator_interface import create_one


class JetAcc:
    def __init__(self):
        self.unit = Unit()
        self.keyboard = Controller()
        self.driver = get_driver()
        self.proton_login = None
        self.proton_password = None
        self.file_name = "../" + protonmails_filename + '.csv'
        self.jetbrains_accounts = "../" + jetbrains_filename + '.csv'
        self.write = True
        self.data = None

    def start_register_jetbrains(self):
        self.driver.get('https://account.jetbrains.com/login')
        time.sleep(5)
        self.driver.find_element(By.NAME, "email").send_keys(self.proton_login)
        elem = WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@class="btn btn-primary btn-lg sign-up-button eml-submit-btn"]')))
        elem.click()

    def protonmail_login(self):
        """
        Підтверджувати обліковий запис
        """
        try:
            url = 'https://account.proton.me/login?product=mail&language=en'
            self.driver.execute(Command.GET, {'url': url})
            time.sleep(5)

            elem = WebDriverWait(self.driver, max_sleeping_time).until(
                EC.presence_of_element_located((By.ID, 'username')))
            elem.send_keys(self.proton_login)

            elem = WebDriverWait(self.driver, max_sleeping_time).until(
                EC.presence_of_element_located((By.ID, 'password')))
            elem.send_keys(self.proton_password)

            elem = WebDriverWait(self.driver, max_sleeping_time).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//button[text() = "Sign in"]')))
            elem.click()

            time.sleep(max_sleeping_time)

            try:
                try:
                    elem = WebDriverWait(self.driver, max_sleeping_time).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//button[text() = "Skip"]')))
                    elem.click()
                except:
                    pass

                for i in range(3):
                    elem = WebDriverWait(self.driver, max_sleeping_time).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//button[@class="button w100 button-large button-solid-norm"]')))
                    elem.click()
                    time.sleep(1)
            except:
                pass

            self.keyboard.press(Key.tab)
            self.keyboard.press(Key.enter)
            # in message here
            time.sleep(1)
            for i in range(times_to_click):
                self.keyboard.press(Key.tab)
                time.sleep(0.5)
            self.keyboard.tap(Key.enter)
            self.keyboard.press(Key.enter)
            time.sleep(2)

            elem = self.driver.find_element(By.XPATH, '//span[@class="text-bold text-break"]')
            reg_link = elem.text
            print(f"Посилання для продовження реєстрації на Jetbrains: {reg_link}")
            # self.driver.close()
            return reg_link

        except:
            return False

    def continue_registration(self, reg_link):
        # in jetbrains

        self.driver.execute(Command.GET, {'url': reg_link})
        try:
            self.unit.generate_values()
            self.driver.find_element(By.NAME, "firstName").send_keys(self.unit.first_name)
            self.driver.find_element(By.NAME, "lastName").send_keys(self.unit.last_name)
            self.driver.find_element(By.NAME, "userName").send_keys(self.unit.user_name)
            self.driver.find_element(By.NAME, "password").send_keys(self.unit.password)
            self.driver.find_element(By.NAME, "pass2").send_keys(self.unit.password)
            self.driver.find_element(By.NAME, "privacy").click()
            time.sleep(5)

            button = WebDriverWait(self.driver, max_sleeping_time).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//button[text() = "Submit"]')))

            button.click()
        except:
            ValueError("Не зареєстровано!!!")

    def write_jetbrains_data(self, data):
        with open(self.jetbrains_accounts, mode='a+',  newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(data)

    def get_data(self):
        with open(self.file_name, newline='', mode='r') as csvfile:
            for row in csv.reader(csvfile, delimiter=';'):
                yield row

    def generate_account(self, row):
        self.driver.maximize_window()
        self.proton_login, self.proton_password = row
        self.start_register_jetbrains()
        time.sleep(3)
        reg_link = self.protonmail_login()
        time.sleep(5)
        self.continue_registration(reg_link)
        time.sleep(10)
        self.driver.close()
        return self.unit.password

    def generate_one_account(self, row):
        try:
            password = self.generate_account(row)
            row.append(password)
            self.data = row
            if self.write:
                self.write_jetbrains_data(self.data)
                print('Записано!')
        except Exception as exc:
            print(f'Exception: {exc}')

    def generate_accounts(self):
        for row in self.get_data():
            if not row:
                print("Немає доступних скриньок!")
            else:
                self.generate_one_account(row)
        print('finish!')


def generate_with_new_email():
    data = create_one()
    jet_acc = JetAcc()
    jet_acc.write = False
    jet_acc.generate_one_account(row=data)
    return jet_acc.data[0], jet_acc.data[1], jet_acc.data[2]


def generate_from_existing_file():
    jet_acc = JetAcc()
    jet_acc.generate_accounts()
    input("Type something to exit;")
