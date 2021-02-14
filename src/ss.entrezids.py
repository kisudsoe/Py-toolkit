#
# Get Entrez Gene ID
## v1.0 160203 First version
## v1.1 160627 Second edition
## v1.2 160704 Add yeast id search format
## v1.3 161005 Add option for Huamn X-ald project
from Bio import Entrez # just one-time
def getid(item,taxon,debug=False):
    Entrez.email="kisudsoe@gmail.com"
    sepbar = '-'*30
<<<<<<< HEAD
    animal = 'Mus musculus'
=======
    if taxon=='M': animal = 'Mus musculus'
    elif taxon=='Y': animal = 'Saccharomyces cerevisiae'
    elif taxon=='H': animal = 'Homo sapiens'
    else:
        print('Please input taxon \n\tM, mouse\n\tY, yeast\n\tH, human')
>>>>>>> 4c53cc8f2b3155edc238f1d794ee69c972d01c6b

    if(item=='---'):
        if(debug==True): print('No gene name here to search.')
        return(['---','---','---'])
    else:
        # Get entrez id from search string
        search_string = item+"[Gene] AND "+animal+"[Organism]"
        handle = Entrez.esearch(db="gene",
                                term=search_string)
        gsearch = Entrez.read(handle)
        handle.close()
        ids = gsearch['IdList']
        if len(ids)==0: # bugfix 160203
            if(debug==True): print('No result from search.')
            return(['---','---','---'])
        else:
            item_id = ids[0]
        if(debug==True): print('Search id for %s is %s' % (search_string,item_id))

        # Valid id with info - added for 160627 ver
        # Get gene information of entrez id
        handle = Entrez.efetch(db="gene",
                               id=item_id,
                               rettype="gb",
                               retmode="text")
        ginfo = handle.read()
        handle.close()
        if(debug==True):
            print('Search result'+sepbar+ginfo) # get data as string

        # Parsing ginfo to extract official gene symbol
        ginfo_spl = ginfo.split("\n")
        #print(ginfo_spl)
        for i in range(1,len(ginfo_spl)):
            ## Search symbol deposit
            if taxon=='M': id_ann = ginfo_spl[i].find('Official Symbol:')
            elif taxon=='Y': id_ann = ginfo_spl[i].find('1. ')

            if(id_ann>=0):
                if taxon=='M': ginfo_sym = ginfo_spl[i].split(" ")[2]
                elif taxon=='Y': ginfo_sym = ginfo_spl[i].split(" ")[1]
                break
            elif(i==len(ginfo_spl)-1 and id_ann==-1):
                ginfo_sym = 'NA'
                if(debug==True): print('='*10+' ERROR '+'='*10+'\n No Symbol in this gene.')
                return([item,item_id,'---'])
        if(debug==True): print(ginfo_sym)
    return([item,item_id,ginfo_sym])

## Get Entrez Gene ID using 'getid' function
import timeit
from tqdm import *
def getidList(data,taxon,debug=False):
    out = []
    for i in tqdm(range(0,len(data))):
        tmp = getid(data[i],taxon)
        out.append(tmp)
        if debug==True: print(i)
    return(out)

## Collect 1 kb resion centered on TSS
from Bio import Entrez
from Bio import SeqIO
def getSeq(item_id,taxon,debug=False):
    Entrez.email="kisudsoe@gmail.com"
    sepbar = '-'*30
    #item = 'Fndc1'
    if taxon=='M': animal = 'Mus musculus'
    elif taxon=='Y': animal = 'Saccharomyces cerevisiae'
    elif taxon=='H': animal = 'Homo sapiens'
    else:
        print('Please input taxon \n\tM, mouse\n\tY, yeast\n\tH, human')
    #search_string = item+"[Gene] AND "+animal+"[Organim] AND mRNA[Filter] AND RefSeq[Filter]"

    if(item_id=='---'):
        #print('No gene name here to search.')
        return([item_id,'---'])
    else:
        # Get gene information of entrez id
        handle = Entrez.efetch(db="gene",
                               id=item_id,
                               rettype="gb",
                               retmode="text")
        ginfo = handle.read()
        handle.close()
        if(debug==True):
            print('Search result'+sepbar+ginfo) # get data as string

        # Parsing ginfo to extract nucore id and coordinate
        ginfo_spl = ginfo.split("\n")
        for i in range(1,len(ginfo_spl)):
            id_ann = ginfo_spl[i].find('Annotation:')
            if(id_ann>=0):
                ginfo_ann = ginfo_spl[i].split(" ")
                break
            elif(i==len(ginfo_spl)-1 and id_ann==-1):
                ginfo_ann = 'NA'
                if(debug==True): print('='*10+' ERROR '+'='*10+'\n No annotation in this gene.')
                return([item_id,'---'])

    if(item_id!='---' and ginfo_ann!='NA'):
        if len(ginfo_ann)>4:
            ginfo_ann_strand = ginfo_ann[4].split(")")[0]
        else:
            ginfo_ann_strand = 'null'

        if ginfo_ann_strand=='complement':
            strand = 2
        else:
            strand = 1
<<<<<<< HEAD
        ginfo_ann_id = 'NC'+ginfo_ann[2].split("NC")[1]
        ginfo_ann_seqst = int(ginfo_ann[3].split("..")[0].split("(")[1])
        ginfo_ann_seqsp = int(ginfo_ann[3].split("..")[1].split(",")[0].split(")")[0])
=======
        #print("\n note:\n"+ginfo_ann[4]+"\n")
        if taxon=='H': # debug 161005
            ginfo_ann_id = 'NC'+ginfo_ann[3].split("NC")[1]
            ginfo_ann_seqst = int(ginfo_ann[4].split("..")[0].split("(")[1])
            ginfo_ann_seqsp = int(ginfo_ann[4].split("..")[1].split(",")[0].split(")")[0])
        else :
            ginfo_ann_id = 'NC'+ginfo_ann[2].split("NC")[1]
            ginfo_ann_seqst = int(ginfo_ann[3].split("..")[0].split("(")[1])
            ginfo_ann_seqsp = int(ginfo_ann[3].split("..")[1].split(",")[0].split(")")[0])
>>>>>>> 4c53cc8f2b3155edc238f1d794ee69c972d01c6b

        if(debug==True):
            print('Parsing result'+sepbar+'\nseq_id= %s' % ginfo_ann_id)
            print('strand= %s (%s)' % (strand,ginfo_ann_strand))
            print('seq_start= %s, seq_stop= %s'% (ginfo_ann_seqst, ginfo_ann_seqsp))
            print('gene length= %d bp\n' % (ginfo_ann_seqsp-ginfo_ann_seqst+1))

        # Get DNA sequence by location
        handle = Entrez.efetch(db="nuccore",
                               id=ginfo_ann_id,
                               strand=strand,
                               rettype="fasta",
                               seq_start=ginfo_ann_seqst-1000,
                               seq_stop=ginfo_ann_seqst-1,
                               retmode="text")
        seq_fa = handle.read()
        seq_fa = seq_fa.replace('\n\n','')
        if(debug==True):
            #record = SeqIO.read(handle,"fasta")
            print('Up-stream 1 kb seq'+sepbar+'\n'+seq_fa)
        return([item_id,seq_fa])

# Collect sequences from Entrez ID list
def getSeqList(data,taxon):
    start = timeit.default_timer()
    for i in range(0,len(data)):
        if i==0:
            out = getSeq(data[i],taxon)
        elif i==1:
            tmp = getSeq(data[i],taxon)
            out = [out,tmp]
        else:
            tmp = getSeq(data[i],taxon)
            out.append(tmp)

        if i%30 ==0 : # Print Process
            print('now process= %d %% (%d/%d iteration)'
            % (round(i*100/len(data),2),i,len(data)))
        elif i==len(data)-1:
            print('now process= %d %% (%d/%d iteration)'
            % (round(i*100/len(data),2),i,len(data)))
    stop = timeit.default_timer()
    ti = stop-start
    m,s = divmod(ti, 60)
    h,m = divmod(m,60)
    print('Process takes %d:%02d:%02d\n' % (h,m,s))
    return(out)
    
# 2016-05-17
# Save out as csv file
import csv
def savecsv(data,name='pyout.csv',dir='C:/Users/KimSS-Work/Desktop',debug=False):
    #path = 'C:/Users/KimSS/Desktop/Py_output/ # Work PC
    #path = 'C:/Users/kisud/Desktop/Py_output/ # Home PC
    path = dir+name
    print('\n'+path)
    with open(path,'w',newline='') as f:
        wr = csv.writer(f)
        wr.writerows(data)

# %%
import win32clipboard # just one-time
def listIn():
    win32clipboard.OpenClipboard()
    clipb = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    
    data = clipb.split("\r\n")
    length = len(data)-1
    print('list length= %d' % length) # read data as string
    return(data[0:length])
# %% Get gene list from clipboard
genes = listIn()

# %% Execute function
genes_id = getidList(genes,"M") # using 160704 ver

<<<<<<< HEAD
genes_id = getidList(genes) # using 160627 ver
=======
# %% Save as csv file
savecsv(genes_id,name='/170417_genes_ids.csv')
>>>>>>> 4c53cc8f2b3155edc238f1d794ee69c972d01c6b
