from fileinput import filename
import json
from logging import warning
from lxml import html
import pandas as pd
from tqdm import tqdm
from doc_scraping import get_details
import warnings, os, sys
warnings.filterwarnings("ignore")
import argparse

from lists import COURTS, cols, folders

# This script converts the scraped data into a pandas dataframe and saves it as a excel file

parser=argparse.ArgumentParser()

# These are optional arguments to help run the script from terminal
# For eg., to run for Court with idx = 0 (KKD) for years 2012 to 2021, run:
# for i in {2012..2021}; do echo $i; python3 doc2data.py --idx 0 --year $i; done

parser.add_argument('--idx','-i', help='Index of Court based [refer to lists.py]')
parser.add_argument('--year','-y', help='Enter year to be scraped')

# If you need to specify a certain range of case types to scrape, do so using "start" and "end" arguments
parser.add_argument('--start','-s', help='Enter start index of case number')
parser.add_argument('--end','-e', help='Enter end index of case number')

args=parser.parse_args()

idx = 0
if args.idx is not None:
    idx = int(args.idx)
    print(f"Scraping FOR COURT: {COURTS[idx]['court_name']} \n\n")

year = "2012"
if args.year is not None:
    year = args.year
    print(f"Scraping FOR YEAR: {year} \n")

court_name = COURTS[idx]["court_name"]
folder_name = COURTS[idx]["folder_name"]
url = COURTS[idx]["url"]

print("\nScraping " + court_name + " for " + year)

# Starting Folder
st = 0
if args.start is not None:
    st = int(args.start)

# Ending Folder
en = len(folders)
if args.end is not None:
    en = int(args.end)

df = pd.DataFrame(columns=cols)

for i,folder in enumerate(folders[st:en],start=st):

    print(str(i) + " : " +folder)

    doc_path = "./COURTS/" + folder_name + "/" + year + "/" +  folder + "/" + "page.html"

    try:
        with open(doc_path,'r') as f:
            home = f.read()
            # &nbsp and \xa0 are html tags to represent a whitespace
            # They are unnecessary trouble and can be removed
            home = home.replace("\xa0","")
            home = home.replace("&nbsp;","")
            page = html.fromstring(home)

        # Get the table
        table = page.xpath("//div[@id='showList']/table/tbody/tr")

        # Get the path to the files
        files_path = "./COURTS/" + folder_name + "/" + year + "/" +  folder + "/" 

        # Iterate over the rows in the table
        for row in tqdm(table):

            try:
                srno = row.xpath("./td[1]/text()")[0]
                case_info = row.xpath(".//td[@class = 'col-xs-3']/text()")[0]
                parties = row.xpath(".//td[@class = 'col-xs-3'][2]//text()")[1::2]
                # view = row.xpath(".//td[@class = 'col-xs-2']/a")[0]

                row_data = {
                    'srno' : srno,
                    'case_info' : case_info,
                    'parties' : parties,
                    # 'view' : view.attrib['href']
                }

                with open(files_path + srno + ".html",'r') as f:
                    doc = f.read()
                    doc = doc.replace("\xa0","")
                    doc = doc.replace("&nbsp;","")
                    tree = html.fromstring(doc)

                # Get the details from the document
                ans = get_details(row_data,tree)

                # Append the details to the dataframe
                df = df.append(ans,ignore_index=True)

            except:
                pass

        print(df.shape)
        # file_name = "./output/" + folder_name + "/" + year + "/" + str(i) +  ".xlsx"
        # df.to_excel(file_name,index = False )
    except:
        pass

print("Saving Data to Excel...")

print(df.shape)
# pd.set_option('display.max_columns', None)

file_name = "./output/" + folder_name + "/" + year + ".xlsx"

df.to_excel(file_name,index = False )

# cols = ['Id', 'CombinedCaseNumber', 'CaseNumber', 'CaseType', 'Year', 'CourtName', 'CourtHallNumber', 'Bench', 'DateFiled', 'CaseClassification', 
#     'OrderType', 'Petitioner', 'PetitionerAdvocate', 'Respondent', 'RespondentAdvocate', 'CurrentStage', 'CurrentStatus', 'District', 'LastActionTaken', 
#     'LatestOrder', 'BeforeHonarbleJudges', 'LastPostedFor', 'LastDateOfAction', 'NextHearingDate', 'LowerCourtName', 'LowerCourtCaseNumber', 
#     'LowerCourtOtherDetails', 'LowerCourtDisposalDate', 'CaseGroup', 'LastSyncTime', 'RespondentType', 'PetitionerType', 'PresentedOn', 'BenchCategory', 
#     'CaseOriginatedFrom', 'ListedTimes', 'Act', 'DisposalDate', 'LastListedOn', 'CaseCategory', 'CurrentPosition', 'NextListingPurpose', 'Purpose', 
#     'FilingNumber', 'SerialNumber', 'cnr_number', 'CaseUpdateOn', 'PoliceStationName', 'NextListingCourt', 'RegistrationDate', 'ActionDate', 
#     'NextListingDate', 'StageName', 'PostingStage', 'ListingDate', 'NextListingTime', 'DepartmentName', 'LowerCourtJudgmentDate', 'PresentDate', 
#     'StampNumber', 'DateOfHearing', 'LowerCourtDistrict', 'LowerCourtJudges', 'Subject', 'CauseListDate', 'RegistrationNo', 'DecisionDate', 
#     'NatureOfDisposal', 'PetitionerAddress', 'RespondentAddress', 'UnderActs', 'UnderSections', 'PoliceStation', 'FIRNo', 'BusinessOnDate', 
#     'hearing_business', 'CourtState', 'CourtType', 'CourtDistrict', 'StageOfCase', 'CourtComplex', 'FirstHearingDate', 'ParsingYear', 'Njdg_Judge_Name', 
#     'Full_Identifier', 'CaseUniqueValue', 'NoOfHearings', 'NoOfOrders', 'JudgementPDFlink', 'JudgementContent']
