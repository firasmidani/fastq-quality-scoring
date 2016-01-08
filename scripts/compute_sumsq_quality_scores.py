#!/usr/bin/env python

import \
 sys, \
 os

# IMPORT ARGUMENTS
file_path  = sys.argv[1]
outp_path  = sys.argv[2];
max_length = int(sys.argv[3]);


# WHAT IS THE MENA QUALITY SCORES AT EACH BASE
basename  = file_path.split('/')[-1].split('.part')[0];
file_name = outp_path+'/'+basename+'.means';

fid       = open(file_name,'r');
means     = fid.readline().strip().split(',');
counts    = fid.readline().strip().split(',');
fid.close();


# COUNT QULAITY SCORES AND THEIR SUMS AT EACH BASE
fid = open(file_path,'r');

sumsq = [0]*max_length;

readquals = 0;

for line in fid:

	#initialize sequence of quality scores
	if (line[0]!=">") and (readquals == 1):

		line = line.strip().split(' ');
		seq  = seq + line;

	#append to sequence of qulaity scores
	elif (line[0]==">") and (readquals==1):
		for ii,ss in zip(range(len(seq)),seq):
			sumsq[ii] += (float(means[ii])-int(ss))**2;
		seq=[];
	
	#start another cycle of reading squences of quality scores
	elif (line[0]==">") and (readquals==0):

		seq=[];
	        readquals=1;	
	#endif
#endfor

for ii,ss in zip(range(len(seq)),seq):
	sumsq[ii] += (float(means[ii])-int(ss))**2;
#endfor

fid.close()


# EXPORT COUNTS AND SUMS OF BASE' QUALITY SCORES
basename = file_path.split('/')[-1]; 
outfile  = open(outp_path+'/'+basename+'.sumsq','w+');
outfile.write(','.join([str(ii) for ii in counts])+'\n');
outfile.write(','.join([str(ii) for ii in means])+'\n');
outfile.write(','.join([str(ii) for ii in sumsq])+'\n');
outfile.close()

