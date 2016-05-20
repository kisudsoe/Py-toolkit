# 2016-05-20 FRI
# v1.1  - 160520, add function: save fimo result filtered by qv_thr as a tsv format
# v1.0  - 160519, create meme file from fimo result 
## Yeast project: Make logo from FIMO result (4689 genes) to ceqlogo format
import os.path
from tqdm import *
def fimo2logo(file_NAME,out_dir,qv_thr=0.05,debug=False):
    dir_PATH = 'D:\\KimSS-NAS\\LFG\\Works\\2016.04 Yeast HD LD Rho0\\(Archive) FIMO analysis'
    PATH = dir_PATH+file_NAME
    
    # 1. Read file & Split read data for array
    fimo_f = open(PATH,'r')
    fimo_fc = fimo_f.readlines()
    fimo_f.close()
    
    fimo_rows = []
    for row in fimo_fc:
        fimo_rows.append(row.split('\t')) # split by tab
    print('1. scanned fimo file -> columns= %d, rows= %d' % (len(fimo_rows[1]),len(fimo_rows)))
    
    # 2. Filter data by qv_thr value from read FIMO file
    fimo_5 = [row for row in fimo_rows[1:] if float(row[7]) <qv_thr] # filter action
    print('2. filtered fimo file by FDR q-value< %s -> columns= %d, rows= %d' % (str(qv_thr),len(fimo_5[1]),len(fimo_5)))
    if debug==True: print('\n--First ten list of filtered fimo data:\n%s'%fimo_5[:10])
    
    # 2-1. Save filtered data as tsv file
    NAME = file_NAME.split('\\')[2].split('.')[0]
    NAME = NAME+'_qv_thr_'+str(qv_thr)+'.tsv'
    fimo_5_out = ['\t'.join(fimo_rows[0])]
    for row in fimo_5:
        fimo_5_row = '\t'.join(row)
        fimo_5_out.append(fimo_5_row)
    fimo_5_out = ''.join(fimo_5_out)
    with open(dir_PATH+'\\'+out_dir+'\\'+NAME,'w') as f:
        f.write(fimo_5_out)
        print('2-1. file written done: %s.tsv' % NAME)
    
    # 3. Make pattern list
    pttn = [row[0] for row in fimo_5] # extract column 0
    pttn_li = list(set(pttn))
    print('3. listed %d pattern names' % len(pttn_li))
    if debug==True: print('%s\n'%pttn_li)
        
    # 3-1. Make sequences to meme format by listed pattern name
    meme = ['MEME version 4\n\nALPHABET= ACGT\n\nstrands: + -\n\nBackground letter frequencies (from uniform background):\nA 0.25000 C 0.25000 G 0.25000 T 0.25000']
    for i in tqdm(range(0,len(pttn_li))):
        pttn_tbl = [r for r in fimo_5 if r[0]==pttn_li[i]]
        if debug==True: print('iter= %d, %s sequences= %d'%(i,pttn_li[i],len(pttn_tbl)))
        pttns = [row[8] for row in pttn_tbl] # extract sequences at column 8
        
        con1 = '\nMOTIF ' + pttn_li[i]
        w = len(pttns[0])-1
        nsites = len(pttn_tbl)
        lpmatrix = con1+'\n\nletter-probability matrix: alength= 4 w= '+str(w)+' nisites= '+str(nsites)+' E= 0\n'
        
        pttn_mat = []
        for j in range(0,w):
            letters = ''.join([let[j] for let in pttns])
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
    
    # 4. Generate '.meme' file
    NAME = file_NAME.split('\\')[2].split('.')[0]
    with open(dir_PATH+'\\'+out_dir+'\\'+NAME+'.meme','w') as f:
        f.write(meme)
        print('4. file written done: %s.meme' % NAME)
    
    return()

# %%
fimo2logo('\\160518_intergenic_4689_YEASTRCT\\fimo_4689_yeastract.tsv','160519_intergenic_4689_qv_5_fimo2logo',qv_thr=0.05)
fimo2logo('\\160518_intergenic_4689_Jaspar\\fimo_4689_jaspar.tsv','160519_intergenic_4689_qv_5_fimo2logo',qv_thr=0.05)
fimo2logo('\\160518_intergenic_4689_SwissRegulon\\fimo_4689_swiss.tsv','160519_intergenic_4689_qv_5_fimo2logo',qv_thr=0.05)
fimo2logo('\\160518_intergenic_4689_UniPROBE\\fimo_4689_uniprobe.tsv','160519_intergenic_4689_qv_5_fimo2logo',qv_thr=0.05)