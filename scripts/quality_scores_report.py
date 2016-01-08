#!/usr/bin/env python

import \
 numpy as np, \
 sys, \
 os

import matplotlib
matplotlib.use('Agg');
import matplotlib.pyplot   as plt
import matplotlib.gridspec as gridspec

tmpd_path = sys.argv[1];
file_path = sys.argv[2];
file_name = sys.argv[3];

# IDENTIFY SUMMARY FILE
basename  = file_name.split('/')[-1].split('.fastq')[0];
file_summ = tmpd_path+'/'+basename+'.stddev';

# READ SUMMARY FILE 
fid = open(file_summ,'r');
count  = fid.readline().strip().split(',');
means  = fid.readline().strip().split(',');
stddev = fid.readline().strip().split(',');
fid.close()

# WRITE SUMMARY REPORT
file_summ = file_path+'/'+basename+'.summary.txt';
fid = open(file_summ,'w+');
fid.write('#Average of quality scores per nucloetide position\n');
fid.write(",".join([("%0.3f" % float(ii)) for ii in means])+"\n")
fid.write('#Standard deviation of quality scores per nucleotide position\n');
fid.write(",".join([("%0.3f" % float(ii)) for ii in stddev])+"\n")
fid.write('#Total bases per nucleotide position bins\n');
fid.write(",".join([("%i" % int(ii)) for ii in count])+"\n")
fid.close()

# PLOT SUMMARY RESULTS
file_summ = file_path+'/'+basename+'.summary.pdf';

means  = [float(ii) for ii in means];
stddev = [float(ii) for ii in stddev];
counts = [int(ii)   for ii in count];

matplotlib.rcParams.update({'font.size':22});

plt.figure(figsize=[10,14]);
ax1=plt.subplot2grid((2,1),(0,0));
ax2=plt.subplot2grid((2,1),(1,0));
plt.subplots_adjust(hspace=0.3,left=0.20);

high = [xx+yy for xx,yy in zip(means,stddev)];
low  = [xx-yy for xx,yy in zip(means,stddev)];

ax1.plot(means,color='blue',lw=4,label='mean');
ax1.fill_between(x=range(len(means)),\
                 y1=low,\
		 y2=high,\
                 color='blue',alpha=0.20);
ax1.set_xlabel('Nucloetide Position',fontsize=25);
ax1.set_ylabel('Quality Score',fontsize=25);
ax1.set_ylim([0,45]);
ax1.axhline(y=25,xmin=0,xmax=len(means)+1,lw=4,color='red',linestyle='--');
ax1.grid()

ax2.plot(counts,color='black',lw=4,label='mean');
ax2.set_xlabel('Nucloetide Position',fontsize=25);
ax2.set_ylabel('Nucleotide Counts',fontsize=25);
ax2.set_ylim([0,float(np.max(counts))*1.2]);
ax2.grid();

plt.suptitle(basename+'.fastq',fontsize=30)
plt.savefig(file_summ,orientation='portrait',format='pdf',dpi=150);
