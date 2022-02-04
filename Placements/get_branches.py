''' helper functions to get branch details and return an updated payslabs
'''

def get_btech_branches(soup,payslabs,verbose):

    if "BTech" in payslabs:
        try :
            btech_list= soup.find("table",cellpadding="0",cellspacing="0",width="690").p.text.split('*')[1:]
            # the first table will be BTech if it is there (checked at if "BTech" in payslabs).
            btech_branches = [i.strip() for i in btech_list]
            payslabs["BTech"].append(btech_branches)
            
            if verbose :
                print("BTech : ",end='')
                print(btech_branches)
        except :
            pass
    return payslabs


def get_dual_branches(soup,payslabs,verbose):

    if "Dual Degree" in payslabs:
        for res in soup.find_all("table",cellpadding="0",cellspacing="0",width="690"):
            if res.b.text == "Post Graduate Degree" and res.b.find_next("b").text == "Dual Degree*":
                try :
                    DD_list = res.find_next("p").text.split('*')[1:]
                    DD_branches = [i.strip() for i in DD_list]
                    payslabs["Dual Degree"].append(DD_branches)
                    
                    if verbose :
                        print("DD : ",end='')
                        print(DD_branches)
                except :
                    pass

    return payslabs


def get_mtech_branches(soup,payslabs,verbose):

    if "MTech" in payslabs :
        for res in soup.find_all("table",cellpadding="0",cellspacing="0",width="690"):
            for res2 in res.find_all("tr"):
                if res2.find("b") and res2.b.text.strip() == "M.Tech / M.S" :
                    try :

                        MTech_list = res2.find_next_sibling().p.text.strip().split("*")[1:]
                        MTech_branches = [i.strip() for i in MTech_list]
                        payslabs["MTech"].append(MTech_branches)
                        
                        if verbose :
                            print("MTech : ",end='')
                            print(MTech_branches)
                    except :
                        print("Except of Mtech branch")
    
    return payslabs


def get_ms_branches(soup,payslabs,verbose):

    if "M.S" in payslabs :
        for res in soup.find_all("table",cellpadding="0",cellspacing="0",width="690"):
            for res2 in res.find_all("tr"):
                if res2.find("b") and res2.b.text.strip() == "M.Tech / M.S" :
                    try :

                        MS_list = res2.find_next_sibling().p.text.strip().split("*")[1:]
                        if len(MS_list) == 1 and MS_list[0].strip() == "All" :
                            MS_branches = [MS_list[0].strip()]
                            payslabs["M.S"].append(MS_branches)
                            
                            if verbose :
                                print("MS : ",end='')
                                print(MS_branches)
                        else :
                            MS_list = res2.find_next_siblings()[1].p.text.strip().split("*")[1:]
                            MS_branches = [i.strip() for i in MS_list]
                            payslabs["M.S"].append(MS_branches)                   
                    except :
                        pass

    return payslabs


def get_phd_branches(soup,payslabs,verbose):

    if "Ph.D." in payslabs:
        for res in soup.find_all("table",cellpadding="0",cellspacing="0",width="690"):
            if res.b.text == "Ph.D" :
                try :
                    PhD_list = res.find_next("td",valign="top").text.split('*')[1:]
                    PhD_branches = [i.strip() for i in PhD_list]
                    payslabs["Ph.D."].append(PhD_branches)
                    
                    if verbose:
                        print("PhD : ",end='')
                        print(PhD_branches)
                except :
                    pass

    return payslabs


def get_msc_branches(soup,payslabs,verbose):

    if "M.Sc." in payslabs:
        for res in soup.find_all("table",cellpadding="0",cellspacing="0",width="690"):
            for res2 in res.find_all("tr"):
                if res2.find("b") and res2.b.text.strip() == "M.Sc":                   # short-circuiting used
                    try :
                        MSc_list = res2.find_next_sibling().p.text.strip().split('*')[1:]
                        MSc_branches = [i.strip() for i in MSc_list]
                        payslabs["M.Sc."].append(MSc_branches)
                        
                        if verbose:
                            print("MSc : ",end='')
                            print(MSc_branches)
                    except :
                        pass

    return payslabs


def get_mba_branches(soup,payslabs,verbose):

    if "M.B.A." in payslabs:
        for res in soup.find_all("table",cellpadding="0",cellspacing="0",width="690"):
            for res2 in res.find_all("tr"):
                if res2.find("b") and res2.b.text.strip() == "M.B.A":                   # short-circuiting used
                    # there is a rogue result which does not have a sibling. Don't use that.
                    try:                                
                        MBA_list = res2.find_next_sibling().p.text.strip().split('*')[1:]
                        MBA_branches = [i.strip() for i in MBA_list]
                        payslabs["M.B.A."].append(MBA_branches)
                        
                        if verbose :
                            print("MBA : ",end='')
                            print(MBA_branches)
                    except:
                        pass

    return payslabs


def get_ma_branches(soup,payslabs,verbose):

    if "M.A." in payslabs:
        for res in soup.find_all("table",cellpadding="0",cellspacing="0",width="690"):
            for res2 in res.find_all("tr"):
                if res2.find("b") and res2.b.text.strip() == "M.A":                   # short-circuiting used
                    try:                                
                        MA_list = res2.find_next_sibling().p.text.strip().split('*')[1:]
                        MA_branches = [i.strip() for i in MA_list]
                        payslabs["M.A."].append(MA_branches)

                        if verbose:
                            print("MA : ",end='')
                            print(MA_branches)
                    except:
                        pass

    return payslabs
