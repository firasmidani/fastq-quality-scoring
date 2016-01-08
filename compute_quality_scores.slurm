#!/bin/sh

#SBATCH --time-min=120
#SBATCH --mem=2GB

file_path=/home/lad44/davidlab/seq_data/2015_12_31_seq_joined/rawdata/decompressed/10k_I1.fastq
code_path=/home/lad44/davidlab/users/fsm/qualityScoring/scripts
num_parts=10
max_length=500

## INITIALIZE PATH VARIABLES

file_name=$(basename $file_path);
file_path=$(dirname  $file_path);
tmpd_path=$file_path/tmp_$file_name

## INITIALIZE BY CONSTRUCTING TEMPORARY FOLDER AND COPY OF FASTQ FILE
if    [ -d "$tmpd_path" ]; 
    then rm $tmpd_path/*
else mkdir "$tmpd_path"; 
     fi 

cp $file_path/$file_name $tmpd_path/$file_name

## SPLIT FASTQ (JOB)
srun -o $tmpd_path/split_fastq_file.out \
     -e $tmpd_path/split_fastq_file.err \
     perl \
	$code_path/fastq-splitter.pl \
	$tmpd_path/$file_name \
        --measure seq \
        --n-parts $num_parts

## CONVERT FASTQ TO QUAL (JOB)
srun -o $tmpd_path/distribute_convert_fastq_to_qual.out \
     -e $tmpd_path/distribute_convert_fastq_to_qual.err \
     python \
	$code_path/distribute_convert_fastq_to_qual.py \
	$tmpd_path \
	$file_name \
	$num_parts

## COMPUTE SUMS (& COUNTS) OF QUALITY SCORES AT EACH BASE (JOB)
srun -o $tmpd_path/distribute_compute_sum_quality_scores.out \
     -e $tmpd_path/distribute_compute_sum_quality_scores.err \
     python \
        $code_path/distribute_compute_sum_quality_scores.py \
	$code_path \
	$tmpd_path \
	$file_name \
	$num_parts \
        $max_length 

# COMPUTE MEANS OF QUALITY SCORES AT EACH BASE (JOB)
srun -o $tmpd_path/compute_mean_quality_scores.out \
     -e $tmpd_path/compute_mean_quality_scores.err \
     python \
        $code_path/compute_mean_quality_scores.py \
        $tmpd_path \
	$file_name \
	$num_parts \
	$max_length

## COMPUTE SUM OF SQUARES OF QUALITY SCORES AT EACH BASE (JOB)
srun -o $tmpd_path/distribute_compute_sumsq_quality_scores.out \
     -e $tmpd_path/distribute_compute_sumsq_quality_scores.err \
     python \
        $code_path/distribute_compute_sumsq_quality_scores.py \
	$code_path \
	$tmpd_path \
	$file_name \
	$num_parts \
        $max_length 

## COMPUTE STANDARD DEVIATION OF QUALITY SCORES AT EACH BASE (JOB)
srun -o $tmpd_path/compute_std_dev_quality_scores.out \
     -e $tmpd_path/compute_std_dev_quality_scores.err \
     python \
        $code_path/compute_std_dev_quality_scores.py \
        $tmpd_path \
        $file_name \
	$num_parts \
	$max_length

## PRINT SUMMARY TEXT FILE AND FIGURE (PDF)
srun -o $tmpd_path/quality_scores_report.out \
     -e $tmpd_path/quality_scores_report.err \
     python \
	$code_path/quality_scores_report.py \
	$tmpd_path \
	$file_path \
	$file_name

## CLEAN UP THE GARBAGE YOU LEFT BEHIND
if [ -d "$tmpd_path" ]; then rm -r $tmpd_path; fi

## END OF SCRIPT
