from behave import given, then
from tests.features.loginHelper import login
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#NOTE this test is limited by the scope of this class
#Ideally you would also test that an sms was received and 
#That once a user inputs the token needed for 2fa access they have 
#2fa enabled

@given('the user is on 2fa page')
def step_given(context) :
    options = Options()
    # options.add_argument("--headless") # Runs Chrome in headless mode.
    # options.add_argument('--no-sandbox') # Bypass OS security model
    # options.add_argument('start-maximized') #to maximize viewport this should still be headless
    # options.add_argument('disable-infobars')
    # options.add_argument("--disable-extensions")
    context.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    context.driver.implicitly_wait(5)
    context.driver.get("http://localhost:5000/")

    login(context.driver)

    context.driver.get("http://localhost:5000/auth/enable_2fa")

@then('the page should have a button to enable 2fa')
def step_then(context) :
    enable2faInput = context.driver.find_element(By.XPATH, "//input[@id='_verification_phone']")
    assert enable2faInput.is_displayed() is True 

@then('the page should have a text field to enter the phone number for 2fa')
def step_then(context) :
    phoneInput = context.driver.find_element(By.XPATH, "//html/body/div[@class='container']/div[@class='row']/div[@class='col-md-4']/form[@class='form']/div[@class='form-group  required']/div/div[@class='iti iti--allow-dropdown iti--separate-dial-code']/input[@id='_verification_phone']")
    assert phoneInput.is_displayed() is True

