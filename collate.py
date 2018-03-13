'''
collate info from multiple runs of sim_expts.py
- calculate summary stats for shiny app
'''

import pandas as pd  
import socket
import os
import glob

#if 'tom' in socket.gethostname():
#    os.chdir('/home/tom/Dropbox/university/toys/ddm_sims/')
#else:
#    print("assuming running in host directory")


#rewrite so 
#1. joins all data
#2. generates summary statistics 


print("stitching source data into single df")

filenames=glob.glob('for_stiching/store*.csv')

for i,filename in enumerate(filenames):

    if i==0: 
        df=pd.read_csv(filename,index_col='Unnamed: 0')
    else:
        df=pd.concat([df,pd.read_csv(filename,index_col='Unnamed: 0')])        



print("creating expt sample size * drift effect size summary table")


#code each p values as significant iff <0.05 and in the right direction
df['RTsig']=((df['p_value_RTs']>0) & (df['p_value_RTs']<0.05))*1 #for fascinating reasons boolean values break the sum function https://github.com/pandas-dev/pandas/issues/3752
df['Acsig']=((df['p_value_Acc']>0) & (df['p_value_Acc']<0.05))*1 #for fascinating reasons boolean values break the sum function https://github.com/pandas-dev/pandas/issues/3752
df['Drsig']=(df['p_value_Drift']<0.1)*1 #for fascinating reasons boolean values break the sum function https://github.com/pandas-dev/pandas/issues/3752

#raw frequencies of significant p values
total_n=df.groupby(['sample_size','Drift_effect_size'])['RTsig'].count()
total_sig=df.groupby(['sample_size','Drift_effect_size'])['RTsig'].sum()
total_n2=df.groupby(['sample_size','Drift_effect_size'])['Acsig'].count()
total_sig2=df.groupby(['sample_size','Drift_effect_size'])['Acsig'].sum()  
total_n3=df.groupby(['sample_size','Drift_effect_size'])['Drsig'].count()
total_sig3=df.groupby(['sample_size','Drift_effect_size'])['Drsig'].sum()

#proportion of significant p values out of total p values
prop_p_values_RTs = (total_sig/total_n)  # Renaming RT Proportion for a separate figure
prop_p_values_Acc = (total_sig2/total_n2) # Renaming Accuracy Proportion for a separate figure
prop_p_values_Drf = (total_sig3/total_n3) # Renaming Accuracy Proportion for a separate figure

 
#get average observed effect size over n simulated experiments for each sample size * Drift ES combination
RT_es=df.groupby(['sample_size','Drift_effect_size'])['RT_effect_size'].mean()
Ac_es=df.groupby(['sample_size','Drift_effect_size'])['Acc_effect_size'].mean()
#Dr_es=df.groupby('sample_size')['Drift_effect_size'].mean()

#join all summary stat dfs together (since are all grouped dfs, already have samples size and Drift ES info)
summary_df=pd.concat([RT_es,Ac_es,prop_p_values_Drf,prop_p_values_RTs,prop_p_values_Acc],axis=1).reset_index()

print("saving summary.csv")     
summary_df.to_csv('summary.csv')