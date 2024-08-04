/home/PYY/miniconda3/bin/cutadapt -g NNNNNATACACGACGCTCTTCCG -o r1.1.fastq bc321.1.fastq 
/home/PYY/miniconda3/bin/cutadapt -a CCTCCTACGCTTCG -o r1.2.fastq r1.1.fastq
/home/PYY/miniconda3/bin/cutadapt -a GCCAGAGGCTTC -o r1.3.fastq r1.2.fastq
cat r1.3.fastq | /home/PYY/miniconda3/bin/seqkit  seq -m 100 -M 134 -g | /home/PYY/miniconda3/bin/seqkit subseq -r 1:61  > r1.4.fastq
/home/PYY/miniconda3/bin/cutadapt -u 11 -o r1.5.fastq r1.4.fastq
cat r1.5.fastq | /home/PYY/miniconda3/bin/seqkit seq -s > r1.6.fastq

/home/PYY/miniconda3/bin/cutadapt -g NNNNNATACACGACGCTCTTCCG -o r2.1.fastq bc321.2.fastq
/home/PYY/miniconda3/bin/cutadapt -a CCTCCTACGCTTCG -o r2.2.fastq r2.1.fastq
/home/PYY/miniconda3/bin/cutadapt -a GCCAGAGGCTTC -o r2.3.fastq r2.2.fastq
cat r2.3.fastq | /home/PYY/miniconda3/bin/seqkit  seq -m 100 -M 134 -g | /home/PYY/miniconda3/bin/seqkit subseq -r 1:61  > r2.4.fastq
/home/PYY/miniconda3/bin/cutadapt -u 11 -o r2.5.fastq r2.4.fastq
cat r2.5.fastq | /home/PYY/miniconda3/bin/seqkit seq -s > r2.6.fastq

cat r1.6.fastq r2.6.fastq | sort | uniq -c > S2.fastq
#rm r*.fastq
