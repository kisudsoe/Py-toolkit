########### Log of this file ###########
## Yeast project: Make logo from FIMO result to ceqlogo format
## v1.0  - 160519, create meme file from fimo result
## v1.1  - 160520a, add function: save fimo result filtered by qv_thr
## v1.2  - 160520b, add function: multiple list support
## v1.3  - 160521, support multiple file & merge output. (Bugfix needed) DBs must have different pattern names.
## v1.4  - 161110, add Database info column at exported tsv file
##                 debug duplicated motif name issue
########################################

import os.path
from tqdm import *
def fimo2logo(dir_PATH,file_li,db_li,out_dir,qv_thr=0.05,debug=False):

    # 1. Read file & Split read data for array
    fimo_rows = []
    fimo_coln = []
    print('1. Read file')
    i = 0
    for name in tqdm(file_li):
        file_NAME = '\\'+name
        if debug==True: print('  ',file_NAME)

        PATH = dir_PATH+file_NAME
        fimo_f = open(PATH,'r')
        fimo_fc = fimo_f.readlines()
        fimo_f.close()

        for j in range(0,len(fimo_fc)): # add and debug 161110
            if j==0:
                fimo_col = []
                fimo_col.append('DATABASE')
                fimo_col.extend(fimo_fc[j].split('\t'))
                fimo_coln = fimo_col
            else:
                fimo_row = []
                fimo_row.append(db_li[i])
                a_row = fimo_fc[j].split('\t')
                fimo_row.append(db_li[i]+'_'+a_row[0])
                fimo_row.extend(a_row[1:9])
                fimo_rows.append(fimo_row) # split by tab
        i+=1
    print('  -> data collection: columns= %d, rows= %d\n' % (len(fimo_rows[1]),len(fimo_rows)))

    # 2. Filter data by qv_thr value from read FIMO file
    fimo_5 = [row for row in fimo_rows if float(row[8]) <qv_thr] # filter by qv_thr
    print('2. filtered fimo file by FDR q-value< %s -> columns= %d, rows= %d' % (str(qv_thr),len(fimo_5[1]),len(fimo_5)))
    if debug==True: print('\n--First ten list of filtered fimo data:\n%s'%fimo_5[:10])

    # 2-1. Save filtered data as tsv file
    fimo_5_out = ['\t'.join(fimo_coln)]
    for row in fimo_5:
        fimo_5_row = '\t'.join(row)
        fimo_5_out.append(fimo_5_row)
    fimo_5_out = ''.join(fimo_5_out)
    NAME = 'fimo_merge_qv_thr_'+str(qv_thr)+'.tsv'
    with open(dir_PATH+'\\'+out_dir+'\\'+NAME,'w') as f:
        f.write(fimo_5_out)
        print('  -> file written done: %s\n' % NAME)

    # 3. Make pattern list
    pttn = [row[1] for row in fimo_5] # extract column 1
    pttn_li = list(set(pttn))
    print('3. listed %d pattern names' % len(pttn_li))
    if debug==True: print('%s\n'%pttn_li)

    # 3-1. Make sequences to meme format by listed pattern name
    meme = ['MEME version 4\n\nALPHABET= ACGT\n\nstrands: + -\n\nBackground letter frequencies (from uniform background):\nA 0.25000 C 0.25000 G 0.25000 T 0.25000']
    for i in tqdm(range(0,len(pttn_li))):
        pttn_tbl = [r for r in fimo_5 if r[1]==pttn_li[i]] # filter by pttn
        if debug==True: print('iter= %d, %s, sequences= %d'%(i,pttn_li[i],len(pttn_tbl)))
        pttns = [row[9] for row in pttn_tbl] # extract sequences at column 9

        con1 = '\nMOTIF ' + pttn_li[i]
        w = len(pttns[0])-1
        nsites = len(pttn_tbl)
        lpmatrix = con1+'\n\nletter-probability matrix: alength= 4 w= '+str(w)+' nisites= '+str(nsites)+' E= 0\n'

        pttn_mat = []
        for j in range(0,w):
            letters = ''.join([lett[j] for lett in pttns])
            propA = round(letters.count('A')/len(letters),6)
            propC = round(letters.count('C')/len(letters),6)
            propG = round(letters.count('G')/len(letters),6)
            propT = round(letters.count('T')/len(letters),6)
            mat_row = ''.join([str(propA),'\t',str(propC),'\t',str(propG),'\t',str(propT),'\n'])
            pttn_mat.append(mat_row)
        pttn_mat = ''.join(pttn_mat)
        meme.append(lpmatrix)
        meme.append(pttn_mat)
    meme = ''.join(meme)
    print('  -> meme format generation done.')

    # 3-2. Generate '.meme' file
    #NAME = file_NAME.split('\\')[2].split('.')[0]+'.meme'
    NAME = 'fimo_merge_qv_thr_'+str(qv_thr)+'.meme'
    with open(dir_PATH+'\\'+out_dir+'\\'+NAME,'w') as f:
        f.write(meme)
        print('  -> file written done: %s\n' % NAME)

    return()

# %%
## Make Logo from FIMO 1kb results for ceqlogo format
## Using fimo2logo - v1.4 161110
dir_path = 'D:\\KimSS-NAS\\LFG\\Works\\2016.09 Yeast dynamic network\\(Archive) FIMO analysis'
file_li = ['161109_fimo_out\\1kb flank_6274_fimo_jaspar.tsv',
           '161109_fimo_out\\1kb flank_6274_fimo_scpd.tsv',
           '161109_fimo_out\\1kb flank_6274_fimo_swiss.tsv',
           '161109_fimo_out\\1kb flank_6274_fimo_uniprobe.tsv',
           '161109_fimo_out\\1kb flank_6274_fimo_yeastract.tsv']
db_li = ['JASPAR','SCPD','SwissReulon','UniPROBE','YEASTRACT']
outdir = '161109_fimo_out'
fimo2logo(dir_path, file_li, db_li, outdir, qv_thr=0.05)
