# database operations

import sqlite3

from pickle_ops import pickle_file_creation


login_page = 'https://placement.iitm.ac.in/students/login.php'
credfile = "placements_ID.txt"
database = "placements.db"
picklefile = "placements.pkl"


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


def populate_db(file_exists):

    if file_exists :
        with open(database,'w') :       # clear file     
            pass

    # step 1
    pickle_file_creation()

    conn,c = db_init(database)

    # Add code for database populating here

    conn.commit()
    conn.close()


