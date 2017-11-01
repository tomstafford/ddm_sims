# ddm_sims
**Simulating decision making data and parameter recovery**

**Running the simulation**

To run the simulation, do

```
python run_simulation.py
```

There are a bunch of warnings.  If you are happy to ignore them, run it with

```
python -W ignore run_simulation.py
```

** Parallelisation **

With the following parameters

```
n_experiments = 50  # Number of simulated experiments  - make this arbitrary large for final run
n_subjects = [10,20,30,100] # n_participants in each experiment
stim_A = 0.2 # Stimulus A - Drift Rate = 0.2
stim_B = 0.3 # Stimulus B - Drift Rate = 0.6
intersubj_drift_var=0.1 # std
n_samples = 100 #for HDDM fitting, put this to 5000 for final run
trial_name = 'ppt_test' # Specfies what each trial is running - e.g. altered number of participants
trials = 20 # trial per participants
```

I got the following times on a 4 core Mid 2014 Macbook Pro.  
There seems to be very little to gain from oversubscribing the cores.

* 1 process   - 1790 seconds
* 4 processes - 584 seconds
* 8 processes - 567 seconds   (3.1x speedup)
