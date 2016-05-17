# 2016-05-17 TUE
## Make Jaspar extraction file
import os.path
from tqdm import *
def memeExt(id_list,file_name):
    dir_PATH = 'D:\\KimSS-NAS\\LFG\\Works\\2016.04 Yeast HD LD Rho0\\(Archive) FIMO analysis\\'
    PATH = dir_PATH+file_name
    
    # 1. Read file
    meme_f = open(PATH,'r')
    meme_fc = meme_f.readlines()
    meme_f.close()
    print('1. Read file done: %d lines' % (len(meme_fc)))
    
    # 2. Search motif information and their index
    motifs = [s for s in meme_fc if 'MOTIF'.lower() in s.lower()]
    motifs_id = [i for i, s in enumerate(meme_fc) if 'MOTIF'.lower() in s.lower()]
    print('2. Search motifs done: %d motifs\n' % (len(motifs_id)))
    
    # 3. Search id_list in motif list
    my_motifs_id = []
    for sch in tqdm(id_list):
        my_id = [i for i, s in enumerate(motifs) if sch.lower() in s.lower()]
        my_motifs_id.append(my_id)
    print('3. Extract my motifs done: %d motifs\n'% len(my_motifs_id))
    
    result = []
    for my in tqdm(my_motifs_id):
        if len(my)>0:
            my_motif = meme_fc[motifs_id[my[0]]:
                motifs_id[my[0]+1]-1]
            my_motif_str = ''.join(my_motif)
            result.append(my_motif_str)
    print('4. Summary my motifs done.%d motifs\n'% len(result))

    return(result)
    
# %%
#id_list = listIn() # import jaspar yeast list from SGD_annot
result = memeExt(id_list,'JASPAR_CORE_2016.meme')