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
USERNAME2 = os.getenv('USERNAMEFORTEST2')
PASSWORD2 = os.getenv('PASSWORDFORTEST2')
BASETESTURL = os.getenv('SELENIUM_TEST_URL')


@given('that I am logged in')
def open_browser(context):
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
    context.driver.find_element(By.ID, "post").send_keys("Test")
    context.driver.find_element(By.ID, "submit").click()

    # Switch to another user
    context.driver.find_element(By.LINK_TEXT, "Logout").click()
    # context.driver.get(f'{BASETESTURL}/auth/logout')
    context.driver.get(BASETESTURL)
    login(context.driver, USERNAME2, PASSWORD2)


@given("I am on the '{name}' page")
def step_impl(context, name):
    context.driver.find_element(By.LINK_TEXT, name).click()


@when("I click on the '{link_text}' link")
def step_impl(context, link_text):
    clicked_link = context.driver.find_element(By.LINK_TEXT, link_text)
    # Save the post id (found in the span that is the fourth previous sibling) so we can check the correct link later
    context.selected_post_id = clicked_link.find_element(By.XPATH, 'preceding-sibling::*[4]').get_dom_attribute('id')
    clicked_link.click()


@when("I click View Archived Posts")
def step_impl(context):
    context.driver.find_element(By.LINK_TEXT, 'View Archived Posts').click()


# For when the user clicks remove from archive SPECIFICALLY from the archived posts page
@when("I click Remove from Archive")
def step_impl(context):
    clicked_link = context.driver.find_element(By.LINK_TEXT, 'Remove from Archive')
    # Save the post id (found in the span that is the second previous sibling) so we can check the correct link later
    context.selected_post_id = clicked_link.find_element(By.XPATH, 'preceding-sibling::*[2]').get_dom_attribute('id')
    clicked_link.click()


# Check that the archived post is no longer there (i.e., cannot find an element with href == context.archive_link_href)
@then("the archived post should disappear")
def step_impl(context):
    assert context.driver.find_elements(By.ID, context.selected_post_id) == []


@then("the link should change to '{link_text}'")
def step_impl(context, link_text):
    link = context.driver.find_element(By.ID, context.selected_post_id)\
        .find_element(By.XPATH, 'following-sibling::*[4]')
    assert link.text == link_text


@then("a banner should show, saying that the post has been '{action}'")
def step_impl(context, action):
    banner = context.driver.find_element(
        By.XPATH,
        f'//html/body/div[@class="container"]/div[@class="alert alert-info"]'
    )
    # Check whether the action word ('archived' or 'removed') is in the banner
    assert action in banner.text


@then("I should be directed to a page displaying all my archived posts")
def step_impl(context):
    assert 'archived' in context.driver.current_url
