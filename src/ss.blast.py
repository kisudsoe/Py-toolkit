# -*- coding: utf-8 -*-
"""
SS.BLAST for X-ALD project
Created on Thu Oct 20 10:24:31 2016

@author: KimSS-Work
"""
# %%
# data load
import win32clipboard # just one-time
def listIn():
    win32clipboard.OpenClipboard()
    clipb = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    
    data = clipb.split("\r\n")
    #data = data.split("\t")[0]
    length = len(data)-1
    print('list length= %d' % length) # read data as string
    return(data[0:length])
# %%
# get query list
q = listIn()

# %% BLAST through online <- server busy
from Bio.Blast import NCBIWWW # http://biopython.org/DIST/docs/api/Bio.Blast.NCBIWWW-module.html
from Bio.Blast import NCBIXML
import time
#help(NCBIWWW.qblast)
def ssblast(query,database,taxon,Eval=0.01):
    connected = False
    while not connected:
        try:
            t_start = time.time()
            n = len(query)
            print('query sequence length: ',n)
            handle = NCBIWWW.qblast(program="blastn",database=database,sequence=query,
                                    entrez_query=taxon)
            blast_records = NCBIXML.parse(handle)
            E_VALUE_THRESH = Eval
            out = NULL
            for blast_record in blast_records:
                #print(blast_record)
                for alignment in blast_record.alignments:
                    for hsp in alignment.hsps:
                        if hsp.expect <E_VALUE_THRESH:
                            print('****Alignment****')
                            print('sequence:', alignment.title)
                            print('length:', alignment.length)
                            print('identities:', hsp.identities)
                            print('score:', hsp.score)
                            print('gaps:', hsp.gaps)
                            print('e-value:', hsp.expect)
                            print(hsp.query[0:75]+'...')
                            print(hsp.match[0:75]+'...')
                            print(hsp.sbjct[0:75]+'...')
                            out = [out,[alignment.title,  # sequence
                                        alignment.length, # length of alignment
                                        hsp.identities,   # identities
                                        n,                # length of query
                                        hsp.gaps,         # gaps
                                        hsp.expect]]      # e-value
            handle.close()
            print(round(time.time()-t_start, 2)," seconds")
            return(out)
            connected=True
            time.sleep(3)
        except:
            print("Server busy, will sleep and try again in 60 seconds")
            time.sleep(60)

def ssmultblast(multiq,database,taxon,Eval=0.01):
    out = []
    out.append(['sequence','a-length','identities','q-length','gaps','e-value'])
    for q in multiq:
        out.append(ssblast(q,database,taxon,Eval))
    return(out)
# %%
out = ssblast(query=q[0],database="refseq_rna",taxon="txid9606 [ORGN]")
# %%
out = ssmultblast(multiq=q,database="refseq_rna",taxon="txid9606 [ORGN]")

# %% BLAST in local
from Bio.Blast.Applications import NcbiblastxCommandline
#help(NcbiblastxCommandline)
blastx_cline = NcbiblastxCommandline(query="opuntia.fasta",
                                     db="refseq_rna", 
                                     evalue=0.001,
                                     outfmt=5, out="opuntia.xml")
blastx_cline = NcbiblastxCommandline(cmd='blastn', 
                                     query="queryfile.fas", 
                                     db="newtest.db", 
                                     evalue=0.01, 
                                     outfmt=5, out="opuntia.xml")