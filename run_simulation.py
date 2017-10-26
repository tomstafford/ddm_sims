from multiprocessing import Pool
from sim_expts import *
from functools import partial
pool = Pool(1)

'''
Define Parameters
'''

n_experiments = 50  # Number of simulated experiments  - make this arbitrary large for final run
n_subjects = [10,20,30,100] # n_participants in each experiment
stim_A = 0.2 # Stimulus A - Drift Rate = 0.2
stim_B = 0.3 # Stimulus B - Drift Rate = 0.6
intersubj_drift_var=0.1 # std
n_samples=100 #for HDDM fitting, put this to 5000 for final run
trial_name = 'ppt_test' # Specfies what each trial is running - e.g. altered number of participants
trials = 20 # trial per participants

start = time.time()

for ppts in n_subjects: # different sample sizes for experiments

    # Stored dataframe with experiment number and p values for the given experiment
    store_pdf=pd.DataFrame(columns=['p_value_RTs','p_value_Acc','p_value_Drift'],index=range(n_experiments))

    # For each experiment ('expt') in the specified simulated experiment range (n_experiments)
    #store_df=pd.DataFrame(columns=['mean_rtA','mean_rtB','prop_acc_A','prop_acc_B','driftA','driftB'],index=range(ppts))
    # 'store_df' = prop_acc_A/prop_acc_B represents proportion of accurate (correct) responses
    #print("doing expt " + str(expt+1) + " of " +str(n_experiments) + " for experiments with " + str(ppts) + " ppts") # Print "doing expt n of N"
    #store_df=pd.DataFrame(columns=['mean_rtA','mean_rtB','prop_acc_A','prop_acc_B','driftA','driftB'],index=range(ppts))
    expt_func = partial(do_experiment,ppts,n_experiments,stim_A,stim_B,intersubj_drift_var,n_samples,trial_name,trials)
    result = pool.map(expt_func, range(n_experiments))

pool.close()

end = time.time() #record finish time

print("TOOK " + str(round(end - start,3)) + " SECONDS \n\n") #TOOK 5046.116 SECONDS = 84 minnutes
