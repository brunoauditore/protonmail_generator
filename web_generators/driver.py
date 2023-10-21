from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def get_driver():
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    return driver
