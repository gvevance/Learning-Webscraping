# fetch the required details from the site

# Reference 1 - https://www.youtube.com/watch?v=RsQ1tFLwldY&t=306s
# Reference 2 - https://docs.python-requests.org/en/latest/user/quickstart/
# Reference 3 - https://www.youtube.com/watch?v=fmf_y8zpOgA

# Step 1 - Figure out login page. Login into portal.
# Step 2 - click companies hyperlink and go to the next page
# Step 3 - Loop through relevant job profiles. Click on each profile and retrieve details.
# Step 4 - Store it in a database or something similar (learn databases)

import requests
from bs4 import BeautifulSoup

login_page = 'https://placement.iitm.ac.in/students/login.php'

def main():
    
    payload = {
        'rollno' : 'ee17b105' ,
        'pass' : 'pen-paper-movie@20-21' ,
        'submit' : 'Login'
    }
    
    with requests.Session() as s :
        
        source = s.post(login_page,data=payload).text
        soup = BeautifulSoup(source,'lxml')    
        for tag in soup.find_all("a"):
            print(tag.text)


if __name__ == "__main__" :
    main()

