___author___ Firas Said Midani
___e-mail___ firas.midani@duke.edu
___date___   2016.01.08

A repository for computing distribution of quality scores at each nucleotide base in FASTQ file. Pipeline intended for usage with SLURM (Simple Linux Utility for Resource Management). 

Usage*
-----
sbatch compute_quality_score.py [full path to FASTQ file] [full path to scripts folder in repository] [number of parallel jobs] [maximum length of sequence in FASTQ file]

* Currently, to encourage provenance, the driver script (compute_quality_scores.py) should be copies and called in the parent directory of each sequencing run. Thus, parameters must be hardcoded in the driver script.

ACKNOWLEDGEMENTS
----------------
* fastq-splitter.pl is written by Kirill Kryukov (2014) and distributed under the zlib/libpng license (http://kirill-kryukov.com/study/tools/fastq-splitter/)
* pipeline was motivated by improvements to quality_scores_plot.py by QIIME (http://qiime.org/scripts/quality_scores_plot.html). 
