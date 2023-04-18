import os
from behave import given, then
from dotenv import load_dotenv
from tests.features.loginHelper import login
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

basedir = os.path.abspath(os.path.dirname('microblog'))
load_dotenv(os.path.join(basedir, '.env'))

USERNAME = os.getenv('USERNAMEFORTEST')
PASSWORD = os.getenv('PASSWORDFORTEST')
BASETESTURL = os.getenv('SELENIUM_TEST_URL')


@given('the user is on the edit post page')
def step_given(context):
    options = Options()
    options.add_argument("--headless") # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('start-maximized') #to maximize viewport this should still be headless
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    context.driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
    context.driver.implicitly_wait(5)
    context.driver.get(BASETESTURL)

    login(context.driver, USERNAME, PASSWORD)

    ##Check post with ID = 1 
    context.driver.get(f"{BASETESTURL}/edit_post/1")


@then('the page should have a text field to change their post')
def step_then(context):
    editInput = context.driver.find_element(By.XPATH, "//*[@id='body']")
    assert editInput.is_displayed() is True


@then('the page should have a button to submit their changes')
def step_then(context):
    submitEdit = context.driver.find_element(By.XPATH, "//*[@id='submit']")
    assert submitEdit.is_displayed() is True
