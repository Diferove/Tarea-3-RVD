
# Se debe tener instalado QuantLib

# In[1]:

from QuantLib import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#get_ipython().magic('matplotlib inline')


# In[2]:

# IBR
depo_maturities = [Period(1,Days), Period(1, Months), Period(3, Months)]
depo_rates = [6.666, 6.43, 6.115]
# Swaps IBR Bullet
swap_bull_maturities = [Period(6, Months), Period(9, Months), Period(12, Months)]
swap_bull_rates = [5.85, 5.71, 5.54]
# Swaps IBR Trimestral
swap_maturities = [Period(24, Months), Period(36, Months), Period(60, Months), Period(84, Months), Period(120, Months)]
swap_rates = [5.135, 5.12, 5.33, 5.61, 6.05]

maturities = depo_maturities+swap_bull_maturities+swap_maturities
rates = depo_rates+swap_bull_rates+swap_rates
pd.DataFrame(list(zip(maturities, rates)) , columns=["Maturities","Curve"], index=['']*len(rates))
#print_curve(depo_maturities+swap_bull_maturities+swap_maturities, depo_rates+swap_bull_rates+swap_rates)


# In[3]:

calc_date = Date(18, 4, 2017)
Settings.instance().evaluationDate = calc_date
calendar = NullCalendar()
bussiness_convention = Unadjusted
day_count = Actual360()
end_of_month = True
settlement_days_ibr = 0
settlement_days_swap = 2
face_amount = 100
coupon_frequency_bullet = Period(Annual)
coupon_frequency_quarterly = Period(Quarterly)


# In[4]:

depo_helpers = [DepositRateHelper(QuoteHandle(SimpleQuote(r/100.0)),
                                          m,
                                          settlement_days_ibr,
                                          calendar,
                                          bussiness_convention,
                                          end_of_month,
                                          day_count)
                for r, m in zip(depo_rates, depo_maturities)]


# In[5]:

swap_bull_helpers = []
for r, m in zip(swap_bull_rates, swap_bull_maturities):
            termination_date = calc_date + m
            schedule = Schedule(calc_date,
                                termination_date,
                                coupon_frequency_bullet,
                                calendar,
                                bussiness_convention,
                                bussiness_convention,
                                DateGeneration.Backward,
                                end_of_month)
            swap_bull_helper = FixedRateBondHelper(QuoteHandle(SimpleQuote(face_amount)),
                                              settlement_days_swap,
                                              face_amount,
                                              schedule,
                                              [r/100.0],
                                              day_count,
                                              bussiness_convention)
            swap_bull_helpers.append(swap_bull_helper)


# In[6]:

swap_helpers = []
for r, m in zip(swap_rates, swap_maturities):
            termination_date = calc_date + m
            schedule = Schedule(calc_date,
                                termination_date,
                                coupon_frequency_quarterly,
                                calendar,
                                bussiness_convention,
                                bussiness_convention,
                                DateGeneration.Backward,
                                end_of_month)
            swap_helper = FixedRateBondHelper(QuoteHandle(SimpleQuote(face_amount)),
                                              settlement_days_swap,
                                              face_amount,
                                              schedule,
                                              [r/100.0],
                                              day_count,
                                              bussiness_convention)
            swap_helpers.append(swap_helper)


# In[7]:

rate_helpers = depo_helpers + swap_bull_helpers + swap_helpers


# In[9]:

ibr_forward_curve = PiecewiseFlatForward(calc_date, rate_helpers, day_count)


# In[10]:

nodes = list(ibr_forward_curve.nodes())


# In[11]:

nodes[:12]


# In[12]:

fwd = pd.DataFrame(nodes[:12],columns=["Maturities","Curve"])
fwd.iloc[0:12, 0:2]


# In[13]:

fwd['Vencimiento']=[0, 1/30, 1, 3, 6, 9, 12, 24, 36, 60, 84, 120]
fwd['Tasas Forward']=100*fwd['Curve']
fwd.iloc[0:12, 0:4]


# In[14]:

plt.plot(fwd['Vencimiento'],fwd['Tasas Forward'], '-',
                  label="Curva Forward Instantanea")
plt.xlabel("Mes", size=12)
plt.ylabel("Tasa Forward", size=12)
plt.xlim(0,120)
plt.ylim([0,10])
plt.legend()
plt.show()


# In[15]:

madurez = [0,1/3,2/31,1,31/30,3,91/30,6,181/30,9,271/30,12,361/30,24,721/30,36,1081/30,60,1801/30,84,2521/30,120]
tasas = [6.665383,6.665383,6.404126,6.404126,5.898738,5.898738,5.479394,5.479394,5.242475,5.242475,
         4.785799,4.785799,4.794019,4.794019,5.055214,5.055214,5.649194,5.649194,6.415734,6.415734,
         7.406222,7.406222]
curva_fwd = pd.DataFrame(list(zip(madurez, tasas)) , columns=["Vencimiento","Tasas Forward"], 
                         index=['']*len(tasas))


# In[17]:

plt.plot(curva_fwd['Vencimiento'],curva_fwd['Tasas Forward'], '-',
                  label="Curva Forward Instantanea")
plt.xlabel("Mes", size=12)
plt.ylabel("Tasa Forward", size=12)
plt.xlim(0,120)
plt.ylim([0,10])
plt.legend()
plt.show()



