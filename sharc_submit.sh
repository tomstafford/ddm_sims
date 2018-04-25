#!/bin/bash
#$ -pe smp 16
#$ -l rmem=16G 
#$ -P rse
#$ -l h_rt=48:00:00
#$ -m bea
#$ -M tom@idiolect.org.uk
#$ -j y


#Load the hddm environment
module load apps/python/conda
source activate hddm

python -W ignore run_simulation2.py

