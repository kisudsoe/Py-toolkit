# %%
## 2016-11-10 THU_function used for Yeast dynamic network
## function for extracting TF names from db files
import os.path
def meme2name(dir_path,dbfile_li,db_li):
    motif_s = []
    print('>> Read meme files')
    for i in range(0,len(dbfile_li)):
        PATH = dir_path+'\\'+dbfile_li[i]
        meme_f = open(PATH,'r')
        meme_fc = meme_f.readlines()
        meme_f.close()

        motif = [row for row in meme_fc if row.find('MOTIF')==0]

        for j in range(0,len(motif)):
            row1 = []
            items = motif[j].split(' ')
            row1.append(db_li[i]+'_'+items[1])
            row1.extend(items[1:len(items)])
            motif_s.append(row1)

    motif_out = ['ID','DBID','NAME','col1','col2','col3']
    motif_out = motif_out[0:len(row1)]
    motif_out = ['\t'.join(motif_out),'\n']
    motif_out = ''.join(motif_out)
    for row in motif_s:
        motif_row = '\t'.join(row)
        motif_out = ''.join([motif_out,motif_row])
    #motif_out = ''.join(motif_out)
    #print(motif_out)
    NAME = 'meme2name.tsv'
    with open(dir_path+'\\'+NAME,'w') as f:
        f.write(motif_out)
        print('>> %s written done.' % NAME)

# %%
dir_path = 'D:\\KimSS-NAS\\LFG\\Works\\2016.09 Yeast dynamic network\\(Archive) FIMO analysis'
dbfile_li = ['JASPAR_CORE_2016_YEAST.meme',
             'scpd_matrix.meme',
             'SwissRegulon_s_cer.meme',
             'yeast_uniprobe_GR09.meme',
             'YEASTRACT_20130918.meme']
db_li = ['JASPAR','SCPD','SwissRegulon','UniPROBE','YEASTRACT']
meme2name(dir_path,dbfile_li,db_li)
