# database operations

import sqlite3
import pickle

from pickle_ops import pickle_file_populate
from helper import get_relevant_branches


login_page = 'https://placement.iitm.ac.in/students/login.php'
credfile = "placements_ID.txt"
database = "placements.db"
picklefile = "placements.pkl"


def db_init(database):
    
    conn = sqlite3.connect(database)
    c = conn.cursor()
    return conn,c


def insert_data_db(profile,table_set,c):
    
    title = profile.title
    designation = profile.designation
    offer_nature = profile.offer_nature
    
    for key in profile.get_payslabs_keys():

        if profile.check_payslabs_health(key) == "OK" :
            
            currency = profile.get_currency(key)
            ctc = profile.get_ctc(key)
            gross_taxable = profile.get_gross(key)
            fixed_pay = profile.get_fixed_pay(key)
            others = profile.get_others(key)

            for branch in profile.get_branch_list(key):

                if branch == "All" :
                    pass
                    # for i in get_relevant_branches(key,table_set) :
                    #     pass

                else :

                    table_name = f"{key} {branch}"
                    text = f'''INSERT INTO "{table_name}" VALUES (?,?,?,?,?,?,?,?)''' 
                    info_tuple_ = (title,designation,offer_nature,currency,ctc,gross_taxable,fixed_pay,others)
                    
                    try :
                        c.execute(text,info_tuple_)

                    except Exception as e:
                        print(e)
                        input()


def create_table_in_db(table_name,c) :
    
    try :
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

    except sqlite3.OperationalError :
        pass
     
    except Exception as e :
        print(e)
        input()


def create_tables(c):
    
    pfile = open(picklefile,'rb')

    table_set = set()

    while True :
    
        try :
            
            profile = pickle.load(pfile)
            if profile.check_health() == "OK" :
                
                for key in profile.get_payslabs_keys():
                    
                    if profile.check_payslabs_health(key) == "OK" :

                        for branch in  profile.get_branch_list(key) :
                            
                            if branch != "All" :

                                table_name = f"{key} {branch}"
                                create_table_in_db(table_name,c)
                                table_set.add(table_name)
            
            else :
                print(profile.check_health())

        except EOFError:
            break
    
    pfile.close()

    return table_set


def update_database(table_set,c):
    
    pfile = open(picklefile,'rb')

    while True :
    
        try :
            
            profile = pickle.load(pfile)
            
            if profile.check_health() == "OK" :
                
                insert_data_db(profile,table_set,c)  

            else :
                print(profile.check_health())

        except EOFError:
            break
    
    pfile.close()


def populate_db(file_exists):

    # step 1
    pickle_file_populate()

    if file_exists :
        with open(database,'w') :       # clear database file     
            pass

    conn,c = db_init(database)

    # Add code for database populating here

    tables = create_tables(c)

    print_tables = input("Tables created. Do you want to print them ? (yes/no) ")
    if print_tables == "yes" :
        for t in sorted(list(tables)) :
            print(t)

    update_database(tables,c)

    conn.commit()
    conn.close()

