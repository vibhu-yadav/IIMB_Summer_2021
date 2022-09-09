"""
This script is for scraping the table for each case_type.
This runs a loop on all case types for selected year, requires manual captcha solving.
Stores the data, containing {case_info, parties, view} in a json file.
'view' contains the javascript command to get doc for each case.
"""

from logging.config import IDENTIFIER
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, tkinter, json
from PIL import Image, ImageTk
from lxml import html
import pandas as pd
# from multiprocessing import cpu_count, Pool
# from concurrent.futures import ThreadPoolExecutor
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from tqdm import tqdm
import warnings, os, sys, argparse
warnings.filterwarnings("ignore")

# from doc_scraping import get_details
from fill_form import fill_form, fill_captcha, verify,process_table
from lists import case_types,cols,COURTS

# These are optional arguments to help run the script from terminal
# For eg., to run for Court with idx = 0 (KKD) for years 2012 to 2021, run:
# for i in {2012..2021}; do echo $i; python3 ct_doc.py --idx 0 --year $i; done
parser=argparse.ArgumentParser()

parser.add_argument('--idx','-i', help='Index of Court based [refer to lists.py]')
parser.add_argument('--year','-y', help='Enter year to be scraped')

# If you need to specify a certain range of case types to scrape, do so using "start" and "end" arguments
parser.add_argument('--start','-s', help='Enter start index')
parser.add_argument('--end','-e', help='Enter end index')

args=parser.parse_args()

# Id of the court to scrape
idx = 0
if args.idx is not None:
    idx = int(args.idx)
    print(f"Scraping FOR COURT: {COURTS[idx]['court_name']} \n\n")

# Year to scrape
year = "2012"
if args.year is not None:
    year = args.year
    print(f"Scraping FOR YEAR: {year} \n")

# Import the court details from lists.py
court_name = COURTS[idx]["court_name"]
folder_name = COURTS[idx]["folder_name"]
url = COURTS[idx]["url"]

# Starting Folder
st = 0
if args.start is not None:
    st = int(args.start)

# Ending Folder
en = len(case_types)
if args.end is not None:
    en = int(args.end)

# This block is used to run the browser in headless mode
# If you want to see the browser in action, comment out the following 3 lines
# And remove the options argument from the webdriver.Chrome() function
chromeOptions = Options()
chromeOptions.headless = True
chromeOptions.add_argument("--headless")
driver = webdriver.Chrome(executable_path="./chromedriver", options= chromeOptions)

for case in tqdm(case_types[st:en]):

    # Load the page on browser
    driver.get(url)

    # Wait for the page to load
    page = EC.presence_of_element_located(('xpath',"//form[@name='frm']"))
    WebDriverWait(driver, 10).until(page)

    # Fill the form
    fill_form(driver,court_name,case,year)

    try:
        # While the captcha is not solved, keep trying
        response = driver.find_element("xpath","//div[@id='errSpan']/p")
        if "invalid" in (response.text.lower()):
            fill_form(driver,court_name,case,year)
    except:
        pass

    rows = []

    # Buffer time to load the page
    time.sleep(2)
    
    try:
        # Wait for the table to load
        table_present = EC.presence_of_element_located(('xpath',"//div[@id='showList']/table/tbody/tr[position() >= 2]"))
        WebDriverWait(driver, 2).until(table_present)

        # Process the table
        tree = html.fromstring(driver.page_source)
        rows = process_table(tree,case)

    except TimeoutException:
        # If the table does not load, it means there are no cases for the given case type
        print("No cases found for : ",case)

    # If there are cases, save the data in a json file
    case_name = case.replace('/','').replace('.','').strip()
    path = "./COURTS/" + folder_name + "/" +  year + "/" + case_name

    # Save the rows in a json file
    with open(path + '/rows.json','w') as f:
        f.write(json.dumps(rows))

    # Save the html content of the home page 
    with open(path + '/page.html','w') as f:
        f.write(driver.page_source)

    # Clear all the cookies
    driver.delete_all_cookies()


driver.quit()

