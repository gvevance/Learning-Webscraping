# fetch the required details from the site

# Reference 1 - https://www.youtube.com/watch?v=RsQ1tFLwldY&t=306s
# Reference 2 - https://docs.python-requests.org/en/latest/user/quickstart/
# Reference 3 - https://www.youtube.com/watch?v=fmf_y8zpOgA
# Reference 4 - https://www.tutorialspoint.com/beautiful_soup/beautiful_soup_navigating_by_tags.htm
# Reference 5 - https://www.geeksforgeeks.org/navigation-with-beautifulsoup/

# Step 1 - Figure out login page. Login into portal.
# Step 2 - Simulate click companies hyperlink and go to the next page (or find out how to, in requests library)
# Step 3 - Loop through relevant job profiles. Click on each profile and retrieve details (simulate it).
# Step 4 - Store it in a database or something similar (learn databases)

# TODO : POPULATE A DATABASE (SQLITE)

import requests
from bs4 import BeautifulSoup

from extract_details import extract_details
from helper import getCredentials
from helper import display
from database_ops import update_database

login_page = 'https://placement.iitm.ac.in/students/login.php'
credfile = "placements_ID.txt"
database = "placements.db"


def main():
    
    # step 1
    username,password = getCredentials(credfile)
    
    payload = {
        'rollno' : username ,
        'pass'   : password ,
        'submit' : 'Login'
    }

    # step 2 - open session
    with requests.Session() as session :
        
        session.post(login_page,data=payload).text      # login [look up Reference 3]

        # step 3 - get URLs of all profiles
        url_all_companies = 'https://placement.iitm.ac.in/students/comp_list_all.php'   # link to get to all companies
        source = session.get(url_all_companies).text        # return html of the URL
        soup = BeautifulSoup(source,'html.parser')                 # send to Beuatifulsoup to parse it

        bad_count = 0
        verbose = True
        for result in soup.find_all("a",onclick='OpenPopup(this.href); return false'):  # all profile links have this tag
            title,designation,offer_nature,payslabs,bad_data_count = extract_details(session,result)
            bad_count += bad_data_count
            if verbose :
                display(title,designation,offer_nature,payslabs)
            update_database(title,designation,offer_nature,payslabs)
        
        print(f"Bad data count = {bad_count}")


if __name__ == "__main__" :
    main()