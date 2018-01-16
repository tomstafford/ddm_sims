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

'''
Main Loop
'''

def do_experiment(ppts,paramsA,paramsB,intersubj_vars,n_samples,trial_names,trials,start_seed,expt):

    # Every experiment has its own random seed
    random_seed = start_seed + expt
    np.random.seed(random_seed)

    #generate random data according to the passed DDM parameters
    data = ppt_ddm_func(trial_names[0],trial_names[1],paramsA,paramsB,trials,ppts,intersubj_vars[0],intersubj_vars[1])

    # fit the data using the HDDM
    m = hddm.HDDM(data, depends_on={'v': 'condition', 'a': 'condition'}) # - define model
    m.find_starting_values() # - find a good starting point which helps with the convergence.
    m.sample(n_samples, burn=int(n_samples*0.05)+20) # - fit
    stats = m.gen_stats() #output
    
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

    #frequentist testing is not appropriate, so we compare posteriors directly
    #following http://ski.clps.brown.edu/hddm_docs/howto.html        
    v_A, v_B= m.nodes_db.node[['v(groupA)', 'v(groupB)']]        
    v_p=(v_A.trace() > v_B.trace()).mean()

#    ''' auditing - save interim data'''
#    if expt == 0:
#        data.to_csv('audit_first_expt_of'+str(n_experiments)+'.csv')  
#        stats.to_csv('audit_stats_expt_of'+str(n_experiments)+'.csv')
#        data.to_csv('audit_single_expt_data.csv')  # store result first time we do this, for auditing
#        
#    if expt == 1:
#        data.to_csv('exptis1.csv')

    print("\n - done" + str(ppts))

    return(pd.DataFrame([[expt,ppts,RTp,Acp,v_p,random_seed]],index = [expt],columns=['experiment_number','sample_size','p_value_RTs','p_value_Acc','p_value_Drift','seed']))
