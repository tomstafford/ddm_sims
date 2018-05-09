# -*- coding: utf-8 -*-
"""
Make plots for Psychonomics talk, Amsterdam, 2018/05/10
"""

import pandas as pd  #dataframes
import numpy as np #number functions
import socket #machine functions
import os #file and folder functions
import matplotlib.pylab as plt #plotting
from scipy.stats import norm #for Z scores
import seaborn as sns #plotting


print("set working directory")
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
        
    
print("set parameters")
dprime_correction=0.001# the amount added to proportions of 0 so the maths works



print("* * * * effect size translation * * * * ")

folder='NOSATO_t40_effectsize/'    
df=pd.read_csv(os.path.join('data',folder,'summary.csv'))

plt.clf()
plt.plot(df['Drift_effect_size'],df['Acc_effect_size'].abs(),'-^',color='red',ms=6,lw=2,label='Accuracy')
plt.plot(df['Drift_effect_size'],df['RT_effect_size'],'-o',color='blue',ms=6,lw=2,label='RT')
plt.xlabel("Cohen's d of drift")
plt.ylabel("Cohen's d of RT or Accuracy")
pad=(df['Drift_effect_size'].max()-df['Drift_effect_size'].min())*0.1

plt.xlim([df['Drift_effect_size'].min()-pad,df['Drift_effect_size'].max()+pad])
plt.legend(loc=0)

plt.savefig('psychonomics/effectsizetranslation_t40.png',bbox_inches='tight')



folder='NOSATO_t400_effectsize/'    
sf=pd.read_csv(os.path.join('data',folder,'summary.csv'))

plt.clf()
plt.plot(sf['Drift_effect_size'],sf['Acc_effect_size'].abs(),'-^',color='firebrick',ms=6,lw=2,label='Accuracy')
plt.plot(sf['Drift_effect_size'],sf['RT_effect_size'],'-o',color='darkblue',ms=6,lw=2,label='RT')
plt.xlabel("Cohen's d of drift")
plt.ylabel("Cohen's d of RT or Accuracy")
pad=(sf['Drift_effect_size'].max()-sf['Drift_effect_size'].min())*0.1

plt.xlim([sf['Drift_effect_size'].min()-pad,sf['Drift_effect_size'].max()+pad])
plt.legend(loc=0)

plt.savefig('psychonomics/effectsizetranslation_t400.png',bbox_inches='tight')


plt.clf()
plt.plot(sf['Drift_effect_size'],sf['Acc_effect_size'].abs(),'-^',color='firebrick',ms=6,lw=2,label='Accuracy, trials = 400')
plt.plot(sf['Drift_effect_size'],sf['RT_effect_size'],'-o',color='darkblue',ms=6,lw=2,label='RT, trials = 400')
plt.plot(df['Drift_effect_size'],df['Acc_effect_size'].abs(),'-^',color='red',ms=6,lw=2,label='Accuracy, trials = 40')
plt.plot(df['Drift_effect_size'],df['RT_effect_size'],'-o',color='blue',ms=6,lw=2,label='RT, trials = 40')
plt.xlabel("Cohen's d of drift")
plt.ylabel("Cohen's d of RT or Accuracy")
pad=(df['Drift_effect_size'].max()-df['Drift_effect_size'].min())*0.1

plt.xlim([df['Drift_effect_size'].min()-pad,df['Drift_effect_size'].max()+pad])
plt.legend(loc=0)

plt.savefig('psychonomics/effectsizetranslation_both.png',bbox_inches='tight')


print("* * * * WITH AND WITHOUT SATO  * * * * ")

folders=['NOSATO_t40/','NOSATO_t40_large/','SATO_t40_down/','SATO_t40_up/']    

for folder in folders:
    df=pd.read_csv(os.path.join('data',folder,'summary.csv'))
    
    Hits=df[~(df['Drift_effect_size']==0)][['sample_size','Drsig','RTsig','Acsig']].set_index('sample_size')
    FAs_=df[df['Drift_effect_size']==0][['sample_size','Drsig','RTsig','Acsig']].set_index('sample_size')
    
    Hits=Hits.applymap(lambda x: dprime_correct(x,dprime_correction))
    FAs_=FAs_.applymap(lambda x: dprime_correct(x,dprime_correction))
    dprime=Hits[['Drsig','RTsig','Acsig']].applymap(norm.ppf)-FAs_[['Drsig','RTsig','Acsig']].apply(norm.ppf)
    
    plt.clf()
    plt.plot(Hits['Drsig'],'-s',color='black',ms=6,lw=2,label='Drift')
    plt.plot(Hits['Acsig'],'-^',color='red',ms=6,lw=2,label='Accuracy')
    plt.plot(Hits['RTsig'],'-o',color='blue',ms=6,lw=2,label='Correct RTs')
    #plt.plot([0,160],[0.8,0.8],lw=1,color='gray')
    plt.ylabel('Hit rate')
    plt.xlabel('Sample size, per group')
    plt.ylim([-0.05 ,1.05])
    plt.xlim([0,160])
    plt.legend(loc=4)
    plt.savefig('psychonomics/'+folder[:-1]+'_HitRate.png',bbox_inches='tight')
    
    
    plt.clf()
    plt.plot(FAs_['Drsig'],'-s',color='black',ms=6,lw=2,label='Drift')
    plt.plot(FAs_['Acsig'],'-^',color='red',ms=6,lw=2,label='Accuracy')
    plt.plot(FAs_['RTsig'],'-o',color='blue',ms=6,lw=2,label='Correct RTs')
    #plt.plot([0,160],[0.8,0.8],lw=1,color='gray')
    plt.ylabel('False Alarm rate')
    plt.xlabel('Sample size, per group')
    plt.ylim([-0.05 ,1.05])
    plt.xlim([0,160])
    plt.legend(loc=0)
    plt.savefig('psychonomics/'+folder[:-1]+'_FalseAlarms.png',bbox_inches='tight')
    
    
    plt.clf()
    plt.plot(dprime['Drsig'],'-s',color='black',ms=6,lw=2,label='Drift')
    plt.plot(dprime['Acsig'],'-^',color='red',ms=6,lw=2,label='Accuracy')
    plt.plot(dprime['RTsig'],'-o',color='blue',ms=6,lw=2,label='Correct RTs')
    #plt.plot([0,160],[0.8,0.8],lw=1,color='gray')
    plt.ylabel('d\'')
    plt.xlabel('Sample size, per group')
    plt.ylim([-0.05 ,5])
    plt.xlim([0,160])
    plt.legend(loc=4)
    plt.savefig('psychonomics/'+folder[:-1]+'_dprime.png',bbox_inches='tight')



print("* * * * DIRECTLY LOOKING AT VARIABILITY IN BOUNDARY (SATOs) * * * * ")

folder='SATO-direct/SATO_highvar2a/' #Boundary=2, var=0.5 -> linear, but heteroscedastic?
folder='SATO-direct/SATO_highvar3/' #Boundary=3, var=0.5 -> linear, but heteroscedastic?
folder='SATO-direct/SATO_highvar4d/' #Boundary=4, var=0.15 -> not variation in accuracy, all RTs very high?
folder='SATO-direct/SATO_highvar4e/' #Boundary=4, var=0.5 -> not variation in accuracy, all RTs very high?
folder='SATO-direct/SATO_highvar/' #Boundary=2, var=1 -> not variation in accuracy, all RTs very high? Two regeimes?
folder='SATO-direct/SATO_highvar1v0p25/' #boundary =1, var =0.5


folder='SATO-direct/SATO_highvar2v1/' #boundary =1, var =1
df=pd.read_csv('data/'+folder+'audit_first_expt_data.csv')
rts=df.groupby(['subj_idx','condition'])['rt','response'].mean().reset_index()['rt'].values
acc=df.groupby(['subj_idx','condition'])['rt','response'].mean().reset_index()['response'].values
plt.clf()
plt.plot(rts,acc,'.')
plt.xlabel('Reaction Time')
plt.ylabel('Accuracy')
plt.ylim([-0.05 ,1.05])
plt.annotate('boundary=2, variance = 1',xy=(1.5,0.1),xycoords='data')
plt.savefig('psychonomics/SATO-direct_scatter.png',bbox_inches='tight')
sns.jointplot(rts,acc,kind="kde") #add labels, move legend etc


plt.savefig('psychonomics/SATO-direct_kde.png',bbox_inches='tight')

folder='SATO-direct/SATO_highvar2a/' #boundary =1, var =1
df=pd.read_csv('data/'+folder+'audit_first_expt_data.csv')
rts=df.groupby(['subj_idx','condition'])['rt','response'].mean().reset_index()['rt'].values
acc=df.groupby(['subj_idx','condition'])['rt','response'].mean().reset_index()['response'].values
plt.clf()
plt.plot(rts,acc,'.')
plt.xlabel('Reaction Time')
plt.ylabel('Accuracy')
plt.ylim([-0.05 ,1.05])
plt.annotate('boundary=4, variance = 0.5',xy=(1.5,0.1),xycoords='data')
