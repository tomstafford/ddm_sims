# -*- coding: utf-8 -*-
"""
Fitting data using the EZ-DDM
"""

import pandas as pd   # Pandas = Data manipulation/analysis (e.g. Numerical tables/ Specific variable arrays)
import scipy          # Scipy  = Signal procesisng, optimization, statistics and more
import time           # Time   = Time access and conversions
import numpy as np    # Numpy
from patsy import dmatrix
import hddm


def ppt_ddm_func(trial_nameA,trial_nameB,paramsA,paramsB,trials,n_subjects,intersubj_drift_var,intersubj_boundary_var):
    '''
    This function simulates data using the DDM model (and the HDDM toolbox)
    with the specified parameters
    '''
    data,params = hddm.generate.gen_rand_data({trial_nameA:paramsA,trial_nameB:paramsB},size=int(trials),subjs=int(n_subjects),subj_noise={'v':intersubj_drift_var,'a':intersubj_boundary_var})
    '''
    The imported hddm allows for random data generation depending
    on the specified arguments (and parameters). Returns a data array.
    '''
    return data
    
    

def ezdiff(rt, correct, s=1.):

    """ 
    generate data as normal, but fit each subj with EZDMM

    This is based on code from https://github.com/CoAxLab/radd/blob/master/radd/tools/analyze.py
    
    And Wagenmakers, E.-J., Van Der Maas, H. L. J., & Grasman, R. P. P. P. (2007). An EZ-diffusion model for response time and accuracy. Psychonomic Bulletin & Review, 14(1), 3–22. doi:10.3758/bf03194023 http://sci-hub.tw/http://link.springer.com/article/10.3758/BF03194023
    
    Input parameters
    
    MRT = mean reaction time
    VRT = variance of reaction time
    Pc = proportion 'correct'
    S = "Across-trials range in the nondecision component of 
            processing"   
    
    Output params
    v = drift
    a = boundary seperation
    tr = non-decision time
    """

    logit = lambda p:np.log(p/(1-p))
    pc = np.mean(correct)

    # subtract or add 1/2 an error to prevent division by zero
    if pc==1.0:
        pc=1 - 1/(2*len(correct))
    if pc==0.5:
        pc=0.5 + 1/(2*len(correct))
    MRT = np.mean(rt[correct==1])
    VRT = np.var(rt[correct==1])

    # Wagenmakers (2007) equation 7, in two parts
    r = (logit(pc)*(((pc**2) * logit(pc)) - pc*logit(pc) + pc - 0.5))/VRT
    v = np.sign(pc-0.5)*s*(r)**0.25
    # Wagenmakers (2007) equation 5
    a = (s**2 * logit(pc))/v
    # noted in the text
    y = (-1*v*a)/(s**2)
    # Wagenmakers (2007) equation 9
    MDT = (a/(2*v))*((1-np.exp(y))/(1+np.exp(y)))
    tr = MRT-MDT

    return([a, v, tr])


def do_experimentEZ(ppts,paramsA,paramsB,intersubj_vars,n_samples,trial_names,trials,start_seed,expt):
    
    # Every experiment has its own random seed
    random_seed = start_seed + expt
    np.random.seed(random_seed)

    #generate random data according to the passed DDM parameters
    data = ppt_ddm_func(trial_names[0],trial_names[1],paramsA,paramsB,trials,ppts,intersubj_vars[0],intersubj_vars[1])

    #collect behavioural means
    #- average of correct RTs for each individual
    gp_meansRTs=data[data['response']==1].groupby(['subj_idx','condition'])['rt'].mean().reset_index()
    #- proportion of correct responses for each individual
    gp_meansAcc=data.groupby(['subj_idx','condition'])['response'].mean().reset_index()
    
    #seperate out for each group, A and B
    RTsA=gp_meansRTs[gp_meansRTs['condition']=='groupA']['rt'].values
    RTsB=gp_meansRTs[gp_meansRTs['condition']=='groupB']['rt'].values
    AccA=gp_meansAcc[gp_meansAcc['condition']=='groupA']['response'].values
    AccB=gp_meansAcc[gp_meansAcc['condition']=='groupB']['response'].values

    #fitting the EZ
    model=pd.DataFrame(index=range((data.subj_idx.max()+1)*2),columns=['condition','subj_inx','a','v','tr'])

    j=0
    for condition in ['groupA','groupB']:
        for i in range(len(RTsA)):
            rts=data[(data['subj_idx']==i) & (data['condition']==condition)]['rt']
            rsp=data[(data['subj_idx']==i) & (data['condition']==condition)]['response']
            model.iloc[j]=np.append(np.append(condition,i),ezdiff(rts,rsp))
            j+=1


    
    #now do t-test on RT, Accuracy for group differences
    
    RTt,RTp = scipy.stats.ttest_ind(RTsA,RTsB)     #if t is -ve then A<B, ie A quicker
    Act,Acp = scipy.stats.ttest_ind(AccA,AccB)    #if t is -ve then A<B, ie A is less accurate
    
    #We transform p values so they indicate correctness of inference (-ve p values reflect incorrect inference)
    if RTt<0: #if A is quicker any significant difference is a false alarm (assuming drift for B is only ever = or > than for A)
        RTp = RTp*(-1)
    else:
        RTp = RTp
        
    if Act<0            :
        Acp = Acp
    else:
        Acp = Acp*(-1) # if A is more accurate, transform p value (because will be false alarm, as above)

    # we replace this bit
    '''
    #frequentist testing is not appropriate, so we compare posteriors directly
    #following http://ski.clps.brown.edu/hddm_docs/howto.html        
    v_A, v_B= m.nodes_db.node[['v(groupA)', 'v(groupB)']]        
    v_p=(v_A.trace() > v_B.trace()).mean()
    '''
    # with this
    a_v=model[model['condition']=='groupA']['v'].values.astype(float)
    b_v=model[model['condition']=='groupB']['v'].values.astype(float)
    v_t,v_p = scipy.stats.ttest_ind(a_v,b_v)     #if t is -ve then A<B, ie A quicker
    
    
    if v_t<0            :
        v_p = v_p
    else:
        v_p = v_p*(-1) # if A is more accurate, transform p value (because will be false alarm, as above)


    ''' auditing - save interim data'''
    if expt == 0:
        model.to_csv('audit_first_expt_stats.csv')
        data.to_csv('audit_first_expt_data.csv')  # store result first time we do this, for auditing


    print("\n - done" + str(ppts))

    def cohen_d(x,y):    
        # from https://stackoverflow.com/questions/21532471/how-to-calculate-cohens-d-in-python
        from numpy import std, mean, sqrt
        nx = len(x)
        ny = len(y)
        dof = nx + ny - 2
        return (mean(x) - mean(y)) / sqrt(((nx-1)*std(x, ddof=1) ** 2 + (ny-1)*std(y, ddof=1) ** 2) / dof)    
    
    
    cohen_d_drift=(paramsB['v']-paramsA['v'])/intersubj_vars[0]

    return(pd.DataFrame([[expt,ppts,RTsA.mean(),RTsB.mean(),AccA.mean(),AccB.mean(),cohen_d(RTsA,RTsB),cohen_d(AccA,AccB),cohen_d_drift,RTp,Acp,v_p,random_seed]],index = [expt],columns=['experiment_number','sample_size','groupA_RT_mean','groupB_RT_mean','groupA_Acc_mean','groupB_Acc_mean','RT_effect_size','Acc_effect_size','Drift_effect_size','p_value_RTs','p_value_Acc','p_value_Drift','seed']))




'''
#This was for trial run of fitting

n_subjects=n_subjects[0]
intersubj_boundary_var=intersubj_vars[1]   
intersubj_drift_var=intersubj_vars[0]     
trial_nameA=trial_names[0] 
trial_nameB=trial_names[1]
paramsA['v']=drift_a[1]       
paramsB['v']=drift_b[1] 

data,params = hddm.generate.gen_rand_data({trial_nameA:paramsA,trial_nameB:paramsB},size=int(trials),subjs=int(n_subjects),subj_noise={'v':intersubj_drift_var,'a':intersubj_boundary_var})


for subj_inx in range(data['subj_idx'].max()):

    data[(data['subj_idx']==0) & (data['condition']=='groupA')]


    rt=data[(data['subj_idx']==0) & (data['condition']=='groupA')]['rt']
    correct=data[(data['subj_idx']==0) & (data['condition']=='groupA')]['response']
    
    a,v,tr=ezdiff(rt,correct)
    
    
   
'''