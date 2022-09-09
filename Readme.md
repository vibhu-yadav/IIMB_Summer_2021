

First of all , the script "create_dirs.sh" should be used to create the folders for all the courts

The scripts should be run in the following order:

1. **ct_home.py** : To scrape the home pages
2. **ct_doc.py** : To scrape the individiual docs for a court and case types
3. **check.py :** To check if there are missing docs

To run any of these over a entire court for a period of years (2012-2021), use the following bash command:

 **for i in {2012..2021}; do echo $i; python3 `<filename> `--idx `<court_id> --$i;`**


Additionally, the script "get_missing.sh" can be used after running the check.py loop to save the missing files.
