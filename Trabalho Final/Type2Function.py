from __future__ import division
class Type2Function(object):
    def __init__(self,centro,min_valor,max_valor,alfa,beta,alfa2):
        self.centro=centro
        self.min=min_valor
        self.max=max_valor
        self.alfa=alfa
        self.beta=beta
        self.alfa2=alfa2

    def get_pert(self,gray_level):
        if (gray_level <= self.min or gray_level>=self.max):
            return 0
        pert=0
        if (gray_level>self.min and gray_level<self.centro):
            pert=(gray_level-self.min)/(self.centro-self.min)
            pert=pert**self.alfa
        else:
            pert=(self.max-gray_level)/(self.max-self.centro)
            pert=pert**self.beta

        return pert

    def get_pert2(self,gray_level,upper):
        pert=self.get_pert(gray_level)
        if(upper):
            return pert**(1/self.alfa2)
        else:
            return pert**self.alfa2

    def adjust_center(self,centro):
        self.centro=centro
        self.min=centro-63
        self.max=centro+63
        if(self.min<0):
            self.min=0
        if(self.max>255):
            self.min=255
