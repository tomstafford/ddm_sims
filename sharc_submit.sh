#!/bin/bash
#$ -pe smp 16
#$ -l rmem=3G 
#$ -P rse

#Load the hddm environment
module load apps/python/conda
source activate hddm

python -W ignore run_simulation.py

