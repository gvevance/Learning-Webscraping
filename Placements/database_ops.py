# database operations


import pickle
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


def insert_data(table_name,title,designation,offer_nature,pay_details,c):
    
    currency = pay_details[0]
    ctc = int(pay_details[1])
    gross_taxable = int(pay_details[2])
    fixed_basic_pay = int(pay_details[3])
    others = pay_details[4]

    text = f'''INSERT INTO "{table_name}" VALUES (?,?,?,?,?,?,?,?)''' 
    tuple_ = (title,designation,offer_nature,currency,ctc,gross_taxable,fixed_basic_pay,others)

    try :
        c.execute(text,tuple_)
        # print(f"Entry added to {table_name}")
    except Exception as e :
        print("New error type found 3.")
        print(e)
        input()


def create_tables(profile,c):
    
    for key in profile.get_payslabs_keys() :
        
        try :
                
            for branch in profile.get_branches(key) :
                
                if branch != "All" :

                    table_name = f"{key} {branch}"
                    text = f''' CREATE TABLE "{table_name}"(
                                Title text ,
                                Designation text ,
                                "Nature of Offer" text ,
                                Currency text ,
                                CTC integer ,
                                "Gross Taxable Income" integer ,
                                "Fixed Basic Pay" integer ,
                                Others text
                                )'''

                    c.execute(text)

                    print(f"Table created - {table_name}.")
        
        except sqlite3.OperationalError :
            # table exixts
            # print("Table exists")
            pass

        except IndexError :
            # bad data
            # print("Bad data")
            pass

        except Exception as e:
            
            print("Error found at table creation except clause.")
            print(e)
            input()


def update_database(title,designation,offer_nature,payslabs,c):
    
    for key in payslabs :
        
        try :
            
            for branch in payslabs[key][5] :
                
                if branch == "All" :
                    # get all tables which start with key and insert to each one
                    pass

                else :
                    table_name = f"{key} {branch}"
                    insert_data(table_name,title,designation,offer_nature,payslabs[key],c)

        except IndexError :
            # print("Bad data. Check it out.")
            print("Bad data")

        except Exception as e:
            print("Error found at table update except clause.")
            print(e)
            input()


def populate_db(exists):

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
            profile,bad_data_count = extract_details(session,result)
            bad_count += bad_data_count
            
            if verbose :
                display(profile)
            
            store_in_pickle(profile)

            # create_tables(profile,c)

        # input("Tables created. Press a key to continue.")
        
        # for result in soup.find_all("a",onclick='OpenPopup(this.href); return false'):  # all profile links have this tag
        #     title,designation,offer_nature,payslabs,bad_data_count = extract_details(session,result)
        #     bad_count += bad_data_count
        #     if verbose :
        #         display(title,designation,offer_nature,payslabs)
        #     update_database(title,designation,offer_nature,payslabs,c)

        
        print(f"Bad data count = {bad_count}")
        conn.commit()
        conn.close()


