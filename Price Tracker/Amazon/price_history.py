# price history functions

import sqlite3
import pickle
import requests

from classes import search_result_class
from helper import print_details


def add_to_track_queue(session) :

    link = input("Enter link : ")
    obj = search_result_class(link)
    try :
        print_details(obj,session)

        track = input("Do you want to add this product to the track queue ? (yes/NO) ")
        if track == "yes" :
            pass

    except requests.exceptions.MissingSchema :
        print("Invalid URL entered. Aborting ... ")
    
    except Exception as e:
        print(f"Error = {e}")
        exit()



def check_price_from_PH_queue(session) :
    pass


def view_all_from_PH_queue(session) :
    pass


def price_history_menu(session) :

    print("\nPrice history menu\n")
    print("1. Enter product to track queue \n2. Check price of product in track queue \n\
3. View current price of all products in track queue \n4. Exit")
    
    PH_menu_choice = input("\nEnter option : ")

    if PH_menu_choice == '1' :
        add_to_track_queue(session)

    elif PH_menu_choice == '2' :
        check_price_from_PH_queue(session)

    elif PH_menu_choice == '3' :
        view_all_from_PH_queue(session)

    elif PH_menu_choice == '4' :
        exit()

    else :
        print("Wrong option entered. Aborting ... ")
        exit()

 