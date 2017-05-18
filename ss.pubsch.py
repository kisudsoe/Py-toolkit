# -*- coding: utf-8 -*-
"""
2016-05-22 SUN v1.1
@author: KimSS

v1.1  - 160522, bug fix and edit structure
v1.0  - 160131, first release
v1.0a - 170517, conda install biopython
"""

# %%
# !pip install biopython
# `conda install biopython` in authorized cmd
# Get pubmed ids from search terms
from Bio import Entrez # just one-time
def getids(term,retmax=100,debug=False):
    Entrez.email="kisudsoe@gmail.com" # always tell NCBI who I am
    sepbar = '-'*30
    handle = Entrez.esearch(db="pubmed",term=term,
                            retmax=retmax)
    record = Entrez.read(handle)
    #if(debug==True): print(record)
    idlist = record["IdList"]
    print('Search result has %d PMID(s).' % len(idlist))
    if debug==True:
        print(sepbar)
        print(idlist)
    return(idlist)

# Load JCR2014.csv
import os.path
def getjcr(where,debug=False):
    #dir = 'D:\\KimSS-NAS\\LFG_etc\\Works_Personal\\Project_Informatics tools\\SSSearch'
    if where=='work': pre = 'D:\\KimSS-NAS\\'
    elif where=='home': pre = 'E:\\KSS-Cloud\\'
    elif where=='tab': pre = 'D:\\KimSS-Cloud\\'
    else :
        print('Please input where you are (home/tab/work)')
        return()
    dir = pre+'LFG_etc\\Works_Personal\\Project_Informatics tools\\SSSearch'
    dbname = "JCR2015.csv"
    PATH = dir+'\\'+dbname
    db_f = open(PATH,'r')
    db_fc = db_f.readlines()
    db_f.close()
    if debug==True: print(db_fc[0:2])

    db_list=[]
    for i in range(0,len(db_fc)):
        db_rows = db_fc[i].split(',') # split by comma
        db_list.append(db_rows)
    print('Scanned JCR db -> columns= %d, rows= %d'
    % (len(db_list[1]),len(db_list)))
    return(db_list)

# Get article information from Pubmed
import time
# `conda install tqdm` in authorized PowerShell
from tqdm import *
from Bio import Medline
def getabs(ids,db_list,debug=False):
    # 1. Get Abstract from Pubmed DB
    start_time = time.time()
    Entrez.email="kisudsoe@gmail.com" # always tell NCBI who I am
    handle = Entrez.efetch(db="pubmed", id=ids,
                         rettype="medline",
                         retmode="text")
    if debug==True:
        handle2 = Entrez.efetch(db="pubmed", id=ids,
                               rettype="medline",
                               retmode="text")
        medl = handle2.read() # Read as plain text
        print(medl)
    record = Medline.parse(handle) # records is an iterator
    records = list(record) # to save the record
    handle.close()
    print("\n\nSearch result has %d abstract(s)."%len(records))
    print(">> Pubmed request : %.1f seconds.\n" % (time.time()-start_time))

    # 2. Make output text
    sep = "\n"
    out = []
    n = len(records)
    i = 0
    j = 0
    for rec in tqdm(records[0:n]):
        JT = rec.get("JT") # get Journal Name
        if not JT: JT="---" # bugfix 160210
        TA = rec.get("TA") # get Journal Abb.
        if not TA: TA="---" # bugfix 160210
        AU_li = rec.get("AU") # get Author list
        if not AU_li: AU_li="---" # bugfix 160216
        AU = []
        AU.append(', '.join(AU_li))
        DP = rec.get("DP")
        if not DP: DP="---" # bugfix 160216
        DP_li = DP.split(" ") # get Publication Date
        pmid = rec.get("PMID") # get pmid
        SO = rec.get("SO") # get publication info.
        AB = rec.get("AB") # get abstract
        if not AB: AB="---" # bugfix 160210
        if not SO: SO="---" # bugfix 160210
        ## 3-1. Get JCR2014 info
        IS_li=str(rec.get("IS"))
        if len(IS_li)==0: IS_li=['---'] # bugfix 160204
        else: IS_li=IS_li.split(' ')
        if len(IS_li)>2:
            IS = IS_li[2]
            jcr_row = [row for row in db_list if row[0]==IS_li[2]]
            if len(jcr_row)==0:
                IS = IS_li[0]
                jcr_row = [row for row in db_list if row[0]==IS]
        else: IS = IS_li[0]
        jcr_row = [row for row in db_list if row[0]==IS]
        ## 2-2. Concatenate info
        if len(jcr_row)==0:
            jcr = ['---']
            IS_str = []
            IS_str.append(''.join(IS_li))
            str_list = [jcr[0],'\t',DP_li[0],'_',TA,' (',pmid,')',sep]
            i += 1
            if debug==True: print('%d. %s %s %s'%(i,pmid,JT,IS_str))
        else:
            jcr_str = [jcr_row[0][1],' (',jcr_row[0][3],', ',
                       jcr_row[0][2],'), ',jcr_row[0][4],' rank in ',jcr_row[0][5]]
            jcr = []
            jcr.append(''.join(jcr_str))
            str_list = [jcr_row[0][3],'\t',DP_li[0],'_',TA,' (',pmid,')',sep]
        str_add=[rec.get("TI"),sep,sep,AU[0],sep,sep,
                        AB,sep,sep,
                        DP_li[0],'_',AU_li[0],'_',TA,'_',pmid,sep,
                        SO,sep,
                        jcr[0]]
        for item in str_add:
            str_list.append(str(item)) # bugfix 160223
        out.append(''.join(str_list))

        if debug==True: print('j= %d'%j)
        if j==0: YR0 = DP_li[0]
        if j==n-1: YR1 = DP_li[0]
        j += 1

    if i==0: print("All items were matched from JCR DB!")
    else: print(">> %d/%d items couldn't match from JCR DB.."%(i,n))
    print(">> Search result has abstracts ranged from %s to %s."%(YR1,YR0))
    print("\nProcess done.")
    if debug==True: print(out[0])
    return(out)

# Get article as reference format
def getref(form,term,retmax=20):
    ids = getids(term,retmax)
    if len(ids)==0:
        print('Nothing to search. Please retry with other term.')
        return()
    Entrez.email="kisudsoe@gmail.com" # always tell NCBI who I am
    handle = Entrez.efetch(db="pubmed", id=ids,
                         rettype="medline",
                         retmode="text")
    record = Medline.parse(handle) # records is an iterator
    records = list(record) # to save the record
    handle.close()
    print("Search result has %d reference(s).\n"%len(records))

    out = []
    for rec in tqdm(records):
        if form=="long":
            AU_li = rec.get("AU") # get Author list
            if len(AU_li)>1: AU = AU_li[0]+' et al.'
            else: AU = AU_li[0]+'.'
            TI = rec.get("TI") # get title of article
            SO = []
            SO_li = rec.get("SO").split('. ') # get publication info.
            SO.append('. '.join(SO_li[0:2]))
            SO = SO[0]+'.'
            PMID = rec.get("PMID") # get pmid
            str_li = [AU,' ',TI,' ',SO,' PMID ',PMID]
            out.append(''.join(str_li))
        elif form=="short":
            AU = rec.get("AU")[0] # get Author list
            DP = rec.get("DP")
            if not DP: DP="---" # bugfix 160216
            DP_li = DP.split(" ")[0] # get Publication Date
            PMID = rec.get("PMID") # get pmid
            str_li = [AU,DP_li,PMID]
            out.append(' '.join(str_li))
        elif form=="doku":
            AU_li = rec.get("AU") # get Author list
            if len(AU_li)>1: AU = AU_li[0]+' et al.'
            else: AU = AU_li[0]+'.'
            DP = rec.get("DP")
            if not DP: DP="---" # bugfix 160216
            DP_li = DP.split(" ")[0] # get Publication Date
            PMID = rec.get("PMID") # get pmid
            link = 'http://www.ncbi.nlm.nih.gov/pubmed/'+PMID
            TI = rec.get("TI") # get title of article
            str_li = ['[[',link,'|',AU,' ',DP_li,']] **',TI,'**']
            out.append(''.join(str_li))
        else:
            print("Please input form either 'long' or 'short'.")
    return(out)

# Execute : getids and getabs
def pubsch(term,db_fc,retmax=100):
    prompt = '> '

    if term:
        ids = getids(term,retmax)
    else: print('Please input search term')

    if len(ids)>100:
        print('Do you want to search abstracts? (y/n)')
        sch = input(prompt)
    elif len(ids)==0:
        print('Please input another search term')
        return()
    else:
        sch='y'

    if sch=='y':
        out = getabs(ids,db_fc)
        return(out)
    elif sch=='n':
        print("Function terminated.")
        return()
    else:
        print("You typed '%s'. Pleast input right character.\nThe pmid length is %d. Do you want to search abstracts? (y/n)"%(sch,len(ids)))
        sch = input(prompt)

# 160211 filter by impact factor : abstracts
def filt_if(abstract,ifac=10):
    ifac_li = []
    out = []
    i = 0
    for item in abstract:
        im_fac = item.split('\t')[0]
        if im_fac=='---': im_fac = 0
        elif im_fac=='-': im_fac = 0 # bugfix 160223
        elif im_fac=='Not Available': im_fac = 0 # bugfix 160806

        if float(im_fac)>=float(ifac): ifac_li.append(i) # filter
        i += 1
    for item in ifac_li:
        out.append(abstract[int(item)])
    print('IF filtered item length= %d' %len(out))
    return(out)

def filt_yr(abstract,year=2011):
    yr_li = []
    out = []
    i = 0
    for item in abstract:
        yr = item.split('_')[0].split('\t')[1].split('-')[0]
        if int(yr)>=int(year): yr_li.append(i)
        i += 1
    for item in yr_li:
        out.append(abstract[int(item)])
    print('Yr filtered item length= %d' %len(out))
    return(out)

import webbrowser
def openurl(pmid):
    url = "http://www.ncbi.nlm.nih.gov/pubmed/"+pmid
    webbrowser.open(url,new=2)

# GUI format v0.1
import sys
from PyQt5.QtWidgets import *
class RefUI(QMainWindow):
    def __init__(self):
        #QMainWindow.__init__(self, parent)
        super(RefUI, self).__init__()
        self.create_ui()

    def create_ui(self):
        out = []
        out.append('\n\n\n'.join(ref))
        print()

        self.text = QtGui.QTextEdit(self)
        self.text.setText(out[0])
        self.setCentralWidget(self.text)

        # x and y coordinates on the screen, width, height
        if len(out[0])<400: self.setGeometry(30,300,550,150)
        else: self.setGeometry(30,300,550,600)
        self.setWindowTitle("Get Reference")

def refui(ref):
    app = QApplication(sys.argv)
    form = RefUI()
    form.show()
    app.exec_()

#if __name__ == "__main__":
#   refui()

# Initiate functions
db_jcr = getjcr('work') # work/home/tab
# %% Search papers using terms
a = 'mouse liver Kdm5b'
abst = pubsch(a,db_jcr,1000)
abst_if15 = filt_if(abst,15)
abst_yr14 = filt_yr(abst,2014)
abst_yr14_if15 = filt_if(abst_yr14,15)

print('\n***********************\n'.join(abst[0:20]))
# %% Get abstract using PMID
a2 = "17264674"
#ref = pubsch("work",a2) # (work/home/tab, term/pmid)
ref = getabs(a2,db_jcr)
print(ref[0])
openurl(a2)
#refui(ref)
# %% Reference information
ref = getref("long","22935518") # (long/short/doku, term/pmid)
print(ref[0])
#refui(ref)
