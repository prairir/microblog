from behave import given, when, then
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv

#Get the directory where the .env file is located (this case on microblog/)
basedir = os.path.abspath(os.path.dirname('microblog'))
load_dotenv(os.path.join(basedir, '.env'))

BASETESTURL = os.getenv('SELENIUM_TEST_URL')

# #These are here for testing
# options = Options()
# # options.add_argument("--headless") # Runs Chrome in headless mode.
# # options.add_argument('--no-sandbox') # Bypass OS security model
# # options.add_argument('start-maximized') #to maximize viewport this should still be headless
# # options.add_argument('disable-infobars')
# # options.add_argument("--disable-extensions")
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# driver.implicitly_wait(5)
# driver.get("http://localhost:5000/")

def loginProcedure(driver, username, password):

    driver.get(BASETESTURL)
    userInput = driver.find_element(By.ID, 'username')
    userInput.send_keys(username)

    passInput = driver.find_element(By.ID, 'password')
    passInput.send_keys(password)

    submitInput = driver.find_element(By.ID, 'submit')
    submitInput.click()

def registerProcedure(driver, username, password):

    driver.get(BASETESTURL+"auth/register")

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
    
    loginProcedure(driver, username, password)

def login(driver, username, password):

    loginProcedure(driver, username, password)

    # We want to register the user if they have not been registered before
    # We know they haven't been registered if they are not redirected to the home page on login
    if driver.current_url != BASETESTURL:
        registerProcedure(driver, username, password)

# # These are here for testing
# def main():
#     login(driver)

# if __name__ == '__main__':
#     main()


