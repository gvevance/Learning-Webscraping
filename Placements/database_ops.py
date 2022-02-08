# database operations


import sqlite3
import requests
from bs4 import BeautifulSoup

from helper import getCredentials
from extract_details import extract_details
from helper import getCredentials
from helper import display


login_page = 'https://placement.iitm.ac.in/students/login.php'
credfile = "placements_ID.txt"
database = "placements.db"


def repopulate_db(exists):

    if exists :
        with open(database,'w') :       # clear file     
            pass

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
        source = session.get(url_all_companies).text                # return html of the URL
        soup = BeautifulSoup(source,'html.parser')                  # send to Beuatifulsoup to parse it

        bad_count = 0
        verbose = False
        for result in soup.find_all("a",onclick='OpenPopup(this.href); return false'):  # all profile links have this tag
            title,designation,offer_nature,payslabs,bad_data_count = extract_details(session,result)
            bad_count += bad_data_count
            if verbose :
                display(title,designation,offer_nature,payslabs)
            update_database(title,designation,offer_nature,payslabs)
        
        print(f"Bad data count = {bad_count}")


def update_database(title,designation,offer_nature,payslabs):
    print(title,designation,offer_nature)
    for key in payslabs :
        print(key,payslabs[key])


