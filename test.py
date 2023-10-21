from selenium import webdriver
from selenium.webdriver.common.by import By

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Navigate to the AliExpress website
driver.get("https://www.aliexpress.com/")

# Click on the "account" link
account_link = driver.find_element(By.XPATH, '//a[@data-role="sign-link"]')
account_link.click()

# Click on the "Register" link
register_link = driver.find_element(By.XPATH, '//a[@data-role="register-link"]')
register_link.click()

# Close the browser
driver.quit()