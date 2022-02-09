# helper functions


def getCredentials(credfile):

    with open(credfile) as cfile :
        username = cfile.readline().strip()
        password = cfile.readline().strip()

    return username , password


def display(profile):
    
    print(f"Title - {profile.title}")
    print(f"Designation - {profile.designation}")
    print(f"Nature of offer - {profile.offer_nature}")
    
    for key in profile.get_payslabs_keys():

        print(f"\nDegree : {key}")
        print("Eligible for branches : ")
        
        try :
            currency = profile.get_currency(key)
            ctc = profile.get_ctc(key)
            gross_taxable = profile.get_gross(key)
            fixed_basic_pay = profile.get_fixed_pay(key)
            others = profile.get_others(key)
            branches = profile.get_branch_list(key)

            for branch in branches:
                print(f"* {branch}")
            print(f"\nCTC - {currency} {ctc} ")
            print(f"Gross Taxable Income - {currency} {gross_taxable}")
            print(f"Fixed basic pay - {currency} {fixed_basic_pay}")
            print(f"Others - {others}")
        
        except :
            # Some discrepency in the data of this company
            print("Bad data.")
    
    print("\n")


def get_relevant_branches(key,table_set):
    
    relevant_branches = [branch for branch in table_set if branch.startswith(key)]
    return relevant_branches
