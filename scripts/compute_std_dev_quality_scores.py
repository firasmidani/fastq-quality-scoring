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

total_sumsq = [0]*int(max_length);
total_count = [0]*int(max_length);

# PARSE THROUGH EACH FILE AND GET TOTAL SUMS AND COUNTS

for part in range(1,int(num_parts)+1):
	print 'part',part
	fileToRead = tmpd_path+'/'+basename+'.part-'+(part_frmt % part)+'.qual.sumsq';

	fid = open(fileToRead,'r');
	current_count = fid.readline().strip().split(',');
	current_mean  = fid.readline().strip().split(',');
	current_sumsq = fid.readline().strip().split(',');
	
	total_mean    = current_mean;
	total_count   = [int(cc) for cc in current_count];
	total_sumsq   = [float(cc)+float(tt) for cc,tt in zip(current_sumsq,total_sumsq)];
	fid.close()
#endfor


# What is the longest read length detected? 
longest_read_length = len(total_count)-np.where(np.cumsum(total_count[::-1]))[0][0];

# COMPUTE TOTAL MEAN 
total_count = total_count[:longest_read_length];
total_mean  = total_mean[:longest_read_length];
total_sumsq = total_sumsq[:longest_read_length];

total_var    = [np.sqrt(float(ss)/(cc-1)) for ss,cc in zip(total_sumsq,total_count)];

# EXPORT COUNTS AND SUMS OF BASE' QUALITY SCORES
outfile  = open(tmpd_path+'/'+basename+'.stddev','w+');
outfile.write(','.join([str(ii) for ii in total_count])+'\n');
outfile.write(','.join([str(ii) for ii in total_mean])+'\n');
outfile.write(','.join([str(ii) for ii in total_var])+'\n');
outfile.close()

