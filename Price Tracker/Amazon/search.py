# search option functions

from bs4 import BeautifulSoup

from classes import search_result_class
from helper import print_details


def get_search_results(session,query) :
    ''' This function returns results of a search query as a list of soup results. 
        session is an HTTP requests session.
        query is the text to search for. '''

    search_url = f"https://www.amazon.in/s?k={query}&i=aps&ref=nb_sb_ss_ts-doa-p_2_2&crid=OYVDLPMKGY95&sprefix=Ki,aps,28"

    res = session.get(search_url,allow_redirects=True).text
    soup = BeautifulSoup(res,'lxml')
    results = soup.find_all("a",class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
    links = ["http://www.amazon.in"+result['href'] for result in results]

    obj_list = []
    for link in links :
        obj_list.append(search_result_class(link))

    return obj_list


def search_menu(session):

    # searching
    query = input("Enter search query : ")   
    result_obj_list = get_search_results(session,query)

    for i in result_obj_list :
        
        print()
        print_details(i,session)
