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


def db_init(database):
    
    conn = sqlite3.connect(database)
    c = conn.cursor()
    return conn,c


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

    conn,c = db_init(database)

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
            update_database(title,designation,offer_nature,payslabs,conn,c)
        
        print(f"Bad data count = {bad_count}")


def update_database(title,designation,offer_nature,payslabs,conn,c):
    
    print(title,designation,offer_nature)
    for key in payslabs :
        try :
            for branch in payslabs[key][5]:
                text = f""" CREATE TABLE "{key} {branch}"(
                        Title text ,
                        Designation text ,
                        "Nature of Offer" text ,
                        CTC integer ,
                        "Gross Taxable Income" integer ,
                        "Fixed Basic Pay" integer ,
                        Others text
                        )"""
                
            c.execute(text)
        except IndexError :
            print("Bad data. Check it out.")
        except sqlite3.OperationalError:
            print(f"Table already exists error.")
        except :
            input("New error type found.")

        