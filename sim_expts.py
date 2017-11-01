'''
Use HDDM http://ski.clps.brown.edu/hddm_docs/

Aim:
1. simulate experiments with different number of participants, and different participant parameter regiemes
2. fit the simulated data with the HDDM and recover the parameters
3. Store simulated expt data and recovered parameters
'''

'''
Import Libraries'
'''

import pandas as pd   # Pandas = Data manipulation/analysis (e.g. Numerical tables/ Specific variable arrays)
import scipy          # Scipy  = Signal procesisng, optimization, statistics and more
import time           # Time   = Time access and conversions
import numpy as np    # Numpy
from patsy import dmatrix
import hddm

'''
Define Function
'''

def ppt_ddm_func(trial_name,params,trials,n_subjects,intersubj_drift_var):
    '''
    This function simulates data using the DDM model (and the HDDM toolbox)
    with the specified parameters
    '''
    data,params = hddm.generate.gen_rand_data({trial_name:params},size=trials,subjs=n_subjects,subj_noise={'v':intersubj_drift_var})
    '''
    The imported hddm allows for random data generation depending
    on the specified arguments (and parameters). Returns a data array.
    '''
    return data

'''
Main Loop
'''

def do_experiment(ppts,n_experiments,stim_A,stim_B,intersubj_drift_var,n_samples,trial_name,trials,start_seed,expt):

    # Every experiment has its own random seed
    random_seed = start_seed + expt
    np.random.seed(random_seed)

    stims = [stim_A,stim_B] # Drift Rate depends on the Stimulus specified.

    cohens_d=(stims[0]-stims[1])/intersubj_drift_var
    params={'v':0.5, 'a':1.0, 't':0.1, 'sv':0.0, 'z':0.5, 'sz':0.0, 'st':0.0} # HDDM Parameters
    # HDDM Parameters:
        # v = Drift rate        # a = Boundary separation
        # t = Non-decision time # z = protent response bias
        # Inter-trial variability in v, z and t all set to 0 (No variability)

    # dataframe for the experiments conducted for each sample size, and the significance value for that sample size.
    # store_apdf=pd.DataFrame(columns=['experiment_number','sample_size','p_value_RTs','p_value_Acc','p_value_Drift'],index=range(n_experiments*len(n_subjects)))

    store_df=pd.DataFrame(columns=['mean_rtA','mean_rtB','prop_acc_A','prop_acc_B','driftA','driftB'],index=range(ppts))
    for i,drift in enumerate(stims):
        params={'v':drift, 'a':2, 't':0.1, 'sv':0, 'z':.5, 'sz':0, 'st':0} # Parameters specified again
        data = ppt_ddm_func(trial_name,params,trials,ppts,intersubj_drift_var)
        if i==0:
            RT_col='mean_rtA'
            ac_col='prop_acc_A'
        else:
            RT_col='mean_rtB'
            ac_col='prop_acc_B'
        store_df[RT_col]=data.groupby('subj_idx')['rt'].mean()
        # 'mean_rtA' + 'mean_rtB' = Mean RTs of participants for each trial.
        store_df[ac_col]=data.groupby('subj_idx')['response'].mean()
        # 'prop_acc_A' + 'prop_acc_B' = Accuracy via proportion of correct responses.

        if i==1:
            data1=data
        else:
            data2=data

    data1['group'] = pd.Series(np.ones((len(data1))), index=data1.index)
    data2['group'] = pd.Series(np.ones((len(data1)))*2, index=data1.index)
    #Now we merge the data for stimulus A and B
    mydata = data1.append(data2, ignore_index=True)
    # fit the data
    # - define model
    m = hddm.HDDM(mydata, depends_on={'v': 'group'})
    # - find a good starting point which helps with the convergence.
    m.find_starting_values()
    # - fit
    m.sample(n_samples, burn=int(n_samples*0.05))
    stats = m.gen_stats()
    # - store
    store_df['driftA']=stats.loc[stats.index.str.contains('v_subj\(1.0\)'),'mean'].values
    store_df['driftB']=stats.loc[stats.index.str.contains('v_subj\(2.0\)'),'mean'].values

    if expt == 0:
        store_df.to_csv('audit_mean_data.csv')  # Save generated data for auditing

    # t-test not appropriate for hierarchically generated data, but fix this later
    t,p = scipy.stats.ttest_ind(store_df['mean_rtA'],store_df['mean_rtB'])
    # Running a t-test for the mean reaction times of both stimulu (t,p)
    t2,p2 = scipy.stats.ttest_ind(store_df['prop_acc_A'],store_df['prop_acc_B'])
    # Running a t-test for the mean proportion of accurate responses for both stimuli (t2,p2)
    t3,p3 = scipy.stats.ttest_ind(store_df['driftA'],store_df['driftB'])
    # Running a t-test for the mean proportion of accurate responses for both stimuli (t2,p2)
    print('\n')
    print([expt,ppts,p,p2,p3])
    return(pd.DataFrame([[expt,ppts,p,p2,p3,random_seed]],index = [expt],columns=['experiment_number','sample_size','p_value_RTs','p_value_Acc','p_value_Drift','seed']))
