import numpy as np
import pandas as pd
from modules.immunization import Immunization
from modules.utils import to_latex_table

# %%
############## EX. 1.1 #################################
# Creating the instances of GIC's
gic1 = Immunization(0.020, 2)
gic2 = Immunization(0.020, 3)

# computing the NPV of future payments
pv_gic1, pv_gic2 = gic1.pv(100000, 2), gic2.pv(110000, 3)
pv_liability = pv_gic1 + pv_gic2
dur_liability = pv_gic1 / (pv_gic1 + pv_gic2) * gic1.liquidation + \
    pv_gic2 / (pv_gic1 + pv_gic2) * gic2.liquidation
#del pv_gic1, pv_gic2

cbb = gic1.cbb_price(0.05, 5)
frb = 1

# duration of the two types of bonds
dur_cbb = gic1.duration(5, bond_type='CBB', list_of_prices=cbb)
dur_frb = gic1.duration(1, bond_type='ZCB')

# Making weights
w1 = gic1.weights(dur_liability, dur_cbb, dur_frb)

investment = gic1.investment(w1[0], w1[1], pv_liability)
result_1_1 = [investment[0] / np.sum(cbb), investment[1] / frb]

print(result_1_1)

Investment = {'CBB': result_1_1[0], 'FRB': result_1_1[1]}
df1 = pd.DataFrame(Investment, index=['Amount investable'])

#to_latex_table('ex11', df1, directory='ASS2', index=True)

# %%
############## EX 1.2 #################
# Creating the instances of GIC's
gic1 = Immunization(0.024, 2)
gic2 = Immunization(0.024, 3)

cbb = np.sum(gic1.cbb_price(0.05, 5))
frb = 1.02 * np.exp(-0.024 * 1)

pv_gic1, pv_gic2 = gic1.pv(100000, 2), gic2.pv(110000, 3)
V_liabilities = pv_gic1 + pv_gic2

cbb_notion, frb_notion = result_1_1[0], result_1_1[1]
V_assets = np.sum([cbb * cbb_notion, frb * frb_notion])

Values = {'V assets': V_assets, 'V liabilities': V_liabilities}
df2 = pd.DataFrame(Values, index=['V'])

#to_latex_table('ex12', df2, directory='ASS2', index=True, nr_decimals=1)


# %%
############# EX 2.2 #####################

_cbb2 = gic1.cbb_price(0.02, 2)
cbb2 = np.sum(np.array(_cbb2))
frb2 = 1
dur_cbb2 = gic1.duration(2, bond_type='CBB', list_of_prices=_cbb2)
dur_frb2 = 0.5
_cbb = gic1.cbb_price(0.05, 5)
cbb = np.sum(_cbb)
dur_cbb  = gic1.duration(4, bond_type='CBB', list_of_prices =_cbb[1:])
#%%
print('prices', cbb, frb, cbb2, frb2)
print('durations', dur_cbb, dur_frb, dur_cbb2, dur_frb2)
# %%
Values2 = {'CBB_4': cbb, 'CBB_2': cbb2, 'FRB': frb, 'FRB_0.5': frb2}
df3 = pd.DataFrame(Values2, index=['Prices'])
Values3 = {'CBB_4': dur_cbb, 'CBB_2': dur_cbb2, 'FRB': dur_frb, 'FRB_0.5': dur_frb2}
df4 = pd.DataFrame(Values3, index=['Duration'])
df5 = pd.concat([df3, df4])
#to_latex_table('ex21', df5, directory='ASS2', index=True, nr_decimals=2)
#%% Minimizing 






