import os,json, sys, argparse
from lists import COURTS

# This script can be run to check if all the files have been saved and if there are missing cases, mark those

# These are optional arguments to help run the script from terminal
# For eg., to run for Court with idx = 0 (KKD) for years 2012 to 2021, run:
# for i in {2012..2021}; do echo $i; python3 check.py --idx 0 --year $i; done
parser=argparse.ArgumentParser()

parser.add_argument('--idx','-i', help='Index of Court based [refer to lists.py]')
parser.add_argument('--year','-y', help='Enter year to be scraped')

args=parser.parse_args()

idx = 4
if "idx" in args:
    idx = int(args.idx)


court_name = COURTS[idx]["court_name"]
folder_name = COURTS[idx]["folder_name"]
url = COURTS[idx]["url"]

year = "2012"
if "year" in args:
    year = args.year


missing = []
total_cases = 0

archived = 0

folder_path = "./COURTS/" + folder_name + "/" + year + "/"

for i,folder in enumerate(os.listdir(folder_path)):

    case_path = folder_path + folder

    try:
        with open(case_path+"/rows.json") as f:
            rows = json.load(f)
    except:
        continue

    total_cases += len(rows)

    archived += len(os.listdir(case_path)) - 2


    if len(rows) != (len(os.listdir(case_path))-2):

        miss = str(i) + " " + str(i+1) + " " + str(len(os.listdir(case_path))-2) + " " + str(len(rows))
        missing.append(miss)

        print(f"{i}) {folder} : {len(os.listdir(case_path))-2} / {len(rows)}")    

    
print("Total Cases : ", total_cases)

print("Archived Cases : ", archived)

with open("./missing/missing_"+str(year)+".txt",'w') as f:
    for i in missing:
        f.write(i+"\n")

print("\n\n")