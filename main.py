from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 
import gspread
import info

from oauth2client.service_account import ServiceAccountCredentials
from constant import LINKS
import time

# *GOOGLE SHEET CREDENTIAL SETUP
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# *CHROME DRIVER SETUP
PATH = "C:\Program Files (x86)\ChromeDriver\chromedriver.exe"
driver = webdriver.Chrome(PATH)

requests = 0

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def extract_link(data, xpath):
    #FIND ALL RESULTS W/ SAME XPATH
    results = driver.find_elements_by_xpath(xpath)
    totalResults=len(results)
    
    #EXTRACT THE TEXT
    for x in range(totalResults):
        data.append(results[x].get_attribute('href'))

def extract_data(data, xpath):
    #FIND ALL RESULTS W/ SAME XPATH
    results = driver.find_elements_by_xpath(xpath)
    totalResults=len(results)

    #EXTRACT THE TEXT
    for x in range(totalResults):
        data.append(results[x].text)

def write_to_sheets(data, col, sheet, requests):
    for i in range(len(data)):
        if not (requests < 60):
            time.sleep(60)
            requests = 0
        if requests < 60:
            sheet.update_cell(i+2, col, data[i])
            requests += 1
    return requests 

#LOG IN

login_link = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
driver.get(login_link)

emailField = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "username"))
)
emailField.send_keys(info.email)

pwField = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "password"))
)
pwField.send_keys(info.password)
signInBtn = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'btn__primary--large from__button--floating')]"))
)

signInBtn.click()

time.sleep(3)

for i in range(len(LINKS)):
    LINK = LINKS[i]
    print(str(i) + ": " + LINK)

    sheet = client.open("Internship Opportunities").get_worksheet(i+1)

    positions = []
    companies = []
    locations = []
    source = []
    
    driver.get(LINK)
    time.sleep(2)

    for i in range(5):
        #LOAD PAGE
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        extract_data(positions, "//a[contains(@class,'disabled ember-view job-card-container__link job-card-list__title')]")
        extract_data(companies, "//a[contains(@class,'job-card-container__link job-card-container__company-name ember-view')]")
        extract_data(locations, "//div[contains(@class, 'artdeco-entity-lockup__caption ember-view')]")
        extract_link(source, "//a[contains(@class,'disabled ember-view job-card-container__link job-card-list__title')]")
    
        #click for next page
        if (check_exists_by_xpath("//button[contains(@aria-label,'Page %d')]" % (i+2))):
            nextPageButton = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label,'Page %d')]" % (i+2)))
            )
            nextPageButton.click()
        else: 
            break

    requests = write_to_sheets(positions, 1, sheet, requests)
    requests = write_to_sheets(companies, 4, sheet, requests)
    requests = write_to_sheets(locations, 6, sheet, requests)
    requests = write_to_sheets(source, 8, sheet, requests)

    print(len(positions))
    print(len(companies))
    print(len(locations))
    print(len(source))