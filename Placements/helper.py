# helper functions


def getCredentials(credfile):

    with open(credfile) as cfile :
        username = cfile.readline().strip()
        password = cfile.readline().strip()

    return username , password


def display(title,designation,offer_nature,payslabs):
    
    print(f"Title - {title}")
    print(f"Designation - {designation}")
    print(f"Nature of offer - {offer_nature}")
    
    for key in payslabs:

        print(f"\nDegree : {key}")
        print("Eligible for branches : ")
        
        try :
            currency,ctc,gross_taxable,fixed_basic_pay,others,branches = payslabs[key]
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