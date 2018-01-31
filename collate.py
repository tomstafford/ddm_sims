'''
collate info from multiple runs of sim_expts.py
- this version compares a single set of positive runs vs negative runs
'''

import pandas as pd  
import os
#os.chdir('/home/tom/Dropbox/university/toys/ddm_sims/')
from scipy.stats import norm #for Z scores
import matplotlib.pylab as plt

#nulldat=pd.read_csv('/home/tom/Dropbox/university/toys/ddm_sims/python_serial/output/store_nDnB_2017-10-23_15-00-47.csv',index_col='Unnamed: 0')
#realdat=pd.read_csv('/home/tom/Dropbox/university/toys/ddm_sims/python_serial/output/store_eDnB_2017-10-23_01-54-26.csv',index_col='Unnamed: 0')
#figlabel='vanilla'

#nulldat=pd.read_csv('/home/tom/Dropbox/university/toys/ddm_sims/python_serial/output/store_nDeB_2017-10-24_00-33-28.csv',index_col='Unnamed: 0')
#realdat=pd.read_csv('/home/tom/Dropbox/university/toys/ddm_sims/python_serial/output/store_eDeB_2017-10-24_00-30-24.csv',index_col='Unnamed: 0')
#figlabel='boundaryshift'

nulldat=pd.read_csv('/home/tom/Dropbox/university/toys/ddm_sims/store_D0B0.csv',index_col='Unnamed: 0')
realdat=pd.read_csv('/home/tom/Dropbox/university/toys/ddm_sims/store_D1B0.csv',index_col='Unnamed: 0')

figlabel='Simple drift increment between group A and group B'

def calc_positives(df):
    df['RTsig']=((df['p_value_RTs']>0) & (df['p_value_RTs']<0.05))*1 #for fascinating reasons boolean values break the sum function https://github.com/pandas-dev/pandas/issues/3752
    df['Acsig']=((df['p_value_Acc']>0) & (df['p_value_Acc']<0.05))*1 #for fascinating reasons boolean values break the sum function https://github.com/pandas-dev/pandas/issues/3752
    df['Drsig']=(df['p_value_Drift']<0.05)*1 #for fascinating reasons boolean values break the sum function https://github.com/pandas-dev/pandas/issues/3752
    
    total_n=df.groupby('sample_size')['RTsig'].count()
    total_sig=df.groupby('sample_size')['RTsig'].sum()
    
    total_n2=df.groupby('sample_size')['Acsig'].count()
    total_sig2=df.groupby('sample_size')['Acsig'].sum()
    
    total_n3=df.groupby('sample_size')['Drsig'].count()
    total_sig3=df.groupby('sample_size')['Drsig'].sum()
    
    prop_p_values_RTs = (total_sig/total_n)  # Renaming RT Proportion for a separate figure
    prop_p_values_Acc = (total_sig2/total_n2) # Renaming Accuracy Proportion for a separate figure
    prop_p_values_Drf = (total_sig3/total_n3) # Renaming Accuracy Proportion for a separate figure
        
    return pd.DataFrame(data=[prop_p_values_RTs,prop_p_values_Acc,prop_p_values_Drf])

hits=calc_positives(realdat)
FAs_=calc_positives(nulldat)

dprimecorrection=0.01 #adding 1% is better when some FAs = 0 due to low sample size (ie doesn't 'overcorrect' for 0 FA rate)
#add a small amount to any floor or ceiling proportions
FAs_=FAs_+(FAs_==0)*dprimecorrection
FAs_=FAs_-(FAs_==1)*dprimecorrection
hits=hits+(hits==0)*dprimecorrection
hits=hits-(hits==1)*dprimecorrection

dprime=hits.apply(norm.ppf)-FAs_.apply(norm.ppf)

hits.transpose().plot()
plt.ylabel('hits')
plt.ylim([0,1])
plt.savefig('hits'+figlabel+'.png',bbox_inches='tight')

FAs_.transpose().plot()
plt.ylabel('FAs_')
plt.ylim([0,1])
plt.savefig('FAs_'+figlabel+'.png',bbox_inches='tight')

dprime.transpose().plot()
plt.ylabel('d prime')
plt.savefig('dprime'+figlabel+'.png',bbox_inches='tight')
