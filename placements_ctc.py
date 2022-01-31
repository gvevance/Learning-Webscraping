# fetch the required details from the site

# Reference 1 - https://www.youtube.com/watch?v=RsQ1tFLwldY&t=306s
# Reference 2 - https://docs.python-requests.org/en/latest/user/quickstart/
# Reference 3 - https://www.youtube.com/watch?v=fmf_y8zpOgA

# Step 1 - Figure out login page. Login into portal.
# Step 2 - click companies hyperlink and go to the next page
# Step 3 - Loop through relevant job profiles. Click on each profile and retrieve details.
# Step 4 - Store it in a database or something similar (learn databases)

from turtle import onclick
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

        url_all_companies = 'https://placement.iitm.ac.in/students/comp_list_all.php'
        source = s.get(url_all_companies).text
        soup = BeautifulSoup(source,'lxml')
        for tag in soup.find_all("a",onclick='OpenPopup(this.href); return false'):
            print(tag.text)

if __name__ == "__main__" :
    main()

# <a href="view_profile.php?cid=250&amp;pid=958" onclick="OpenPopup(this.href); return false" style="text-decoration:underline"><font color="blue">Safety Software Engineer</font></a>