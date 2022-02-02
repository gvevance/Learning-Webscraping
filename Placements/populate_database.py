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
# TODO : EXTRACT ELIGIBILITY (BRANCHES OPEN TO)

import requests
from bs4 import BeautifulSoup
from os.path import exists
import sqlite3

login_page = 'https://placement.iitm.ac.in/students/login.php'
picklefile = "profiles.pkl"
credfile = "placements_ID.txt"
database = "placements.db"


def getCredentials():

    with open(credfile) as cfile :
        username = cfile.readline().strip()
        password = cfile.readline().strip()

    return username , password


def extract_details(session,result):
    
    str1 = 'https://placement.iitm.ac.in/students/'
    source = session.get(str1+result['href']).text
    soup = BeautifulSoup(source,'lxml')

    '''
    title - td,width="80%"
    job designation - td width="377"
    type of offer - td valign="top" width="380"
    nature of profile - td height="32" align="right"

    '''

    title = soup.find("td",width="80%").text.strip()
    designation = soup.find("td",width="377").text.strip()
    offer_nature = soup.find("td",valign="top",width="380").text.strip()

    tempsoup = soup.body.find("table",border=1)
    payslabs = []
    for item in tempsoup.tr.find_next_siblings():   
    # The first tr tag is the titles of the table. Get all the "next siblings" (same level) with the tr tag
        
        degree = item.find("td",width="20%").text
        ctc = item.find("td",width="14%").text
        gross_taxable = item.find("td",width="13%").text
        fixed_basic_pay = item.find("td",width="16%").text
        others = item.find("td",width="16%").find_next_sibling().text
        # "fixed pay" and "others" have the same tags so used find_next_sibling() on the first occurrence ...
        # (fixed pay column) to get the second one (others column) '''
        
        payslabs.append((degree,ctc,gross_taxable,fixed_basic_pay,others))

    return title,designation,offer_nature,payslabs


def init_db(rewrite):
    ''' initialise database. If it is being rewritten, delete old file.'''

    if rewrite :
        open(database,"w").close()

    dbfile = open(database,"w+")
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()

    c.execute('''CREATE TABLE profiles(
            Title text ,
            Designation text ,
            "Nature of Offer" text 
            )''')
    return conn , c


def update_db(title,designation,offer_nature,payslabs):
    
    conn = sqlite3.connect(database)
    c = conn.cursor()


def main():
    
    # step 1
    username,password = getCredentials()
    
    payload = {
        'rollno' : username ,
        'pass'   : password ,
        'submit' : 'Login'
    }

    # step 2 - open session
    with requests.Session() as session :
        
        session.post(login_page,data=payload).text      # login [look up Reference 3]

        # get URLs of all profiles
        url_all_companies = 'https://placement.iitm.ac.in/students/comp_list_all.php'   # link to get to all companies
        source = session.get(url_all_companies).text        # return html of the URL
        soup = BeautifulSoup(source,'lxml')                 # send to Beuatifulsoup to parse it
        
        if exists(database) :
            choice = input(f"Database {database} already exists. Rewrite ? (yes/no) : ")

            if choice == "yes" :
                conn , c = init_db(rewrite=True)   # initialise database after deleting old file
                for result in soup.find_all("a",onclick='OpenPopup(this.href); return false'):  # all profile links have this tag
                    title,designation,offer_nature,payslabs = extract_details(session,result)
                    update_db(title,designation,offer_nature,payslabs)
            else :
                exit()

        else :
            conn , c = init_db(rewrite=False)   # initialise database from scratch
            for result in soup.find_all("a",onclick='OpenPopup(this.href); return false'):  # all profile links have this tag
                title,designation,offer_nature,payslabs = extract_details(session,result)
                update_db(title,designation,offer_nature,payslabs)


if __name__ == "__main__" :
    main()