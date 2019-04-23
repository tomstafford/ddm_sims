'''
make plots for project report

'''

'''
--------------------> LIBRARIES <----------------------------
'''

import pandas as pd  
import socket
import os
import matplotlib.pylab as plt
import glob
from scipy.stats import norm #for Z scores

'''
--------------------> FUNCTIONS <----------------------------
'''


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
        
'''
--------------------> PARAMETERS <----------------------------
'''

#    os.chdir('/home/tom/t.stafford@sheffield.ac.uk/A_UNIVERSITY/toys/ddm_sims/write_up/figs')

acc_marker='o'
rts_marker='^'
dft_marker='x'

acc_color='#1f77b4'
rts_color='#ff7f0e'
dft_color='#2ca02c'

acc_linestyle='-.'
rts_linestyle='--'
dft_linestyle=':'

linewidth=3

dprime_correction=0.0001# 0.01 #the amount added to proportions of 0 so the maths works

#Effect size of interest
ES=2.0 #this defines the slice throught the 3d space we're going to take (sample size, effect size, power)


'''
--------------------> PLOTS <----------------------------
'''

print("* * * * Figure 3: effect size translation * * * * ")
folder='SATO-direct/SATO_t40_final/' #boundary =1, var =1
df=pd.read_csv('../../data/'+folder+'audit_first_expt_data.csv')
rts=df.groupby(['subj_idx','condition'])['rt','response'].mean().reset_index()['rt'].values
acc=df.groupby(['subj_idx','condition'])['rt','response'].mean().reset_index()['response'].values
plt.clf()
plt.plot(rts,acc,'.',ms=7,alpha=0.3)
plt.xlabel('Reaction Time')
plt.ylabel('Accuracy')
plt.ylim([-0.05 ,1.05])
#plt.annotate('boundary=2 (variance = 1)\n drift = 1 (variance = 0)',xy=(1.2,0.1),xycoords='data')
plt.savefig('SATO-direct_scatter.png',bbox_inches='tight')


print("* * * * Figure 4: effect size translation * * * * ")

print("nb for this figure it doesn't matter if you use EZ or HDDM data, since the fits are not used, only the raw (simulated) data")
df=pd.read_csv('../../data/ez_vbig/summary.csv')


#get observed effect sizes for RT and Acc for each declared drift effect size
RT_effect_size=df.groupby("Drift_effect_size").apply(wavg, "RT_effect_size", "sample_size")
Ac_effect_size=df.groupby("Drift_effect_size").apply(wavg, "Acc_effect_size", "sample_size")
#merge
effect_df=pd.merge(RT_effect_size.reset_index(), Ac_effect_size.reset_index(), how='inner', on=['Drift_effect_size'])
effect_df.columns=['Drift','RT_','Acc']
#make all ES positive
effect_df=effect_df.apply(abs)

effect_df=effect_df[effect_df['Drift']<4.1] #we only show part of the range

plt.clf()
plt.plot(effect_df['Drift'],effect_df['Acc'],ms=5,linestyle=acc_linestyle,marker=acc_marker,color=acc_color,label='Accuracy')
plt.plot(effect_df['Drift'],effect_df['RT_'],ms=5,linestyle=rts_linestyle,marker=rts_marker,color=rts_color,label='RT')
plt.xlabel("Cohen's d of (true) drift")
plt.ylabel("Cohen's d of (observed) RT/Accuracy")
pad=(effect_df['Drift'].max()-effect_df['Drift'].min())*0.1

plt.xlim([effect_df['Drift'].min()-pad,effect_df['Drift'].max()+pad])
plt.legend(loc=0)
plt.savefig('effectsizetranslation.png',bbox_inches='tight')





print("* * * * Figures 5, 6 , 7: measure comparison for a fixed effect size, no SATO * * * *" )

print("using EZ fits")

filenames=['../../data/ez_vbig/summary.csv','../../data/SATO_down_t40_ez/summary.csv']
outnames=['NOSATO_','SATO_']

subplots=True


for filename,outname in zip(filenames,outnames):

    df=pd.read_csv(filename)


    #False alarms is hit rate when there is no true difference
    FAs_=df[df['Drift_effect_size']==0][['sample_size','Drsig','RTsig','Acsig']].set_index('sample_size')

    #Hits is hit rate when there is a true difference (for the effet size specified)
    mask=(df['Drift_effect_size']>(ES-0.01)) & (df['Drift_effect_size']<(ES+0.01))
    Hits=df[mask][['sample_size','Drsig','RTsig','Acsig']].set_index('sample_size')

    #Apply dprime correction, in case any values are 0 or 1
    FAs_=FAs_.applymap(lambda x: dprime_correct(x,dprime_correction))
    Hits=Hits.applymap(lambda x: dprime_correct(x,dprime_correction))

    #Calculate dprime to combine hits and false alarms
    dprime=Hits[['Drsig','RTsig','Acsig']].applymap(norm.ppf)-FAs_[['Drsig','RTsig','Acsig']].apply(norm.ppf)


    
    if subplots: #thank you Jake https://jakevdp.github.io/PythonDataScienceHandbook/04.08-multiple-subplots.html
        plt.subplot(1,2,2)
    
    #plt.clf()
    plt.plot(FAs_.index,FAs_.Drsig,linestyle=dft_linestyle,lw=linewidth,color=dft_color,label='Drift')
    plt.plot(FAs_.index,FAs_.Acsig,linestyle=acc_linestyle,lw=linewidth,color=acc_color,label='Accuracy')
    plt.plot(FAs_.index,FAs_.RTsig,linestyle=rts_linestyle,lw=linewidth,color=rts_color,label='RT')
    plt.ylabel('False Alarm rate')
    plt.ylim([-0.05 ,1.05])
    plt.xlabel('Sample size, per group')
    plt.legend(loc=0)
    if not subplots:
        plt.savefig(outname+'FalseAlarms.png',bbox_inches='tight')

    if subplots:
        plt.subplot(1,2,1)

    #plt.clf()
    plt.plot(Hits.index,Hits.Drsig,linestyle=dft_linestyle,lw=linewidth,color=dft_color,label='Drift')
    plt.plot(Hits.index,Hits.Acsig,linestyle=acc_linestyle,lw=linewidth,color=acc_color,label='Accuracy')
    plt.plot(Hits.index,Hits.RTsig,linestyle=rts_linestyle,lw=linewidth,color=rts_color,label='RT')
    plt.ylabel('Hit rate')
    plt.ylim([-0.05 ,1.05])
    plt.xlabel('Sample size, per group')
    if not subplots:
        plt.legend(loc=0)    
        plt.savefig(outname+'HitRate.png',bbox_inches='tight')
    
    if subplots:
        plt.subplots_adjust(hspace=0.4, wspace=0.4)
        fig = plt.gcf()
        fig.set_size_inches(9, 5)
        plt.savefig(outname+'hit_and_FA.png',bbox_inches='tight')
        
        


    plt.clf()
    plt.plot(dprime.index,dprime.Drsig,linestyle=dft_linestyle,lw=linewidth,color=dft_color,label='Drift')
    plt.plot(dprime.index,dprime.Acsig,linestyle=acc_linestyle,lw=linewidth,color=acc_color,label='Accuracy')
    plt.plot(dprime.index,dprime.RTsig,linestyle=rts_linestyle,lw=linewidth,color=rts_color,label='RT')
    plt.ylabel('d\'')
    plt.xlabel('Sample size, per group')
    plt.legend(loc=0)
    plt.savefig(outname+'dprime.png',bbox_inches='tight')


