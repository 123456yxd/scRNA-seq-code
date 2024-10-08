## Supplement to "Prokaryotic single-cell RNA sequencing by in situ combinatorial indexing" (doi: 10.1038/s41564-020-0729-6)
## Written by Sydney Blattman
## Tavazoie Lab, Columbia University
## Last updated March 2020 

import time
import os
import sys
import preprocess_2 as preprocess
import os.path
import os, errno

start = time.time()
script_dir = sys.argv[0].split('sc_pipeline_11.py')[0]
i=1
sample = sys.argv[i][0:sys.argv[i].find('_S')]
if(sys.argv[i].find('_S') == -1):
    print('error: must include _S after after sample')
    exit()
n_lanes = int(sys.argv[2])
# Clean up old files
os.system('rm -r ' + sample + '/*QF_* 2> rm.log')
os.system('rm -r ' + sample + '_bc3 2> rm.log')
os.system('rm -r ' + sample + '_bc2 2> rm.log')
os.system('rm -r ' + sample + '_bc1 2> rm.log')
os.system('rm -r ' + sample + '_bc1_table.txt 2> rm.log')
os.system('rm -r ' + sample + '_bc2_table.txt 2> rm.log')
os.system('rm -r ' + sample + '_bc3_table.txt 2> rm.log')
os.system('rm -r ' + sample + '_logs/sc_pipeline_11 2> rm.log')
os.system('rm -r ' + sample + '_bc1_cumulative_frequency_table.txt 2> rm.log')
os.system('rm -r ' + sample + '_bc2_cumulative_frequency_table.txt 2> rm.log')
os.system('rm -r ' + sample + '_bc3_cumulative_frequency_table.txt 2> rm.log')
if(os.path.exists('rm.log')):
    os.system('rm rm.log')
os.system('mkdir ' + sample + '_logs')
os.system('mkdir ' + sample + '_logs/sc_pipeline_11')
print('Preprocessing ' + sample)
# Run Fastqc on all lanes
os.system('mkdir ' + sample + '_logs/sc_pipeline_11/fastqc')
os.system('fastqc -o ' + sample + '_logs/sc_pipeline_11/fastqc ' + sample + '/*_001.fastq.gz' )
print('Fastqc done')
# trim low quality reads
os.system('cutadapt -q 10,10 --minimum-length 55:14 --max-n 3 --pair-filter=any -o ' + sample + '/' + sample + '_QF_L001_R1_001.fastq.gz -p ' + sample + '/' + sample + '_QF_L001_R2_001.fastq.gz ' + sample + '/' + sys.argv[i] + '_L001_R1_001.fastq.gz ' + sample + '/' + sys.argv[i] + '_L001_R2_001.fastq.gz > ' + sample + '_logs/sc_pipeline_11/QF.log')
print('Quality Trim Done')

# extract UMI
os.system('umi_tools extract --stdin=' + sample + '/' + sample + '_QF_L001_R1_001.fastq.gz --bc-pattern=NNNNNNN --read2-in=' + sample + '/' + sample + '_QF_L001_R2_001.fastq.gz --log=' + sample + '_logs/sc_pipeline_11/UMI_extract.log --stdout ' + sample + '/' + sample + '_QF_UMI_L001_R1_001.fastq.gz --read2-out=' + sample + '/' +  sample + '_QF_UMI_L001_R2_001.fastq.gz')

# demultiplex by bc3
os.system('mkdir ' + sample + '_bc3')
if(os.path.exists(sample + '_logs/sc_pipeline_11/bc3.log')):
    os.system('rm ' + sample + '_logs/sc_pipeline_11/bc3.log')
os.system('cutadapt -g file:'+script_dir+'sc_barcodes_v2/BC3_anchored.fa -e 0.05 --overlap 21 --untrimmed-output ' + sample + '_bc3/' + sample + '_no_bc3_L001_R1_001.fastq.gz  --untrimmed-paired-output ' + sample + '_bc3/' + sample + '_no_bc3_L001_R2_001.fastq.gz  -o ' + sample + '_bc3/' + sample + '_{name}x_L001_R1_001.fastq.gz -p ' + sample + '_bc3/' + sample + '_{name}x_L001_R2_001.fastq.gz ' + sample + '/' + sample + '_QF_UMI_L001_R1_001.fastq.gz ' + sample + '/' + sample + '_QF_UMI_L001_R2_001.fastq.gz >> ' + sample + '_logs/sc_pipeline_11/bc3.log')
print('bc3 done')

# demultiplex by bc2
os.system('mkdir ' + sample + '_bc2')
if(os.path.exists(sample + '_logs/sc_pipeline_11/bc2.log')):
    os.system('rm ' + sample + '_logs/sc_pipeline_11/bc2.log')
bc3_list = ''
for i in range(1,97):
    if(os.path.exists(sample + '_bc3/' + sample + '_bc3_' + str(i) + 'x_L001_R1_001.fastq.gz')):
       os.system('cutadapt -g file:'+script_dir+'sc_barcodes_v2/BC2_anchored.fa -e 0.05 --overlap 20 --untrimmed-output ' + sample + '_bc2/' + sample + '_bc3_' + str(i) + '_R1_no_bc2.fastq.gz  --untrimmed-paired-output ' + sample + '_bc2/' + sample + '_bc3_' + str(i) + '_R2_no_bc2.fastq.gz -o ' + sample + '_bc2/' + sample + '_R1_{name}_bc3_' + str(i) + '.fastq.gz -p ' + sample + '_bc2/' + sample + '_R2_{name}_bc3_' + str(i) + '.fastq.gz ' + sample + '_bc3/' + sample +'_bc3_' + str(i) + 'x_L001_R1_001.fastq.gz ' + sample + '_bc3/' + sample + '_bc3_' + str(i) + 'x_L001_R2_001.fastq.gz >> ' + sample + '_logs/sc_pipeline_11/bc2.log')
print('bc2 done')
#os.system('rm -r ' + sample + '_bc3')

# demultiplex by bc1
os.system('mkdir ' + sample + '_bc1')
if(os.path.exists(sample + '_logs/sc_pipeline_11/bc1.log')):
    os.system('rm ' + sample + '_logs/sc_pipeline_11/bc1.log')
for bc3 in range(1,97):
    bc2_list = ''
    for bc2 in range(1,97):
        if(os.path.exists(sample + '_bc2/' + sample + '_R1_bc2_' + str(bc2) + '_bc3_' + str(bc3) + '.fastq.gz')):
	#os.system('rm -r ' + sample + '_bc2')
            os.system('cutadapt -g file:'+script_dir+'sc_barcodes_v2/BC1_5p_anchor_v2.fa -e 0.2 --no-indels --overlap 7 --no-trim -o ' + sample + '_bc1/' + sample + '_R1_{name}_bc2_' + str(bc2) + '_bc3_' + str(bc3) + '.fastq.gz -p ' + sample + '_bc1/' + sample + '_R2_{name}_bc2_' + str(bc2) + '_bc3_' + str(bc3) + '.fastq.gz ' + sample + '_bc2/' + sample +'_R1_bc2_' + str(bc2) + '_bc3_' + str(bc3) + '.fastq.gz ' + sample + '_bc2/' + sample + '_R2_bc2_' + str(bc2) + '_bc3_' + str(bc3) + '.fastq.gz >> ' + sample + '_logs/sc_pipeline_11/bc1.log')
if(os.path.exists(sample + '_bc1_cumulative_frequency_table.txt')):
    os.system('rm ' + sample + '_bc1_cumulative_frequency_table.txt')
preprocess.log_to_table(sample,'bc1')
preprocess.log_plot(sample,'bc1',0)
preprocess.freq_plot(sample,'bc1',0)
    #os.system('rm ' + sample + '_bc1_table.txt')
print('bc1 done')
    
end = time.time()
print(end-start)

#os.system('rm -r ' + sample + '_bc3')
