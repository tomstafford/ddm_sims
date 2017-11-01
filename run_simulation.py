from multiprocessing import Pool
from sim_expts import *
from functools import partial
pool = Pool(8)

'''
Define Parameters
'''

n_experiments = 5  # Number of simulated experiments  - make this arbitrary large for final run
n_subjects = [10,20,30,100] # n_participants in each experiment
stim_A = 0.2 # Stimulus A - Drift Rate = 0.2
stim_B = 0.3 # Stimulus B - Drift Rate = 0.6
intersubj_drift_var=0.1 # std
n_samples = 100 #for HDDM fitting, put this to 5000 for final run
trial_name = 'ppt_test' # Specfies what each trial is running - e.g. altered number of participants
trials = 20 # trial per participants



start = time.time()
store_apdf = pd.DataFrame(columns=['experiment_number','sample_size','p_value_RTs','p_value_Acc','p_value_Drift','seed'])
for block_num,ppts in enumerate(n_subjects): # different sample sizes for experiments
    start_seed = block_num * n_experiments
    expt_func = partial(do_experiment,ppts,n_experiments,stim_A,stim_B,intersubj_drift_var,n_samples,trial_name,trials,start_seed)
    result = pool.map(expt_func, range(n_experiments))
    result = pd.concat(result)
    store_apdf = pd.concat([store_apdf,result])


store_apdf.to_csv('samples_v_p_values.csv') # Saving the data array to a CSV.

pool.close()

end = time.time() #record finish time

print("TOOK " + str(round(end - start,3)) + " SECONDS \n\n") #TOOK 5046.116 SECONDS = 84 minnutes
