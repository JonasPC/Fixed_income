
#Creating the class to do both Exercises
import numpy as np

class Immunization(object):
    """
    computes duration of liabilities and assets and adjusts assets such that the net duration = 0.
    Computes the investable amout in each asset to immunize portfolio
    """
    
    def __init__(self, interest, liquidation):
        self.interest = interest #the flat interest rate 
        self.liquidation = liquidation #time until liquidation of positions, such that contract can be honored
        
    def set_interest(self, interest):
        self.interest = interest
    
    def frb_price(self, maturity):
        list_of_cf = []
        counter = 1
        for i in range(maturity):
            price_cf = (1)*np.exp(-self.interest)
            list_of_cf.append(price_cf)
        return price_cf
    
    def cbb_price(self, c, maturity):
        list_of_cf = []
        for i in range(1, maturity+1):
            if i == maturity:
                price_cf = c*np.exp(-self.interest*i) + 1*np.exp(-self.interest*i)
            else:
                price_cf = c*np.exp(-self.interest*i)
            list_of_cf.append(price_cf)
        return list_of_cf            
    
    def pv(self, future_val, y ):
        pv = future_val*np.exp(-self.interest*y)
        return pv
        
    def duration(self, maturity, bond_type='CBB', list_of_prices = [], n=1):
        array_of_durations = np.array(range(1, n*(maturity+1)))/n
        array_of_prices = np.array(list_of_prices)
        if bond_type == 'ZCB':
            duration = maturity
        elif bond_type == 'CBB':
            duration = sum((array_of_prices*array_of_durations)/sum(array_of_prices))
        else:
            raise Exception('bond_type must be CBB or ZCB')
        return duration
    
    def convexity(self, maturity, list_of_prices = [], n=1):
        array_of_durations = np.array(range(1, n*(maturity+1)))/n
        array_of_prices = np.array(list_of_prices)
        if bond_type == 'ZCB':
            convexity = maturity
        elif bond_type == 'CCB':
            convexity = sum((array_of_prices*array_of_durations**2)/sum(array_of_prices))
        else:
            raise Exception('bond_type must be CBB or ZCB')
        return convexity
        
    def weights(self, duration_liability, duration1, duration2):
        weigth1 = (duration_liability - duration2)/(duration1 - duration2)
        weigth2 = 1 - weigth1
        return [weigth1, weigth2]
    
    def investment(self, weigth1, weigth2, pv_liability):
        investment1 = weigth1*pv_liability
        investment2 = weigth2*pv_liability 
        return [investment1, investment2]
    
    def investment_to_fv(self, investment, price):
        fv = investment/price
        return fv
        
        
        
  
############## EX. 1.1 #################################
#Creating the instances of GIC's 
gic1 = Immunization(0.020, 2)
gic2 = Immunization(0.020, 3)


# computing the NPV of future payments
pv_gic1, pv_gic2 = gic1.pv(100000, 2), gic2.pv(110000, 3)
pv_liability = pv_gic1 + pv_gic2
dur_liability = pv_gic1/(pv_gic1+pv_gic2)*gic1.liquidation + pv_gic2/(pv_gic1+pv_gic2)*gic2.liquidation
#del pv_gic1, pv_gic2

cbb = gic1.cbb_price(0.05, 5)
frb = gic1.frb_price(4)
frb = 1

# duration of the two types of bonds
dur_cbb = gic1.duration(5, bond_type='CBB', list_of_prices = cbb)
dur_frb = gic1.duration(1, bond_type='ZCB')

# Making weights
w1 = gic1.weights(dur_liability, dur_cbb, dur_frb)

investment = gic1.investment(w1[0], w1[1], pv_liability)
result_1_1 = [investment[0]/np.sum(cbb), investment[1]/frb]
                      
print(result_1_1)


