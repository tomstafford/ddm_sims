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


print("* * * * Figure 1: effect size translation * * * * )

#get observed effect sizes for RT and Acc for each declared drift effect size
effect_df=df.groupby('Drift_effect_size')['RT_effect_size','Acc_effect_size'].mean().reset_index()
#make all ES positive
effect_df=effect_df.apply(abs)

plt.clf()
plt.plot(effect_df['Drift_effect_size'],effect_df['RT_effect_size'],'.',ms=10,label='RT')
plt.plot(effect_df['Drift_effect_size'],effect_df['Acc_effect_size'],'.',ms=10,label='Accuracy')
plt.xlabel("Cohen's d of drift")
plt.ylabel("Cohen's d of RT or Accuracy")
plt.legend(loc=0)
plt.savefig('effectsizetranslation.png',bbox_inches='tight')







print("* * * * Figures 2-4: measure comparison for a fixed effect size, no SATO * * * * )


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



