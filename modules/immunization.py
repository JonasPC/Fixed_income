
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