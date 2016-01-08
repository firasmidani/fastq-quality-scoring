#!/usr/bin/env python

import \
 sys, \
 os

# IMPORT ARGUMENTS
file_path  = sys.argv[1]
outp_path  = sys.argv[2];
max_length = int(sys.argv[3]);


# COUNT QULAITY SCORES AND THEIR SUMS AT EACH BASE
fid = open(file_path,'r');

sums  = [0]*max_length;
count = [0]*max_length;

readquals = 0;

for line in fid:

	#initialize sequence of quality scores
	if (line[0]!=">") and (readquals == 1):

		line = line.strip().split(' ');
		seq  = seq + line;

	#append to sequence of qulaity scores
	elif (line[0]==">") and (readquals==1):

		for ii,ss in zip(range(len(seq)),seq):
			count[ii]   += 1;
			sums[ii]    += int(ss);
		seq=[];
	
	#start another cycle of reading squences of quality scores
	elif (line[0]==">") and (readquals==0):

		seq=[];
	        readquals=1;	
	#endif
#endfor

for ii,ss in zip(range(len(seq)),seq):
	count[ii] += 1;
	sums[ii]  += int(ss);
#endfor

fid.close()


# EXPORT COUNTS AND SUMS OF BASE' QUALITY SCORES
basename  = file_path.split('/')[-1]; 
file_name = outp_path+'/'+basename+'.sums';

outfile  = open(file_name,'w+');
outfile.write(','.join([str(ii) for ii in count])+'\n');
outfile.write(','.join([str(ii) for ii in sums])+'\n');
outfile.close()


