#!/bin/bash
#SBATCH -J demo
#SBATCH -p cpu
#SBATCH -n 20
#SBATCH -o demo.out


python /home/yanxiaod/scripts/sc_pipeline_11.py demo_S5 1

