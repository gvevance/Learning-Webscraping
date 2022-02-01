# fetch the required details from the site

# Reference 1 - https://www.youtube.com/watch?v=RsQ1tFLwldY&t=306s
# Reference 2 - https://docs.python-requests.org/en/latest/user/quickstart/
# Reference 3 - https://www.youtube.com/watch?v=fmf_y8zpOgA
# Reference 4 - https://www.tutorialspoint.com/beautiful_soup/beautiful_soup_navigating_by_tags.htm
# Reference 5 - https://www.geeksforgeeks.org/navigation-with-beautifulsoup/

# Step 1 - Figure out login page. Login into portal.
# Step 2 - click companies hyperlink and go to the next page
# Step 3 - Loop through relevant job profiles. Click on each profile and retrieve details.
# Step 4 - Store it in a database or something similar (learn databases)

import numpy as np
import requests
from bs4 import BeautifulSoup

login_page = 'https://placement.iitm.ac.in/students/login.php'

def main():
    
    payload = {
        'rollno' : 'ee17b105' ,
        'pass'   : 'pen-paper-movie@20-21' ,
        'submit' : 'Login'
    }
    
    with requests.Session() as s :
        
        s.post(login_page,data=payload).text

        # get links of all profiles
        url_all_companies = 'https://placement.iitm.ac.in/students/comp_list_all.php'
        source = s.get(url_all_companies).text
        soup = BeautifulSoup(source,'lxml')
        str1 = 'https://placement.iitm.ac.in/students/'
        links = []
        
        for item in soup.find_all("a",onclick='OpenPopup(this.href); return false'):
            links.append(str1+item['href'])

        i = 545

        for i in range(544,548):

            source = s.get(links[i]).text
            soup = BeautifulSoup(source,'lxml')

            '''
            title - td,width="80%"
            job designation - td width="377"
            type of offer - td valign="top" width="380"
            nature of profile - td height="32" align="right"

            '''
            # print title
            print(soup.find("td",width="80%").text.strip())
            print(soup.find("td",width="377").text.strip())
            print(soup.find("td",valign="top",width="380").text.strip())
            print()


            tempsoup = soup.body.find("table",border=1)
            for item in tempsoup.tr.find_next_siblings():
                branch = item.find("td",width="20%").text
                ctc = item.find("td",width="14%").text
                gross_taxable = item.find("td",width="13%").text
                fixed_basic_pay = item.find("td",width="16%").text
                others = item.find("td",width="16%").find_next_sibling().text
                
                print(f"Branch - {branch}")
                if ctc :
                    print(f"CTC - {ctc}")
                if gross_taxable :
                    print(f"Gross Taxable Income - {gross_taxable}")
                if fixed_basic_pay :
                    print(f"Fixed Basic Pay - {fixed_basic_pay}")
                if others :
                    print(f"Others - {others}")
                print("")




if __name__ == "__main__" :
    main()