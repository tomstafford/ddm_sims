'''
make plots for project report
'''

import pandas as pd  
import socket
import os
import matplotlib.pylab as plt
import glob
from scipy.stats import norm #for Z scores

#if 'tom' in socket.gethostname():
#    os.chdir('/home/tom/Dropbox/university/toys/ddm_sims/')
#else:
#    print("assuming running in host directory")




def dprime_correct(val,correction):
    #add a small amount to any floor or ceiling proportions
    if val==0:
        return correction
    elif val==1:
        return 1-correction
    else:
        return val



def wavg(group, avg_name, weight_name):
    """
    weigthed mean function for applying to grouped df data  
    cribbing from http://pbpython.com/weighted-average.html which in turn cribs from
    http://stackoverflow.com/questions/10951341/pandas-dataframe-aggregate-function-using-multiple-columns
    In rare instance, we may not have weights, so just return the mean. 
    """
    d = group[avg_name]
    w = group[weight_name]
    try:
        return (d * w).sum() / w.sum()
    except ZeroDivisionError:
        return d.mean()
        


df=pd.read_csv('summary.csv')


print("* * * * Figure 1: effect size translation * * * * ")

#get observed effect sizes for RT and Acc for each declared drift effect size
RT_effect_size=df.groupby("Drift_effect_size").apply(wavg, "RT_effect_size", "sample_size")
Ac_effect_size=df.groupby("Drift_effect_size").apply(wavg, "Acc_effect_size", "sample_size")
#merge
effect_df=pd.merge(RT_effect_size.reset_index(), Ac_effect_size.reset_index(), how='inner', on=['Drift_effect_size'])
effect_df.columns=['Drift','RT','Acc']
#make all ES positive
effect_df=effect_df.apply(abs)

plt.clf()
plt.plot(effect_df['Drift'],effect_df['Acc'],'.',ms=10,label='Accuracy')
plt.plot(effect_df['Drift'],effect_df['RT'],'.',ms=10,label='RT')
plt.xlabel("Cohen's d of drift")
plt.ylabel("Cohen's d of RT or Accuracy")
pad=(effect_df['Drift'].max()-effect_df['Drift'].min())*0.1

plt.xlim([effect_df['Drift'].min()-pad,effect_df['Drift'].max()+pad])
plt.legend(loc=0)
plt.savefig('effectsizetranslation.png',bbox_inches='tight')







print("* * * * Figures 2-4: measure comparison for a fixed effect size, no SATO * * * *" )


ES=3.0

dprime_correction=0.001# 0.01 #the amount added to proportions of 0 so the maths works

FAs_=df[df['Drift_effect_size']==0][['sample_size','Drsig','RTsig','Acsig']].set_index('sample_size')

Hits=df[df['Drift_effect_size'].astype(int)==int(ES)][['sample_size','Drsig','RTsig','Acsig']].set_index('sample_size')


FAs_=FAs_.applymap(lambda x: dprime_correct(x,dprime_correction))
Hits=Hits.applymap(lambda x: dprime_correct(x,dprime_correction))

dprime=Hits[['Drsig','RTsig','Acsig']].applymap(norm.ppf)-FAs_[['Drsig','RTsig','Acsig']].apply(norm.ppf)


FAs_.sort_index().plot()
plt.ylabel('False Alarm rate')
plt.ylim([-0.05 ,1.05])
plt.savefig('FalseAlarms.png',bbox_inches='tight')



Hits.sort_index().plot()
plt.ylabel('Hit rate')
plt.ylim([-0.5 ,1.05])
plt.savefig('HitRate.png',bbox_inches='tight')


dprime.sort_index().plot()
plt.ylabel('d prime')
plt.savefig('dprime.png',bbox_inches='tight')



