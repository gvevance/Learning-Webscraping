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

# TODO : POPULATE A DATABASE (SQLITE)

from os.path import exists

from database_ops import populate_db


database = "placements.db"


def main():
    
    print("\nPlacements project - \n")

    if exists(database):
        populate = input("Database exists. Do you want to repopulate it ? (yes/no) ")
        if populate == "yes" or populate == "YES" :
            populate_db(file_exists=True)
    
    else :
        print("Populating database.")
        populate_db(file_exists=False)
    

if __name__ == "__main__" :
    main()