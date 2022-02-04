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

from locale import currency
import requests
from bs4 import BeautifulSoup
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
    soup = BeautifulSoup(source,'html.parser')

    '''
    title - td,width="80%"
    job designation - td width="377"
    type of offer - td valign="top" width="380"
    nature of profile - td height="32" align="right"

    '''

    title = soup.find("td",width="80%").text.strip()
    designation = soup.find("td",width="377").text.strip()
    offer_nature = soup.find("td",valign="top",width="380").text.strip()
    currency = soup.find("td",width="464",valign="top").text.split("\n")[0]

    # Extracting CTC related information
    tempsoup = soup.body.find("table",border=1)
    payslabs = {}
    for item in tempsoup.tr.find_next_siblings():   
    # The first tr tag is the titles of the table. Get all the "next siblings" (same level) with the tr tag
        
        degree = item.find("td",width="20%").text.strip()
        ctc = item.find("td",width="14%").text
        gross_taxable = item.find("td",width="13%").text
        fixed_basic_pay = item.find("td",width="16%").text
        others = item.find("td",width="16%").find_next_sibling().text
        # "fixed pay" and "others" have the same tags so used find_next_sibling() on the first occurrence ...
        # (fixed pay column) to get the second one (others column)
        if int(ctc) != 0 or int(gross_taxable) != 0 or int(fixed_basic_pay) != 0 :
            payslabs[degree]=[currency,ctc,gross_taxable,fixed_basic_pay,others]

    # code to extract branches within each degree
    
    if "BTech" in payslabs:
        btech_list= soup.find("table",cellpadding="0",cellspacing="0",width="690").p.text.split('*')[1:]
        # the first table will be BTech if it is there (checked at if "BTech" in payslabs).
        btech_branches = [i.strip() for i in btech_list]
        payslabs["BTech"].append(btech_branches)
        # print("BTech : ",end='')
        # print(btech_branches)
    
    if "Dual Degree" in payslabs:
        for res in soup.find_all("table",cellpadding="0",cellspacing="0",width="690"):
            if res.b.text == "Post Graduate Degree" and res.b.find_next("b").text == "Dual Degree*":
                try :
                    DD_list = res.find_next("p").text.split('*')[1:]
                    DD_branches = [i.strip() for i in DD_list]
                    payslabs["Dual Degree"].append(DD_branches)
                    # print("DD : ",end='')
                    # print(DD_branches)
                except :
                    pass
                
    if "MTech" in payslabs :
        for res in soup.find_all("table",cellpadding="0",cellspacing="0",width="690"):
            for res2 in res.find_all("tr"):
                if res2.find("b") and res2.b.text.strip() == "M.Tech / M.S" :
                    try :

                        MTech_list = res2.find_next_sibling().p.text.strip().split("*")[1:]
                        MTech_branches = [i.strip() for i in MTech_list]
                        payslabs["MTech"].append(MTech_branches)
                        # print("DD : ",end='')
                        # print(DD_branches)
                    except :
                        print("Except of Mtech branch")
            
    if "M.S" in payslabs :
        for res in soup.find_all("table",cellpadding="0",cellspacing="0",width="690"):
            for res2 in res.find_all("tr"):
                if res2.find("b") and res2.b.text.strip() == "M.Tech / M.S" :
                    try :

                        MS_list = res2.find_next_sibling().p.text.strip().split("*")[1:]
                        if len(MS_list) == 1 and MS_list[0].strip() == "All" :
                            MS_branches = [MS_list[0].strip()]
                            payslabs["M.S"].append(MS_branches)
                            # print("MS : ",end='')
                            # print(MS_branches)
                        else :
                            MS_list = res2.find_next_siblings()[1].p.text.strip().split("*")[1:]
                            MS_branches = [i.strip() for i in MS_list]
                            payslabs["M.S"].append(MS_branches)                   
                    except :
                        print("Except of MS branch")

    if "Ph.D." in payslabs:
        for res in soup.find_all("table",cellpadding="0",cellspacing="0",width="690"):
            if res.b.text == "Ph.D" :
                try :
                    PhD_list = res.find_next("td",valign="top").text.split('*')[1:]
                    PhD_branches = [i.strip() for i in PhD_list]
                    payslabs["Ph.D."].append(PhD_branches)
                    # print("PhD : ",end='')
                    # print(PhD_branches)
                except :
                    pass

    if "M.Sc." in payslabs:
        for res in soup.find_all("table",cellpadding="0",cellspacing="0",width="690"):
            for res2 in res.find_all("tr"):
                if res2.find("b") and res2.b.text.strip() == "M.Sc":                   # short-circuiting used
                    try :
                        MSc_list = res2.find_next_sibling().p.text.strip().split('*')[1:]
                        MSc_branches = [i.strip() for i in MSc_list]
                        payslabs["M.Sc."].append(MSc_branches)
                        # print("MSc : ",end='')
                        # print(MSc_branches)
                    except :
                        pass

    if "M.B.A." in payslabs:
        for res in soup.find_all("table",cellpadding="0",cellspacing="0",width="690"):
            for res2 in res.find_all("tr"):
                if res2.find("b") and res2.b.text.strip() == "M.B.A":                   # short-circuiting used
                    # there is a rogue result which does not have a sibling. Don't use that.
                    try:                                
                        MBA_list = res2.find_next_sibling().p.text.strip().split('*')[1:]
                        MBA_branches = [i.strip() for i in MBA_list]
                        payslabs["M.B.A."].append(MBA_branches)
                        # print("MBA : ",end='')
                        # print(MBA_branches)
                    except:
                        pass
                    
    if "M.A." in payslabs:
        for res in soup.find_all("table",cellpadding="0",cellspacing="0",width="690"):
            for res2 in res.find_all("tr"):
                if res2.find("b") and res2.b.text.strip() == "M.A":                   # short-circuiting used
                    try:                                
                        MA_list = res2.find_next_sibling().p.text.strip().split('*')[1:]
                        MA_branches = [i.strip() for i in MA_list]
                        payslabs["M.A."].append(MA_branches)
                        print("MA : ",end='')
                        print(MA_branches)
                    except:
                        pass

    missing_data_count = 0
    for key in payslabs:
        if len(payslabs[key]) != 6 :
            missing_data_count += 1

    return title,designation,offer_nature,payslabs,missing_data_count


def display(title,designation,offer_nature,payslabs):
    
    print(f"Title - {title}")
    print(f"Designation - {designation}")
    print(f"Nature of offer - {offer_nature}")
    
    for key in payslabs:

        print(f"\nDegree : {key}")
        print("Eligible for branches : ")
        
        try :
            currency,ctc,gross_taxable,fixed_basic_pay,others,branches = payslabs[key]
            for branch in branches:
                print(f"* {branch}")
            print(f"\nCTC - {currency} {ctc} ")
            print(f"Gross Taxable Income - {currency} {gross_taxable}")
            print(f"Fixed basic pay - {currency} {fixed_basic_pay}")
            print(f"Others - {others}")
        
        except :
            # Some discrepency in the data of this company
            print("Bad data.")
    
    print("\n")

def update_database(title,designation,offer_nature,payslabs):
    pass


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

        # step 3 - get URLs of all profiles
        url_all_companies = 'https://placement.iitm.ac.in/students/comp_list_all.php'   # link to get to all companies
        source = session.get(url_all_companies).text        # return html of the URL
        soup = BeautifulSoup(source,'html.parser')                 # send to Beuatifulsoup to parse it

        count = 0
        verbose = True
        for result in soup.find_all("a",onclick='OpenPopup(this.href); return false'):  # all profile links have this tag
            title,designation,offer_nature,payslabs,missing_data_count = extract_details(session,result)
            count += missing_data_count
            if verbose :
                display(title,designation,offer_nature,payslabs)
            update_database(title,designation,offer_nature,payslabs)
        
        print(f"Count = {count}")


if __name__ == "__main__" :
    main()