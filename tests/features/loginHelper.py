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

USERNAME = os.getenv('USERNAMEFORTEST')
PASSWORD = os.getenv('PASSWORDFORTEST')
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

def loginProcedure(driver):

    driver.get(BASETESTURL)
    userInput = driver.find_element(By.XPATH, "//input[@id='username']")
    userInput.send_keys(USERNAME)

    passInput = driver.find_element(By.XPATH, "//input[@id='password']")
    passInput.send_keys(PASSWORD)

    submitInput = driver.find_element(By.XPATH, "//html/body/div[@class='container']/div[@class='row']/div[@class='col-md-4']/form[@class='form']/input[@id='submit']")
    submitInput.click()

def registerProcedure(driver):

    driver.get(BASETESTURL+"auth/register")

    userRegisterInput = driver.find_element(By.XPATH, "//html/body/div[@class='container']/div[@class='row']/div[@class='col-md-4']/form[@class='form']/div[@class='form-group  required'][1]/input[@id='username']")
    userRegisterInput.send_keys(USERNAME)

    emailRegisterInput = driver.find_element(By.XPATH, "//html/body/div[@class='container']/div[@class='row']/div[@class='col-md-4']/form[@class='form']/div[@class='form-group  required'][2]/input[@id='email']")
    emailRegisterInput.send_keys(f'{USERNAME}@gmail.com')

    passRegisterInput = driver.find_element(By.XPATH, "//html/body/div[@class='container']/div[@class='row']/div[@class='col-md-4']/form[@class='form']/div[@class='form-group  required'][3]/input[@id='password']")
    passRegisterInput.send_keys(PASSWORD)

    passConfirmRegisterInput = driver.find_element(By.XPATH, "//input[@id='password2']")
    passConfirmRegisterInput.send_keys(PASSWORD)

    regisrerInput = driver.find_element(By.XPATH, "//html/body/div[@class='container']/div[@class='row']/div[@class='col-md-4']/form[@class='form']/input[@id='submit']")
    regisrerInput.click()
    
    loginProcedure(driver)

def login(driver):
   
    loginProcedure(driver)

    dump_text = driver.page_source

    # We want to register the user if they have not been registered before
    # We know they havent been registered if they are no redirected to the home page on login
    if (('Hi, aa!' in dump_text) is False):
        registerProcedure(driver)

# # These are here for testing
# def main():
#     login(driver)

# if __name__ == '__main__':
#     main()


