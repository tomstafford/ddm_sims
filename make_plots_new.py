'''
make plots for project report
'''

import pandas as pd  
import socket
import os
import matplotlib.pylab as plt
import glob
from scipy.stats import norm #for Z scores

if 'tom' in socket.gethostname():
    os.chdir('/home/tom/Dropbox/university/toys/ddm_sims/')
else:
    print("assuming running in host directory")




def dprime_correct(val,correction):
    #add a small amount to any floor or ceiling proportions
    if val==0:
        return correction
    elif val==1:
        return 1-correction
    else:
        return val


df=pd.read_csv('summary.csv')

ES=2.0

dprime_correction=0.01 #the amount added to proportions of 0 so the maths works

FAs_=df[df['Drift_effect_size']==0][['sample_size','Drsig','Acsig','RTsig']].set_index('sample_size')

Hits=df[df['Drift_effect_size'].astype(int)==int(ES)][['sample_size','Drsig','Acsig','RTsig']].set_index('sample_size')


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



df.groupby('Drift_effect_size')['RT_effect_size','Acc_effect_size'].mean().plot()
