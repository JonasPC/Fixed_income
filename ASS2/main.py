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

to_latex_table('ex11', df1, directory='ASS2', index=True)

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

to_latex_table('ex12', df2, directory='ASS2', index=True, nr_decimals=1)
