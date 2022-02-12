# search prices in Amazon

import requests

from helper import getCredentials
from helper import login_amazon
from helper import get_search_results

credfile = "Amazon_ID.txt"

email,password = getCredentials(credfile)

with requests.Session() as session :

    soup = login_amazon(session,email,password)

    # searching
    query = input("Enter search query : ")    
    results = get_search_results(session,query)

    for result in results :
        if all([i.lower() in result.text.lower() for i in query.split()]) :
            print(result.text)
