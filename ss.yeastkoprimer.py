# v1.0  - 170518 first version for Mice Lv CR project, yeast validation

from Bio import SeqIO
path = "C:/Users/kisud/Desktop/"
f_name = "S288C_YER015W_FAA2_flanking.fsa"
for f_line in SeqIO.parse(path+f_name,"fasta"):
    seq_name = f_line.id
    sequen = f_line.seq
    seq_len = len(f_line)
print("%s has read with length %i." %(seq_name,seq_len))

from Bio.Seq import Seq
from Bio.Alphabet import generic_dna
forward = sequen[955:1000]
rev_tmp = sequen[seq_len-1000:seq_len-955]
reverse = rev_tmp.reverse_complement()
print('f= '+forward+'\nr= '+reverse)

# for primer specificity validation
# https://www.ncbi.nlm.nih.gov/tools/primer-blast/index.cgi?LINK_LOC=BlastHome
