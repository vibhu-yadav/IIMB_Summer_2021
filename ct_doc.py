from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, tkinter, json
from PIL import Image, ImageTk
from lxml import html
import pandas as pd
import argparse

from multiprocessing import cpu_count, Pool
from concurrent.futures import ThreadPoolExecutor

# from doc_scraping.py import get_details
from doc_scraping import get_details

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options

from json.decoder import JSONDecodeError

from tqdm import tqdm
import warnings, os, argparse
warnings.filterwarnings('ignore')

from lists import case_types,COURTS


# These are optional arguments to help run the script from terminal
# For eg., to run for Court with idx = 0 (KKD) for years 2012 to 2021, run:
# for i in {2012..2021}; do echo $i; python3 ct_doc.py --idx 0 --year $i; done
parser=argparse.ArgumentParser()

parser.add_argument('--idx','-i', help='Index of Court based [refer to lists.py]')
parser.add_argument('--year','-y', help='Enter year to be scraped')

# If you need to specify a certain range of case types to scrape, do so using "start" and "end" arguments
parser.add_argument('--start','-s', help='Enter start index')
parser.add_argument('--end','-e', help='Enter end index')

# If the program crashes midway, you can resume from the last case type scraped by specifying the "rwst" (row to start) argument
parser.add_argument('--rwst','-r',help='Row to start from')

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

# This block is used to run the browser in headless mode
# If you want to see the browser in action, comment out the following 3 lines
# And remove the options argument from the webdriver.Chrome() function
chromeOptions = Options()
chromeOptions.headless = True
chromeOptions.add_argument("--headless")
driver = webdriver.Chrome(executable_path="./chromedriver", options= chromeOptions)

folder_path = "./COURTS/" + folder_name + "/" + year + "/"

# Starting Folder
st = 0
if args.start is not None:
    st = int(args.start)

# Ending Folder
en = len(os.listdir(folder_path))
if args.end is not None:
    en = int(args.end)

# Run loop over all the case types to be scraped
for i,folder in enumerate(os.listdir(folder_path)[st:en],start = st):

    # Path to the folder containing the case types
    case_path = folder_path + folder
    rows = []

    try:
        with open(case_path + "/rows.json",'r') as f:
            rows = json.load(f) 
    except JSONDecodeError:
        print(folder + " is empty")
        continue

    driver.get(url)

    time.sleep(2)

    print(f"{i}: Getting Docs for : ",folder)

    rwst = 0
    # The optional row start argument is used to resume from the last case type scraped
    if args.rwst is not None:
        rwst = int(args.rwst)

    for row in tqdm(rows[rwst:]):
        # row['view'] contains the javascript command that opens the case details
        # We execute this command in the browser to open the case details
        cmd = row['view']
        driver.execute_script(cmd)

        # Wait for the case details to load
        data_present = EC.presence_of_element_located(('xpath',"//div[@align='center']"))
        WebDriverWait(driver, 10).until(data_present)

        # Get the page with case details and save as a html
        with open(case_path + "/" + row['srno'] + ".html",'w') as f:
            f.write(driver.page_source)

driver.quit()