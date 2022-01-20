from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gspread
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

def extract_data(data, xpath):
    #FIND ALL RESULTS W/ SAME XPATH
    jobResults = driver.find_elements_by_xpath(xpath)
    totalResults=len(jobResults)

    #EXTRACT THE TEXT
    for x in range(totalResults):
        data.append(jobResults[x].text)

def write_to_sheets(data, col, sheet):
    for i in range(2, len(data)):
        sheet.update_cell(i, col, data[i])

for i in range(len(LINKS)):
    LINK = LINKS[i]

    sheet = client.open("Internship Opportunities").get_worksheet(i+1)

    positions = []
    companies = []
    locations = []
    dates_posted = []
    
    driver.get(LINK)

    #LOAD PAGE
    for i in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    extract_data(positions, "//h3[contains(@class,'base-search-card__title')]")
    extract_data(companies, "//h4[contains(@class,'base-search-card__subtitle')]")
    extract_data(locations, "//span[contains(@class,'job-search-card__location')]")
    extract_data(dates_posted, "//time[contains(@class,'job-search-card__listdate')]")

    if (len(positions) == len(companies) == len(locations) == len(dates_posted)):
        print("data categories unequal")
    
    write_to_sheets(positions, 1, sheet)
    write_to_sheets(companies, 4, sheet)
    write_to_sheets(locations, 6, sheet)
    write_to_sheets(dates_posted, 8, sheet)
    