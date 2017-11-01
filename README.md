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

** Setting up the Conda environment on ShARC **

Before we can run hddm on ShARC, you need to install the conda environment in your home directory.

* Log in and start a `qrshx` session.
* Load the conda module

```
module load apps/python/conda
```
* Create the base hddm environment

```
conda create -n hddm python=3.4
```

You will be faced by a blank screen for quite a while.
Don't worry, it hasn't crashed (probably!).

* Source the new environment and install gddm
```
source activate hddm
conda install -c pymc hddm
```

** Running the simulation on ShARC **

To run the simulation currently on GitHub

```
git clone https://github.com/mikecroucher/ddm_sims
cd ddm_sims
qsub sharc_submit.sh
```

The level of parallelisation is controlled in two places.
You need to ensure that they are set to the same value.

To use 16 cores

In `sharc_submit.sh`:

```
#$ -pe smp 16
```

In `run_simulation.py`
```
pool = Pool(16)
```

The parallelisation scheme currently used is limited to the number of cores available on a single node.  This is currently 16.  32 core nodes are available but only to people who have contributed to the [RSE group's premium queue](http://rse.shef.ac.uk/resources/hpc/premium-hpc/)

We could explore additional schemes for better scaling.

** Parallelisation timings (small job)**

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

**4 core Mid 2014 Macbook Pro**
There seems to be very little to gain from oversubscribing the cores.

* 1 process   - 1790 seconds
* 4 processes - 584 seconds
* 8 processes - 567 seconds   (3.1x speedup)

**32 core node on ShARC**

Note that this is only available to people who have contributed to the [RSE group's premium queue](http://rse.shef.ac.uk/resources/hpc/premium-hpc/).
They are more powerful than anything else on ShARC

* 32 processes -  122.661 seconds (14.7x faster than the Mac using 1 core)

** Parallelisation timings (large job)**

```
n_experiments = 100  # Number of simulated experiments  - make this arbitrary large for final run
n_subjects = [10,20,30,100] # n_participants in each experiment
stim_A = 0.2 # Stimulus A - Drift Rate = 0.2
stim_B = 0.3 # Stimulus B - Drift Rate = 0.6
intersubj_drift_var=0.1 # std
n_samples = 5000 #for HDDM fitting, put this to 5000 for final run
trial_name = 'ppt_test' # Specfies what each trial is running - e.g. altered number of participants
trials = 20 # trial per participants
```

**Timings to come**
