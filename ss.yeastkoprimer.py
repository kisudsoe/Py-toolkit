# v1.0  - 170518 first version for Mice Lv CR project, yeast validation
# v1.0a - 170523 code optimization for result displaying

from Bio import SeqIO
path = "C:/Users/kisud/Desktop/yeast/"
f_name = ["S288C_YOR040W_GLO4_flanking.fsa",
          "S288C_YLR372W_ELO3_flanking.fsa"]
for f_line in SeqIO.parse(path+f_name[1],"fasta"):
    seq_name = f_line.id
    sequen = f_line.seq
    seq_len = len(f_line)
print("%s has read with length %i." %(seq_name,seq_len))

from Bio.Seq import Seq
from Bio.Alphabet import generic_dna
forward = sequen[955:1000]
rev_tmp = sequen[seq_len-1000:seq_len-955]
reverse = rev_tmp.reverse_complement()
print('UP= '+forward+'\n\nrev_tmp= '+rev_tmp+'\nDN= '+reverse+'\n')
print("%s has read with length %i." %(seq_name,seq_len)+'\n\n'+sequen)

# for primer specificity validation
# https://www.ncbi.nlm.nih.gov/tools/primer-blast/index.cgi?LINK_LOC=BlastHome
