#!/bin/bash
#BATCH -J B1214-7
#SBATCH -p cpu
#SBATCH -n 20
#SBATCH -o B1214-7.out

sh /home/yanxiaod/scripts/pipeline.sh demo 40 /home/yanxiaod/Reference/Escherichia_coli_str_k_12_substr_mg1655_gca_000005845.ASM584v2.dna.toplevel.fa.gz /home/yanxiaod/Reference/Escherichia_coli_str_k_12_substr_mg1655.ASM584v2.46.gtf demo_CDS

