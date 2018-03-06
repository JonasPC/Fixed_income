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
dur_cbb = gic1.duration(4, bond_type='CBB', list_of_prices=_cbb[1:])
con_cbb = Immunization.convexity(4, _cbb[1:], bond_type='CBB')
con_cbb2 = Immunization.convexity(2, _cbb2, bond_type='CBB')
con_frb = dur_frb**2
con_frb2 = dur_frb2**2
cbb2_notion = 0
frb2_notion = 0
print('prices', cbb, frb, cbb2, frb2)
print('durations', dur_cbb, dur_frb, dur_cbb2, dur_frb2)
print('convexities', con_cbb,  con_frb, con_cbb2, con_frb2)
print('notionals', cbb_notion, frb_notion, cbb2_notion, frb2_notion)

# %%
Values2 = {'CBB_4': cbb, 'CBB_2': cbb2, 'FRB': frb, 'FRB_0.5': frb2}
df3 = pd.DataFrame(Values2, index=['Prices'])
Values3 = {'CBB_4': dur_cbb, 'CBB_2': dur_cbb2, 'FRB': dur_frb, 'FRB_0.5': dur_frb2}
df4 = pd.DataFrame(Values3, index=['Duration'])
df5 = pd.concat([df3, df4])
#to_latex_table('ex21', df5, directory='ASS2', index=True, nr_decimals=2)

dur_liability = pv_gic1 / (pv_gic1 + pv_gic2) * (gic1.liquidation - 1) + \
    pv_gic2 / (pv_gic1 + pv_gic2) * (gic2.liquidation - 1)

con_liability = pv_gic1 / (pv_gic1 + pv_gic2) * (gic1.liquidation - 1)**2 + \
    pv_gic2 / (pv_gic1 + pv_gic2) * (gic2.liquidation - 1)**2

not_list = [cbb_notion, frb_notion, cbb2_notion, frb2_notion]
pri_list = [cbb, frb, cbb2, frb2]

value_assets = np.sum([not_list[i] * pri_list[i] for i in range(len(not_list))])
print(value_assets)

C_l, D_l = dur_liability, con_liability
print(C_l, D_l)

b1 = {'P': cbb, 'D': dur_cbb, 'C': con_cbb, 'N': cbb_notion}
b2 = {'P': frb, 'D': dur_frb, 'C': con_frb, 'N': frb_notion}
b3 = {'P': cbb2, 'D': dur_cbb2, 'C': con_cbb2, 'N': cbb2_notion}
b4 = {'P': frb2, 'D': dur_frb2, 'C': con_frb2, 'N': frb2_notion}

list_of_bonds = [b1, b2, b3, b4]
x0 = [0.25, 0.25, 0.25, 0.25]
opt_sol = Immunization.Practical_immunization(
    list_of_bonds, C_l, D_l, x0=x0, value_assets=value_assets)

opt_sol
print(np.sum(opt_sol.x))

opt_sol
