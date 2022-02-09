# class definition

class profile :

    def __init__(self,title,designation,offer_nature,payslabs) :
        self.title = title
        self.designation = designation
        self.offer_nature = offer_nature
        self.payslabs = payslabs


    def check_health(self):
        # payslabs is empty, (add more as they are discovered)
        
        if len(self.payslabs) == 0 :
            return "Paylslabs empty."
        else :
            return "All good."


    def get_all(self):
        return self.title,self.designation,self.offer_nature,self.payslabs


    def get_payslabs_keys(self):
        return [i for i in self.payslabs]


    def check_payslabs_health(self,key):
        
        if len(self.payslabs[key]) != 6 :
            return "No branch list not found."
    
        elif self.payslabs[key][5] == [] :
            return "Branch list is empty"

        else :
            return "All good."


    def get_currency(self,key):
        ''' call after checking health of this class object '''
        return self.payslabs[key][0]


    def get_ctc(self,key):
        ''' call after checking health of this class object '''
        return self.payslabs[key][1]
    

    def get_gross(self,key):
        ''' call after checking health of this class object '''
        return self.payslabs[key][2]


    def get_fixed_pay(self,key):
        ''' call after checking health of this class object '''
        return self.payslabs[key][3]


    def get_others(self,key):
        ''' call after checking health of this class object '''
        return self.payslabs[key][4]

    
    def get_branch_list(self,key):
        return self.payslabs[key][5]


    
    
    