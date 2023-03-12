from behave import given, when, then
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options

USERNAME = "aa"
PASSWORD = "aa"


options = Options()
# options.add_argument("--headless") # Runs Chrome in headless mode.
# options.add_argument('--no-sandbox') # Bypass OS security model
# options.add_argument('start-maximized') #to maximize viewport this should still be headless
# options.add_argument('disable-infobars')
# options.add_argument("--disable-extensions")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.implicitly_wait(5)
driver.get("http://localhost:5000/")

def login():
    userInput = driver.find_element(By.XPATH, "//input[@id='username']")
    userInput.send_keys(USERNAME)

    passInput = driver.find_element(By.XPATH, "//input[@id='password']")
    passInput.send_keys(PASSWORD)

    submitInput = driver.find_element(By.XPATH, "//html/body/div[@class='container']/div[@class='row']/div[@class='col-md-4']/form[@class='form']/input[@id='submit']")
    submitInput.click()

    dump_text = driver.page_source
    print(dump_text)

    #We want to register the user if they have not been registered before
    if (("Hi, aa!" in dump_text) is False):
        driver.get("http://localhost:5000/auth/register")

        userInput = driver.find_element(By.XPATH, "//input[@id='username']")
        userInput.send_keys(USERNAME)

        passInput = driver.find_element(By.XPATH, "//input[@id='password']")
        passInput.send_keys(PASSWORD)

        userInput = driver.find_element(By.XPATH, "//input[@id='username']")
        userInput.send_keys(USERNAME)

        passInput = driver.find_element(By.XPATH, "//input[@id='password']")
        passInput.send_keys(PASSWORD)

        
        submitInput = driver.find_element(By.XPATH, "//html/body/div[@class='container']/div[@class='row']/div[@class='col-md-4']/form[@class='form']/input[@id='submit']")
        submitInput.click()

    driver.get(f'http://localhost:5000/user/{USERNAME}')




