from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv

# Get the directory where the .env file is located (this case on microblog/)
basedir = os.path.abspath(os.path.dirname('microblog'))
load_dotenv(os.path.join(basedir, '.env'))

BASETESTURL = os.getenv('SELENIUM_TEST_URL')


def login_procedure(driver, username, password):
    driver.get(BASETESTURL)
    user_input = driver.find_element(By.ID, 'username')
    user_input.send_keys(username)

    pass_input = driver.find_element(By.ID, 'password')
    pass_input.send_keys(password)

    submit_input = driver.find_element(By.ID, 'submit')
    submit_input.click()


def register_procedure(driver, username, password):
    driver.get(BASETESTURL + "auth/register")

    user_register_input = driver.find_element(By.ID, 'username')
    user_register_input.send_keys(username)

    email_register_input = driver.find_element(By.ID, 'email')
    email_register_input.send_keys(f'{username}@gmail.com')

    pass_register_input = driver.find_element(By.ID, 'password')
    pass_register_input.send_keys(password)

    pass_confirm_register_input = driver.find_element(By.ID, 'password2')
    pass_confirm_register_input.send_keys(password)

    register_input = driver.find_element(By.ID, 'submit')
    register_input.click()

    login_procedure(driver, username, password)


def login(driver, username, password):
    login_procedure(driver, username, password)

    # We want to register the user if they have not been registered before
    # We know they haven't been registered if they are not redirected to the home page on login
    if driver.current_url != BASETESTURL:
        register_procedure(driver, username, password)
