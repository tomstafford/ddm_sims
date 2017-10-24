from multiprocessing import Pool
from sim_expts import *
pool = Pool(8)

'''
Define Parameters
'''

n_experiments = 20  # Number of simulated experiments  - make this arbitrary large for final run
n_subjects = [10] # n_participants in each experiment

start = time.time()

for ppts in n_subjects: # different sample sizes for experiments

    # Stored dataframe with experiment number and p values for the given experiment
    store_pdf=pd.DataFrame(columns=['p_value_RTs','p_value_Acc','p_value_Drift'],index=range(n_experiments))

    for expt in range(n_experiments):
        pass
        # For each experiment ('expt') in the specified simulated experiment range (n_experiments)
        #store_df=pd.DataFrame(columns=['mean_rtA','mean_rtB','prop_acc_A','prop_acc_B','driftA','driftB'],index=range(ppts))
        # 'store_df' = prop_acc_A/prop_acc_B represents proportion of accurate (correct) responses
        #print("doing expt " + str(expt+1) + " of " +str(n_experiments) + " for experiments with " + str(ppts) + " ppts") # Print "doing expt n of N"
    #store_df=pd.DataFrame(columns=['mean_rtA','mean_rtB','prop_acc_A','prop_acc_B','driftA','driftB'],index=range(ppts))
    result = pool.map(do_experiment, range(n_experiments))
# y_serial == y_parallel!

pool.close()

end = time.time() #record finish time

print("TOOK " + str(round(end - start,3)) + " SECONDS \n\n") #TOOK 5046.116 SECONDS = 84 minnutes
