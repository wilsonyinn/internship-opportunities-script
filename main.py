from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = "C:\Program Files (x86)\ChromeDriver\chromedriver.exe"

driver = webdriver.Chrome(PATH)

LINK = "https://www.linkedin.com/jobs/search?keywords=software%20engineer%20intern&location=San%20Francisco%2C%20California%2C%20United%20States&geoId=102277331&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"

#CHANGE THIS TO OBJECT
positions = []
company = []
location = []
date_posted = []

driver.get(LINK)

#LOAD PAGE
for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

#FIND ALL RESULTS W/ SAME XPATH
jobResults = driver.find_elements_by_xpath("//h3[contains(@class,'base-search-card__title')]")
totalResults=len(jobResults)

#EXTRACT THE TEXT
for x in range(totalResults):
    positions.append(jobResults[x].text)

