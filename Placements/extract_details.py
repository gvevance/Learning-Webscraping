# extract details from the given link

from bs4 import BeautifulSoup

from profile import profile
from get_branches import get_btech_branches
from get_branches import get_dual_branches
from get_branches import get_mtech_branches
from get_branches import get_ms_branches
from get_branches import get_msc_branches
from get_branches import get_phd_branches
from get_branches import get_mba_branches
from get_branches import get_ma_branches

def extract_details(session,result):

    str1 = 'https://placement.iitm.ac.in/students/'
    source = session.get(str1+result['href']).text
    soup = BeautifulSoup(source,'html.parser')

    title = soup.find("td",width="80%").text.strip()
    designation = soup.find("td",width="377").text.strip()
    offer_nature = soup.find("td",valign="top",width="380").text.strip()
    currency = soup.find("td",width="464",valign="top").text.split("\n")[0]

    # Extracting CTC related information
    tempsoup = soup.body.find("table",border=1)
    payslabs = {}
    for item in tempsoup.tr.find_next_siblings():   
    # The first tr tag is the titles of the table. Get all the "next siblings" (same level) with the tr tag
        
        degree = item.find("td",width="20%").text.strip()
        ctc = item.find("td",width="14%").text
        gross_taxable = item.find("td",width="13%").text
 
        fixed_basic_pay = item.find("td",width="16%").text
        others = item.find("td",width="16%").find_next_sibling().text

        # "fixed pay" and "others" have the same tags so used find_next_sibling() on the first occurrence ...
        # (fixed pay column) to get the second one (others column)
 
        if int(ctc) != 0 or int(gross_taxable) != 0 or int(fixed_basic_pay) != 0 :
            payslabs[degree]=[currency,ctc,gross_taxable,fixed_basic_pay,others]

    # code to extract branches within each degree
    
    payslabs = get_btech_branches(soup,payslabs,False)
    payslabs = get_dual_branches(soup,payslabs,False)
    payslabs = get_mtech_branches(soup,payslabs,False)
    payslabs = get_ms_branches(soup,payslabs,False)
    payslabs = get_phd_branches(soup,payslabs,False)
    payslabs = get_msc_branches(soup,payslabs,False)
    payslabs = get_mba_branches(soup,payslabs,False)
    payslabs = get_ma_branches(soup,payslabs,False)

    bad_data_count = 0
    for key in payslabs:
        if len(payslabs[key]) != 6 :
            bad_data_count += 1

    if len(payslabs) == 0 :
        bad_data_count += 1

    temp = profile(title,designation,offer_nature,payslabs)
    
    return temp,bad_data_count