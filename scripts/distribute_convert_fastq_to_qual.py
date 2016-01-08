#!/usr/bin/env python

import \
 sys, \
 os

# IMPORT ARGUMENTS
tmpd_path = sys.argv[1];
file_name = sys.argv[2];
num_parts = sys.argv[3];

# INFER FILENAMES FOR FASTQ PARTS
numDigits = str(len(num_parts));
basename  = file_name.split('.fastq')[0];
part_frmt = "%0"+numDigits+".f";

# INITIALIZE TRACERS OF JOB ARRAY COMPLETIONS
fastq_part_names = [];
for part in range(1,int(num_parts)+1):
	pn = tmpd_path+'/'+basename+'.part-'+(part_frmt % part)+'.fastq.complete';
	fastq_part_names.append(pn);

#  FASTQ SPLITTING COMMAND
cmd  = 'srun \\\n';
cmd += ' python \\\n';
cmd += '  /opt/qiime/1.8.0/bin/convert_fastaqual_fastq.py \\\n';
cmd += '  -f $fastq_part_name \\\n';
cmd += '  -c fastq_to_fastaqual \\\n';
cmd += '  -o '+tmpd_path+'\n';

# SLURMIZE FASTQ SPLITTING COMMAND
cmd_name = file_name+'.convert.to.qual.slurm';
cmd_file = tmpd_path+'/'+cmd_name; 

fid  = open(cmd_file,'w');
fid.write('#!/bin/sh\n\n');
fid.write('#SBATCH --time-min=30\n');
fid.write('#SBATCH --mem=4GB\n');
fid.write('#SBATCH --array=1-'+num_parts+'\n');
fid.write('#SBATCH --output='+tmpd_path+'/'+cmd_name+'.out\n');
fid.write('#SBATCH --error='+tmpd_path+'/'+cmd_name+'.err\n\n');
fid.write('source /opt/qiime/1.8.0/activate.sh\n\n');
fid.write('num_parts='+num_parts+'\n');
fid.write('part_number=$(printf "%0*d" ${#num_parts} $SLURM_ARRAY_TASK_ID)\n');
fid.write('fastq_part_name='+tmpd_path+'/'+basename+'.part-$part_number.fastq\n\n');
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
#os.system('rm '+tmpd_path+'/*.complete');
