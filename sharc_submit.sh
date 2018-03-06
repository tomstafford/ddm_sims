#!/bin/bash
#$ -pe smp 32
#$ -l rmem=3G 
#$ -P rse
#$ -l h_rt=48:00:00

#Load the hddm environment
module load apps/python/conda
source activate hddm

python -W ignore run_simulation.py

