# contains class definitions and function defintions

class profile :
    
    # constructor
    def __init__(self,company="ABC",role="SDE",annualctc=0,monthly=0):
        self.company = company
        self.role = role
        self.annualctc = annualctc
        self.monthly = monthly

    # class methods
    def getCompName(self):
        return self.company

    def getRole(self):
        return self.role

    def getAnnualCTC(self):
        return self.annualctc

    def getMonthlySalary(self):
        return self.monthly


