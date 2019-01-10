# ddm_sims
*Simulating decision making data and parameter recovery*

## Workflow/file descriptions

### Folders
/attic - old stuff we can probably forget about 
/data - simulations results (raw outputs)
/figs - figures (processed data)
/for_stiching - a holding folder for outputs from simulations with the same parameters (but which require multiple jobs to generate)
/psychonomics - files for International Psychonomics Society Meeting in Amsterdam, 2018
/write_up - paper describing project

### Files

clean.sh - used to tidy up cluster after having run a job

collate.py - gather raw outputs in /for_stitching, output summary.csv
P_make_plots_new.py - make hits,FAs,drpime plots from summary.csv
P_psychonomicsplots.py - make plots for psychonomics talk

README.md - this file

run_simulaton2.py - run a job
run_simulation_SATO - run a job, with SATO (do we need this?)

sendemail.py - funciton for sending emails
sharc_submit - script for submitting job on cluster

sim_expts.py - functions for simulating data and fitting HDDM
sim_ez.py - analogous functions for simulating data and fitting with EZDDM



## Details on running the simulations

To run the simulation, edit `run_simulation.py` so that you request a `Pool` size that's suitable for your machine.
Then do,

```
python run_simulation.py
```

There are a bunch of warnings.  If you are happy to ignore them, run it with

```
python -W ignore run_simulation.py
```

**Setting up the Conda environment on ShARC**

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

**Running the simulation on ShARC**

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

**Parallelisation timings (small job)**

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

**16 core node on ShARC**

These are the standard nodes -- available to everyone.

* 16 processes 208.452 seconds

**32 core node on ShARC**

Note that this is only available to people who have contributed to the [RSE group's premium queue](http://rse.shef.ac.uk/resources/hpc/premium-hpc/).
They are more powerful than anything else on ShARC

* 32 processes -  122.661 seconds (14.7x faster than the Mac using 1 core)

**Parallelisation timings (large job)**

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

* 32 processes - 6570 seconds

