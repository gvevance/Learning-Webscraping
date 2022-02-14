# helper function


def print_details(obj,session,verbose = False):

    soup = obj.get_soup(session)
    title = obj.extract_title(soup)
    rating = obj.extract_rating(soup)
    del_date = obj.extract_deliver_by(soup)
    price = obj.extract_price(soup)
    review_count = obj.extract_review_count(soup)
    
    print(title)
    print(rating)
    print(price)
    print(review_count)
    print(del_date)

            
    if verbose :
        if  del_date == "Delivery date not found." or price == "Price not found." or \
                rating == "Rating not found." or review_count == "Review count not found." :
                
            obj.goto_link()
            input()