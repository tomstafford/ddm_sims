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
    import hddm # Import the HDDM Module
    data,params = hddm.generate.gen_rand_data({trial_name:params},size=trials,subjs=n_subjects,subj_noise={'v':intersubj_drift_var})
    '''
    The imported hddm allows for random data generation depending
    on the specified arguments (and parameters). Returns a data array.
    '''
    return data

'''
Main Loop
'''

def do_experiment(expt):
    ppts = 10 #TEMP FUDGE
    n_experiments = 50  # Number of simulated experiments  - make this arbitrary large for final run
    n_subjects = [10,20,30,100] # n_participants in each experiment
    stim_A = 0.2 # Stimulus A - Drift Rate = 0.2
    stim_B = 0.3 # Stimulus B - Drift Rate = 0.6
    stims = [stim_A,stim_B] # Drift Rate depends on the Stimulus specified.
    intersubj_drift_var=0.1 # std
    cohens_d=(stims[0]-stims[1])/intersubj_drift_var
    trial_name = 'ppt_test' # Specfies what each trial is running - e.g. altered number of participants
    trials = 20 # trial per participants
    n_experiments = 50  # Number of simulated experiments  - make this arbitrary large for final run
    params={'v':0.5, 'a':1.0, 't':0.1, 'sv':0.0, 'z':0.5, 'sz':0.0, 'st':0.0} # HDDM Parameters
    # HDDM Parameters:
        # v = Drift rate        # a = Boundary separation
        # t = Non-decision time # z = protent response bias
        # Inter-trial variability in v, z and t all set to 0 (No variability)
    n_samples=100 #for HDDM fitting, put this to 5000 for final run

    # dataframe for the experiments conducted for each sample size, and the significance value for that sample size.
    store_apdf=pd.DataFrame(columns=['experiment_number','sample_size','p_value_RTs','p_value_Acc','p_value_Drift'],index=range(n_experiments*len(n_subjects)))

    store_df=pd.DataFrame(columns=['mean_rtA','mean_rtB','prop_acc_A','prop_acc_B','driftA','driftB'],index=range(ppts))
    for i,drift in enumerate(stims):
        params={'v':drift, 'a':2, 't':0.1, 'sv':0, 'z':.5, 'sz':0, 'st':0} # Parameters specified again
        data=ppt_ddm_func(trial_name,params,trials,ppts,intersubj_drift_var)
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

    # t-test not appropriate for hierarchically generated data, but fix this later
    t,p = scipy.stats.ttest_ind(store_df['mean_rtA'],store_df['mean_rtB'])
    # Running a t-test for the mean reaction times of both stimulu (t,p)
    t2,p2 = scipy.stats.ttest_ind(store_df['prop_acc_A'],store_df['prop_acc_B'])
    # Running a t-test for the mean proportion of accurate responses for both stimuli (t2,p2)
    t3,p3 = scipy.stats.ttest_ind(store_df['driftA'],store_df['driftB'])
    # Running a t-test for the mean proportion of accurate responses for both stimuli (t2,p2)

    print([expt,ppts,p,p2,p3])
    return([expt,ppts,p,p2,p3])
