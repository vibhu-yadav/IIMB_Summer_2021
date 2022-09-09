#!/bin/bash

# This bash script is used to create the directories for storing the scraped data as html and json files
# Run this before beginning the scraping process.

for folder in $(ls);
do for year in {2012..2021};
do mkdir "./$folder/$year";
cat "./types.txt" | while read case;
	do mkdir "./$folder/$year/$case";
done;
done;
done;
