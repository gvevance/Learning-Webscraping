# helper function


def print_details(obj,session):

    soup = obj.get_soup(session)
    title = obj.extract_title(soup)
    rating = obj.extract_rating(soup)
    del_date = obj.extract_deliver_by(soup)
    price = obj.extract_price(soup)
    review_count = obj.extract_review_count(soup)
    
    print(f"\n{title}")
    print(f"Rating : {rating}")
    print(f"Price : {price}")
    print(f"Review count : {review_count}")
    print(f"Delivery date : {del_date}")
  
    go = input("\nDo you want to go to the Amazon listing ? (yes/NO) ")
    if go == "yes" :
        obj.goto_link()