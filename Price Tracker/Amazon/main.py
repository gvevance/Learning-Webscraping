# search prices in Amazon

from menu_init import session_init


def main() :
    
    print("\nAmazon Price Tracker\n")
    print("1. Search for product \n2. Get details by link \n\
        3. Price history by link \n4. Exit \n")
    menu_choice = input("Enter option : ")

    if menu_choice in ['1','2','3'] :
        session_init(menu_choice)

    elif menu_choice == '4':
        exit()

    else :
        print("Wrong option entered. Aborting ... ")
        exit()


if __name__ == "__main__" :
    main()