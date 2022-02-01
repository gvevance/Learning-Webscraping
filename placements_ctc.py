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

import requests
from bs4 import BeautifulSoup

login_page = 'https://placement.iitm.ac.in/students/login.php'
picklefile = "profiles.pkl"
credfile = "placements_ID.txt"


def getCredentials():

    with open(credfile) as cfile :
        username = cfile.readline().strip()
        password = cfile.readline().strip()

    return username , password


def main():
    
    username,password = getCredentials()
    
    payload = {
        'rollno' : username ,
        'pass'   : password ,
        'submit' : 'Login'
    }

    link_dict = {} 
    with requests.Session() as s :
        
        s.post(login_page,data=payload).text

        # get links of all profiles
        url_all_companies = 'https://placement.iitm.ac.in/students/comp_list_all.php'
        source = s.get(url_all_companies).text
        soup = BeautifulSoup(source,'lxml')
        str1 = 'https://placement.iitm.ac.in/students/'
        
        count = 0
        for result in soup.find_all("a",onclick='OpenPopup(this.href); return false'):
            
            # --------------------------------- remove -------------------------------------
            count = count + 1
            
            if count > 3 :
                continue
            # -------------------------------------------------------------------------------

            source = s.get(str1+result['href']).text
            soup = BeautifulSoup(source,'lxml')

            '''
            title - td,width="80%"
            job designation - td width="377"
            type of offer - td valign="top" width="380"
            nature of profile - td height="32" align="right"

            '''
            # print title, designation, nature of offer ( Domestic / International )
            print(soup.find("td",width="80%").text.strip())
            print(soup.find("td",width="377").text.strip())
            print(soup.find("td",valign="top",width="380").text.strip())
            print()

            tempsoup = soup.body.find("table",border=1)
            for item in tempsoup.tr.find_next_siblings():   
            # The first tr tag is the titles of the table. Get all the "next siblings" (same level) with the tr tag
                branch = item.find("td",width="20%").text
                ctc = item.find("td",width="14%").text
                gross_taxable = item.find("td",width="13%").text
                fixed_basic_pay = item.find("td",width="16%").text
                others = item.find("td",width="16%").find_next_sibling().text
                # "fixed pay" and "others" have the same tags so used find_next_sibling() on the first occurrence ...
                # (fixed pay column) to get the second one (others column) '''
                
                print(f"Branch - {branch}")
                if ctc :   
                # Logic : if ctc is not empty, print it (some companies don't fill some details)
                    print(f"CTC - {ctc}")
                if gross_taxable :
                    print(f"Gross Taxable Income - {gross_taxable}")
                if fixed_basic_pay :
                    print(f"Fixed Basic Pay - {fixed_basic_pay}")
                if others :
                    print(f"Others - {others}")
                print("")

            link_dict[soup.find("td",width="80%").text.strip()] = str1+result['href']
            # storing title as key and link as value
        
        # testing speed of solution to see if it's enough
        query = input("Enter query to search for : ")

        for key in link_dict :
            if query in key :
                source = s.get(link_dict[key]).text
                soup = BeautifulSoup(source,'lxml')
                print(soup.find("td",width="80%").text.strip())
                print()


if __name__ == "__main__" :
    main()