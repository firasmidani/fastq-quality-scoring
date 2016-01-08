#!/usr/bin/env python

import \
 sys, \
 os

# IMPORT ARGUMENTS
code_path  = sys.argv[1];
tmpd_path  = sys.argv[2];
file_name  = sys.argv[3];
num_parts  = sys.argv[4];
max_length = sys.argv[5];


# INFER FILENAMES FOR FASTQ PARTS
numDigits = str(len(num_parts));
basename  = file_name.split('.fastq')[0];
part_frmt = "%0"+numDigits+".f";

# INITIALIZE TRACERS OF JOB ARRAY COMPLETIONS
fastq_part_names = [];
for part in range(1,int(num_parts)+1):
	pn = tmpd_path+'/'+basename+'.part-'+(part_frmt % part)+'.qual.complete';
	fastq_part_names.append(pn);

# SLURMIZE FASTQ SPLITTING COMMAND
cmd_name = file_name+'.compute_sum_quality_scores.slurm';
cmd_file = tmpd_path+'/'+cmd_name; 

#  FASTQ SPLITTING COMMAND
cmd  = 'srun \\\n';
cmd += ' -o '+tmpd_path+'/'+cmd_name+'.part.$SLURM_ARRAY_TASK_ID.out \\\n';
cmd += ' -e '+tmpd_path+'/'+cmd_name+'.part.$SLURM_ARRAY_TASK_ID.err \\\n';
cmd += ' python \\\n';
cmd += '  '+code_path+'/compute_sum_quality_scores.py \\\n';
cmd += '   $fastq_part_name \\\n';
cmd += '   '+tmpd_path+'\\\n';
cmd += '   '+max_length+'\n';

fid  = open(cmd_file,'w');
fid.write('#!/bin/sh\n\n');
fid.write('#SBATCH --time-min=30\n');
fid.write('#SBATCH --mem=4GB\n');
fid.write('#SBATCH --array=1-'+num_parts+'\n\n');
fid.write('num_parts='+num_parts+'\n');
fid.write('part_number=$(printf "%0*d" ${#num_parts} $SLURM_ARRAY_TASK_ID)\n');
fid.write('fastq_part_name='+tmpd_path+'/'+basename+'.part-$part_number.qual\n\n');
fid.write(cmd+'\n');
fid.write('touch '+'$fastq_part_name.complete\n');
fid.close();

# SUMBIT FASTQ SPLITTING JOB
os.system('sbatch '+cmd_file);

# WAIT FOR FASTQ SPLITTING JOB COMPLETION
complete = 0;
while complete == 0:
	cnt = 0;
	os.system('sleep 5');
	for ff in fastq_part_names:
		if os.path.isfile(ff):
			cnt+=1;
	if cnt==(len(fastq_part_names)):
		complete=1;

# CLEAN UP YOUR GARBAGE
os.system('rm '+tmpd_path+'/*.complete');
