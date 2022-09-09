#!/bin/bash

# If the ct_doc.py , the script for scraping docs crashes midway or skips some cases
# After getting the details of missing files using check.py, this script can be used to rerun and fetch them.

# You would need to provide the idx of the court as a input
# Run this script as "./get_missing.sh 0" if the court idx is 0.


for file in $(ls "./missing/");
    # do for line in $(cat "./missing/$file");
    do 
    id=$(echo "$file" | cut -d'_' -f2);
    # echo "$id";

    year=$(echo "$id" | cut -d'.' -f1);
    echo "$year"
    
    while IFS= read -r line;

        do read -r st en rwst ttl <<< "$line";
        python3 ct_doc.py --idx $1 --year $year --start $st --end $en --rwst $rwst;

    done < "./missing/$file"
    rm "./missing/$file"
        done;
