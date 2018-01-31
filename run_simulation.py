from multiprocessing import Pool
from sim_expts import *
from functools import partial
pool = Pool(32) #how many processors to use, 4 in the VM, 32 on the RSE Sharc cluster
from sendemail import send_mail #for sending email

'''
Define Parameters
'''

'''experiment parameters'''
trial_names = ['groupA','groupB'] # Specfies what each trial is running - e.g. altered number of participants
n_subjects = [20,40] # n_participants in each experiment

n_experiments = 10  # Number of simulated experiments  - make this arbitrary large for final run
n_samples = 200  #for HDDM fitting, put this to 5000 for final run

trials = 40 # trial per participants

'''HDDM parameters'''
    # HDDM Parameters:
        # v = Drift rate        # a = Boundary separation
        # t = Non-decision time # z = protent response bias
        # Inter-trial variability in v, z and t all set to 0 (No variability)
''' ------------------- usually only these change between runs ---- '''
drifts=[1.0,1.1] # different drift for each group. Drift of 1->0.85% accuracy. ASSUME GROUP B BETTER IF AT ALL
a_param=[2, 2] #boundary 
suffix='D1B0' 
''' ------------------- ------------------------------------------ '''
z_param=0.5 #bias 0.5 is no bias
t_param=0.3 #non-decision time
sv_param=0 #trial by trial drift variability
sz_param=0
st_param=0
paramsA={'v':drifts[0], 'a':a_param[0], 't':t_param, 'z':z_param, 'sv':sv_param, 'sz':sz_param, 'st':st_param} # Parameters specified again
paramsB={'v':drifts[1], 'a':a_param[1], 't':t_param, 'z':z_param, 'sv':sv_param, 'sz':sz_param, 'st':st_param} # Parameters specified again
intersubj_vars=[0.05,0.05] # [intersubj_drift_var,intersubj_boundary_var]

'''
Send of single experiments to parallel processing, getting back the p values associated with the mean participant data
'''

start = time.time()
store_apdf = pd.DataFrame(columns=['experiment_number','sample_size','groupA_RT_mean','groupB_RT_mean','groupA_Acc_mean','groupB_Acc_mean','RT_effect_size','Acc_effect_size','Drift_effect_size','p_value_RTs','p_value_Acc','p_value_Drift','seed'])
for block_num,ppts in enumerate(n_subjects): # different sample sizes for experiments
    start_seed = block_num * n_experiments
    expt_func = partial(do_experiment,ppts,paramsA,paramsB,intersubj_vars,n_samples,trial_names,trials,start_seed)
    result = pool.map(expt_func, range(n_experiments))
    result = pd.concat(result)
    store_apdf = pd.concat([store_apdf,result])


store_apdf.to_csv('store_'+suffix+'.csv') # Saving the data array to a CSV.

pool.close()

end = time.time() #record finish time

endmsg="TOOK " + str(round(end - start,3)) + " SECONDS \n\n" 
print(endmsg)

try:
    send_mail('t.stafford@sheffield.ac.uk','tom@idiolect.org.uk','sim_expts.py' + ' :'+suffix+': '+'complete',endmsg,None,'smtp.gmail.com')
except:
    print("Couldn't send mail notification")