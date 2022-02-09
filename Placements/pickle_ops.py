# pickle operation functions

import pickle
from os.path import exists
import requests
from bs4 import BeautifulSoup

from helper import getCredentials
from helper import display
from extract_details import extract_details


login_page = 'https://placement.iitm.ac.in/students/login.php'
credfile = "placements_ID.txt"
database = "placements.db"
picklefile = "placements.pkl"


def store_in_pickle(object,picklefile_obj):
    pickle.dump(object,picklefile_obj)


def pickle_print_all(picklefile_obj):
    
    while True :
    
        try :
            obj = pickle.load(picklefile_obj)
            print(obj.get_all())

        except EOFError:
            break


def pickle_file_creation():

    if exists(picklefile):
        
        rewrite_pkl = input("Pickle file exists. Do you want to rewrite it ? (yes/no) ")

        if rewrite_pkl == "yes" :

            username,password = getCredentials(credfile)
            
            payload = {
                'rollno' : username ,
                'pass'   : password ,
                'submit' : 'Login'
            }

            # clear file            
            with open(picklefile,"w"):
                pass

            # step 2 - open session
            with requests.Session() as session :
                
                session.post(login_page,data=payload).text      # login [look up Reference 3]

                # step 3 - get URLs of all profiles
                url_all_companies = 'https://placement.iitm.ac.in/students/comp_list_all.php'   # link to get to all companies
                source = session.get(url_all_companies).text                # return html of the URL
                soup = BeautifulSoup(source,'html.parser')                  # send to Beuatifulsoup to parse it

                # opening pickle file
                
                pfile = open(picklefile,'ab+')

                bad_count = 0
                verbose = False
                for result in soup.find_all("a",onclick='OpenPopup(this.href); return false'):  # all profile links have this tag
                    profile,bad_data_count = extract_details(session,result)
                    bad_count += bad_data_count
                    
                    if verbose :
                        display(profile)
                    
                    store_in_pickle(profile,pfile)

                pfile.close()                
                print(f"Bad data count = {bad_count}")

            
    else :      # if pickle file does not exist, create it without asking for user-input
        
        username,password = getCredentials(credfile)
        
        payload = {
            'rollno' : username ,
            'pass'   : password ,
            'submit' : 'Login'
        }

        with requests.Session() as session :
                
            session.post(login_page,data=payload).text      # login [look up Reference 3]

            # step 3 - get URLs of all profiles
            url_all_companies = 'https://placement.iitm.ac.in/students/comp_list_all.php'   # link to get to all companies
            source = session.get(url_all_companies).text                # return html of the URL
            soup = BeautifulSoup(source,'html.parser')                  # send to Beuatifulsoup to parse it

            # opening pickle file
            
            pfile = open(picklefile,'ab+')

            bad_count = 0
            verbose = False
            for result in soup.find_all("a",onclick='OpenPopup(this.href); return false'):  # all profile links have this tag
                profile,bad_data_count = extract_details(session,result)
                bad_count += bad_data_count
                
                if verbose :
                    display(profile)
                
                store_in_pickle(profile,pfile)

            pfile.close()            
            print(f"Bad data count = {bad_count}")

    
    # print all objects
    printall = input("Do you want to print all objects ? (yes/no) ")
    if printall == "yes" :
        pfile = open(picklefile,'rb')       # create "file" object
        pickle_print_all(pfile)             # send it to read and print all
        pfile.close()                       # close the file

    # create an file object again
    pfile = open(picklefile,'rb')

    return pfile
