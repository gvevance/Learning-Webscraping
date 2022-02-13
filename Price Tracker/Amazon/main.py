# search prices in Amazon

import requests

from helper import getCredentials
from helper import login_amazon
from helper import get_search_results

credfile = "Amazon_ID.txt"

email,password = getCredentials(credfile)

with requests.Session() as session :

    # login into amazon. session object is sent as a reference so no need of return object
    login_amazon(session,email,password)

    # searching
    query = input("Enter search query : ")   
    result_obj_list = get_search_results(session,query)

    for i in result_obj_list :
        soup = i.get_soup(session)
        print()
        print(i.extract_title(soup))
        print(i.extract_rating(soup))
        print(i.extract_price(soup))
        print(i.extract_review_count(soup))
        print(i.extract_deliver_by(soup))

