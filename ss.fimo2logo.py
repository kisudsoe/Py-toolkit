# 2016-02-02 TUE
# Make Logo input file (FIMO 1kb q-value<0.01)
# Edit Fimo for meme input files (fasta format) v1.1
import os.path
def fimo2logo(file_NAME,out_dir,qv_thr=0.05,debug=False):
    #dir_PATH = 'D:\\KimSS-NAS\\LFG\\Works\\2012.08 Sarcopenia project\\2-4.Gn array analysis_rma_r\\1.Data_rma\\(Archive) MEME analysis'
	dir_PATH = 'D:\\KimSS-NAS\\LFG\\Works\\2016.04 Yeast HD LD Rho0\\(Archive) FIMO analysis'
    #PATH = dir_PATH+'\\Total_fimo\\'+file_NAME+'.txt'
    PATH = dir_PATH+file_NAME
    
    # 1. Read file
    fimo_f = open(PATH,'r')
    fimo_fc = fimo_f.readlines()
    fimo_f.close()
    
    # 2. Get data from FIMO file
    for i in range(1,len(fimo_fc)):
        if i==1:        
            fimo_rows = fimo_fc[i].split('\t') # split by tab
        elif i==2:
            rows = fimo_fc[i].split('\t')
            fimo_rows = [fimo_rows,rows]
        else:
            rows = fimo_fc[i].split('\t')
            fimo_rows.append(rows)
    print('1. scanned fimo file -> columns= %d, rows= %d' 
    % (len(fimo_rows[1]),len(fimo_rows)))
    
    # 3. Filtered by FDR<0.05 and Extract pattern name list from FIMO
    fimo_5 = [row for row in fimo_rows if float(row[7]) <qv_thr] # filter action
    print('2.1. filtered fimo file by FDR q-value< %s -> columns= %d, rows= %d' 
    % (str(qv_thr),len(fimo_5[1]),len(fimo_5)))
    if debug==True: print('--First ten list of filtered fimo data:\n%s'%fimo_5[:10])
    
    pttn = [row[0] for row in fimo_5] # extract column 0
    pttn_li = list(set(pttn))
    print('2.2. listed %d pattern names' % len(pttn_li))
    if debug==True: print('%s\n'%pttn_li)
    
    # 4. Make sequences to fasta format by pattern name
    for i in range(0,len(pttn_li)):
        pttn_tbl = [r for r in fimo_5 if r[0]==pttn_li[i]]
        if debug==True:
            print('iter= %d, %s sequences= %d'%(i,pttn_li[i],len(pttn_tbl)))
        for j in range(0,len(pttn_tbl)):
            if j==0:            
                fa='>'+pttn_tbl[j][1]+'_'+str(j)+'\n'+pttn_tbl[j][8]
            else:
                fa1='>'+pttn_tbl[j][1]+'_'+str(j)+'\n'+pttn_tbl[j][8]
                fa = fa+fa1
        
        # write txt file for every edited fasta
        with open(dir_PATH+'\\'+out_dir+'\\'+pttn_li[i]+'_Total.txt','w') as f:
            f.write(fa)
        if debug==True: print('file written done.')
    print('3. file written process done.\n')
    return()
# %%
fimo2logo('\\160513_intergenic_SCPD\\fimo_scpd.tsv','160513_intergenic_qv_5_logo',qv_thr=0.05)
fimo2logo('\\160513_intergenic_SwissRegulon\\fimo_swissreg.tsv','160513_intergenic_qv_5_logo',qv_thr=0.05)
fimo2logo('\\160513_intergenic_UniPROBE\\fimo_uniprobe.tsv','160513_intergenic_qval5_logo',qv_thr=0.05)
fimo2logo('\\160513_intergenic_YEASTRACT\\fimo_yeastract.tsv','160513_intergenic_qval5_logo',qv_thr=0.05)