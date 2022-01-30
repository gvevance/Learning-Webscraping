# fetch the required details from the site

# Reference 1 - https://www.youtube.com/watch?v=RsQ1tFLwldY&t=306s
# Reference 2 - https://docs.python-requests.org/en/latest/user/quickstart/

# Step 1 - Figure out login page. Login into portal.
# Step 2 - click companies hyperlink and go to the next page
# Step 3 - Loop through relevant job profiles. Click on each profile and retrieve details.
# Step 4 - Store it in a database or something similar (learn databases)

import requests
from bs4 import BeautifulSoup

login_page = 'https://placement.iitm.ac.in/students/login.php'

def main():
    
    source = requests.get(login_page).text
    soup = BeautifulSoup(source,'lxml')
    # print(soup.prettify())

    match = soup.find("title")
    print(match)

if __name__ == "__main__" :
    main()
