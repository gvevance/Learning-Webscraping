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
    currency = soup.find("td",width="464",valign="top").text

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
        payslabs[degree]=[currency,ctc,gross_taxable,fixed_basic_pay,others]
    
    # code to extract branches within each degree
    
    if "MTech" in payslabs:
        #! there is an error here. "find_next" is not correct
        for res in soup.find_all("table",cellpadding="0",cellspacing="0",width="690"):
            for res2 in res.find_all("tr") :
                if res2.find('b'):
                    if res2.b.text == "M.Tech / M.S":
                        MTech_list = res2.b.find_next("p").text.split('*')[1:]
                        MTech_branches = [i.strip() for i in MTech_list if i.strip().endswith("[M.Tech]")]
                        payslabs["MTech"].append(MTech_branches)
                        # print("MTech : ",end='')
                        # print(MTech_branches)

    if "M.B.A." in payslabs:
        pass
    
    if "M.S" in payslabs:
        #! there is an error here. "find_next" is not correct
        for res in soup.find_all("table",cellpadding="0",cellspacing="0",width="690"):
            for res2 in res.find_all("tr"):
                if res2.find("p"):
                    if res2.p.text.strip().endswith("[M.S]"):
                        MS_list = res2.p.text.strip('*')[1:]
                        MS_branches = [i.strip() for i in MS_list]
                        payslabs["M.S"].append(MS_branches)
                        print("DD : ",end='')
                        print(MS_branches)

    
    if "Dual Degree" in payslabs:
        for res in soup.find_all("table",cellpadding="0",cellspacing="0",width="690"):
            if res.b.text == "Post Graduate Degree" and res.b.find_next("b").text == "Dual Degree*":
                DD_list = res.find_next("p").text.split('*')[1:]
                DD_branches = [i.strip() for i in DD_list]
                payslabs["Dual Degree"].append(DD_branches)
                # print("DD : ",end='')
                # print(DD_branches)
        
    if "Ph.D." in payslabs:
        for res in soup.find_all("table",cellpadding="0",cellspacing="0",width="690"):
            if res.b.text == "Ph.D" :
                PhD_list = res.find_next("td",valign="top").text.split('*')[1:]
                PhD_branches = [i.strip() for i in PhD_list]
                payslabs["Ph.D."].append(PhD_branches)
                # print("PhD : ",end='')
                # print(PhD_branches)
    
    if "M.A." in payslabs:
        pass
        # for res in soup.find_all("table",cellpadding="0",cellspacing="0",width="690"):
        #     if res.b.text == "Post Graduate Degree" and res.b.find_next("b").text == "M.Tech / M.S":
        #         MTech_list = res.find_next("p").text.split('*')[1:]
        #         MTech_branches = [i.strip() for i in MTech_list if i.strip().endswith("[M.Tech]")]
        #         payslabs["MTech"].append(MTech_branches)
    
    if "BTech" in payslabs:
        btech_list= soup.find("table",cellpadding="0",cellspacing="0",width="690").p.text.split('*')[1:]
        btech_branches = [i.strip() for i in btech_list]
        payslabs["BTech"].append(btech_branches)
        # print("BTech : ",end='')
        # print(btech_branches)
    
    if "M.Sc." in payslabs:
        pass

    return title,designation,offer_nature,payslabs


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
        soup = BeautifulSoup(source,'html.parser')                 # send to Beuatifulsoup to parse it

        testing = False
        
        if testing :

            result = soup.find_all("a",onclick='OpenPopup(this.href); return false')[14]
            title,designation,offer_nature,payslabs = extract_details(session,result)
            print(f"{title}")

        
        else :

            for result in soup.find_all("a",onclick='OpenPopup(this.href); return false'):  # all profile links have this tag
                title,designation,offer_nature,payslabs = extract_details(session,result)
                print(f"{title}")

        
if __name__ == "__main__" :
    main()