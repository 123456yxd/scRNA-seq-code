## Supplement to "Prokaryotic single-cell RNA sequencing by in situ combinatorial indexing" (doi: 10.1038/s41564-020-0729-6)
## Written by Sydney Blattman
## Tavazoie Lab, Columbia University
## Last updated March 2020 

import sam_edit_tools
import sys
import os
import multiprocessing

def pipeline(sample,ID,name,gff):
	#with open(ID + '_selected_cumulative_frequency_table.txt') as fin:
        #	for line in fin:
        #    		name = line.strip().split('\t')[1]
        name = name.replace(ID,"R2")
        infile = old_sample + '_bwa_sam/' + name + "_bwa.sam"
        outfile = sample +"_no_XT/" + name + "_no_XT.sam"
        sam_edit_tools.no_xt_new(infile,outfile)
    			
	os.system('samtools view -bS ' + sample + "_no_XT/" +  name + '_no_XT.sam | samtools sort ->  ' + sample + "_no_XT/" +  name + '_no_XT_sorted.bam')    			
	os.system('samtools index  ' + sample + '_no_XT/' + name + '_no_XT_sorted.bam')
	os.system('featureCounts -t CDS -g gene_id -a ' + gff + ' -o  ' + sample + "_FC/" + name + '_FC -R BAM  ' + sample + "_no_XT/" + name + '_no_XT_sorted.bam')
    	os.system('samtools index ' + sample + '_FC/' + name + '_no_XT_sorted.bam.featureCounts.bam')
	os.system('/home/yanxiaod/.local/bin/umi_tools group --per-gene --gene-tag=XT -I  ' + sample + "_FC/" + name + '_no_XT_sorted.bam.featureCounts.bam --group-out=' + sample + '_FC_directional_grouped_2/' + name + "_UMI_counts.tsv.gz --method=directional --output-bam -S " + sample + '_FC_directional_grouped_2/' + name + "_group_FC.bam")



ID = sys.argv[1] 
if len(sys.argv) > 2:
    sample = sys.argv[2]
else:
    sample = ID
if len(sys.argv) > 3:
    old_sample = sys.argv[3]
os.system('mkdir ' + sample + '_no_XT/')
gff = sys.argv[4]
table = open(ID+'_selected_cumulative_frequency_table.txt')

os.system('mkdir ' + sample + '_FC')
os.system('mkdir ' + sample + '_FC_directional_grouped_2')
os.system('mkdir ' + old_sample + '_logs/featureCounts_directional_5')
jobs = []
pool =  multiprocessing.Pool(10)
for line in table:
    name = line.split('\t')[1]
    pool.apply_async(pipeline,args=(sample,ID,name,gff))
pool.close()
pool.join()
