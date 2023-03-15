import os
from dotenv import load_dotenv
from behave import given, when, then
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from tests.features.loginHelper import login

basedir = os.path.abspath(os.path.dirname('microblog'))
load_dotenv(os.path.join(basedir, '.env'))

USERNAME1 = os.getenv('USERNAMEFORTEST')
PASSWORD1 = os.getenv('PASSWORDFORTEST')
BASETESTURL = os.getenv('SELENIUM_TEST_URL')


@given("I am on the home page")
def step_impl(context):
    # Implementation of headless from https://stackoverflow.com/questions/46920243/how-to-configure-chromedriver-to-initiate-chrome-browser-in-headless-mode-throug
    # Stackoverflow post desribes what is goin on with options to enable headless chrome
    options = Options()
    options.add_argument('--headless')  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('start-maximized')  # to maximize viewport this should still be headless
    options.add_argument('disable-infobars')
    options.add_argument('--disable-extensions')
    context.driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
    context.driver.implicitly_wait(5)
    context.driver.get(BASETESTURL)

    # Login and create an archived post
    login(context.driver, USERNAME1, PASSWORD1)

    # Go to the home page
    context.driver.get(BASETESTURL)


@given("I have created a post")
def step_impl(context):
    context.driver.find_element(By.ID, "post").send_keys("Test")
    context.driver.find_element(By.ID, "submit").click()


@when("I click on the Delete link")
def step_impl(context):
    clicked_link = context.driver.find_element(By.LINK_TEXT, 'Delete')
    # Save the post id (found in the span that is the fourth previous sibling) so we can check the correct link later
    context.selected_post_id = clicked_link.find_element(By.XPATH, 'preceding-sibling::*[4]').get_dom_attribute('id')
    clicked_link.click()


# Check that the archived post is no longer there (i.e., cannot find an element with href == context.archive_link_href)
@then("the post should disappear")
def step_impl(context):
    assert context.driver.find_elements(By.ID, context.selected_post_id) == []


@then("a banner should show, saying '{message}'")
def step_impl(context, message):
    banner = context.driver.find_element(
        By.XPATH,
        f'//html/body/div[@class="container"]/div[@class="alert alert-info"]'
    )
    # Check whether the action word ('archived' or 'removed') is in the banner
    assert message == banner.text
