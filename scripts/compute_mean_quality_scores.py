#!/usr/bin/env python

import \
 numpy as np, \
 sys, \
 os

# IMPORT ARGUMENTS
tmpd_path  = sys.argv[1]
file_name  = sys.argv[2];
num_parts  = sys.argv[3]
max_length = sys.argv[4];

# INFER FILENAMES FOR FASTQ PARTS
numDigits = str(len(num_parts))
basename  = file_name.split('.fastq')[0];
part_frmt = "%0"+numDigits+".f";

total_sum   = [0]*int(max_length);
total_count = [0]*int(max_length);

# PARSE THROUGH EACH FILE AND GET TOTAL SUMS AND COUNTS

for part in range(1,int(num_parts)+1):

	fileToRead = tmpd_path+'/'+basename+'.part-'+(part_frmt % part)+'.qual.sums';

	fid = open(fileToRead,'r');
	current_count = fid.readline().strip().split(',');
	current_sum   = fid.readline().strip().split(',');

	total_count   = [int(cc)+int(tt) for cc,tt in zip(current_count,total_count)];
	total_sum     = [int(cc)+int(tt) for cc,tt in zip(current_sum,total_sum)];
	fid.close()
#endfor

# What is the longest read length detected? 
longest_read_length = len(total_count)-np.where(np.cumsum(total_count[::-1]))[0][0];

# COMPUTE TOTAL MEAN 
total_count = total_count[:longest_read_length];
total_sum   = total_sum[:longest_read_length];

total_mean    = [float(ss)/cc for ss,cc in zip(total_sum,total_count)];


# EXPORT COUNTS AND SUMS OF BASE' QUALITY SCORES
outfile  = open(tmpd_path+'/'+basename+'.means','w+');
outfile.write(','.join([str(ii) for ii in total_mean])+'\n');
outfile.write(','.join([str(ii) for ii in total_count])+'\n');
outfile.write(','.join([str(ii) for ii in total_sum])+'\n');
outfile.close()

