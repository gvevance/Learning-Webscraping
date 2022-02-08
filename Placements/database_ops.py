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


def insert_data(table_name,title,designation,offer_nature,pay_details,conn,c):
    
    currency = pay_details[0]
    ctc = int(pay_details[1])
    gross_taxable = int(pay_details[2])
    fixed_basic_pay = int(pay_details[3])
    others = pay_details[4]

    text = f'''INSERT INTO {table_name} VALUES (?,?,?,?,?,?,?,?)'''
    # dict = {"Title"                 : title ,
    #         "Designation"           : designation ,
    #         "Nature"                : offer_nature ,
    #         "Currency"              : currency ,
    #         "CTC"                   : ctc ,
    #         "Gross"                 : gross_taxable ,
    #         "Fixed"                 : fixed_basic_pay ,
    #         "Others"                : others }
    
    tuple_ = (title,designation,offer_nature,currency,ctc,gross_taxable,fixed_basic_pay,others)

    try :
        c.execute(text,tuple_)
    except Exception as e :
        print("New error type found 3.")
        print(e)
        input()

        
def update_database(title,designation,offer_nature,payslabs,conn,c):
    
    print(title,designation,offer_nature)
    for key in payslabs :
        try :
            for branch in payslabs[key][5]:
                text = f""" CREATE TABLE "{key} {branch}"(
                        Title text ,
                        Designation text ,
                        "Nature of Offer" text ,
                        Currency text ,
                        CTC integer ,
                        "Gross Taxable Income" integer ,
                        "Fixed Basic Pay" integer ,
                        Others text
                        )"""
                try :
                    c.execute(text)
                
                except sqlite3.OperationalError :
                    print(f"Table already exists error.")
                
                except Exception as e :
                    print("New error type found 1")
                    print(e)
                    input()

                table_name = f'''"{key} {branch}"'''
                insert_data(table_name,title,designation,offer_nature,payslabs[key],conn,c)

        except IndexError :
            print("Bad data. Check it out.")
        except Exception as e:
            print("New error type found 2")
            print(e)
            input()

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
        conn.commit()
        conn.close()


