'''
collate info from multiple runs of sim_expts.py
- calculate summary stats for shiny app
'''

import pandas as pd  
import socket
import os
import matplotlib.pylab as plt
import glob

if 'tom' in socket.gethostname():
    os.chdir('/home/tom/Dropbox/university/toys/ddm_sims/')
else:
    print("assuming running in host directory")





filenames=glob.glob('store*.csv')


store_df=pd.DataFrame(columns=['sample_size', 'RT_effect_size', 'Acc_effect_size', 'Drift_effect_size',
       'RTsig', 'Acsig', 'Drsig'])

for filename in filenames:

    df=pd.read_csv(filename,index_col='Unnamed: 0')

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
    
    pd.DataFrame(prop_p_values_RTs).reset_index().merge(pd.DataFrame(prop_p_values_Acc).reset_index()).merge(pd.DataFrame(prop_p_values_Drf).reset_index())
    
    
        
    RT_es=df.groupby('sample_size')['RT_effect_size'].mean()
    Ac_es=df.groupby('sample_size')['Acc_effect_size'].mean()
    Dr_es=df.groupby('sample_size')['Drift_effect_size'].mean()
    
    summary_df=pd.concat([pd.concat([RT_es,Ac_es,Dr_es],axis=1),pd.concat([prop_p_values_RTs,prop_p_values_Acc,prop_p_values_Drf],axis=1)],axis=1).reset_index()
    
    store_df=pd.concat([store_df,summary_df])        
    

store_df.to_csv('summary.csv')