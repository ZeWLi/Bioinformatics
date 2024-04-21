This is a script for adaptor removal when submitting genomes to NCBI database. When NCBI pipeline finds your adaptors that they can't automatically fix, you can use this script to remove adaptors as suggested in 'RemainContamination' file.

Dependency: Bio.SeqIO, Bio.SeqRecord

## Usage:
```
python adaptor_removal_for_submit.py RC_folder fasta_folder output_folder
```


RC_folder is a folder with all your 'RemainContamination' files
fasta_folder is a folder with your genomes your need to fix (This script identifies genome name with format 'XX_XX_bins_XX.fasta'. If your submitted genomes are not named like that you need to custom the 66th line in this script.
output_folder will contain your genomes after adaptor removal
