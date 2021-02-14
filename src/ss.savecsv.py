# 2016-05-17
# Save out as csv file
import csv
def savecsv(data,name='pyout.csv',dir='C:/Users/KimSS/Desktop/',debug=False):
    #path = 'C:/Users/KimSS/Desktop/Py_output/ # Work PC
    #path = 'C:/Users/kisud/Desktop/Py_output/ # Home PC
    path = dir+name
    print('\n'+path)
    with open(path,'w',newline='') as f:
        wr = csv.writer(f)
        wr.writerows(data)
	
# %%
savecsv(out,name='py_output/160509_SGDids.csv')


# 2016-05-17
# Save out as txt file
def savetxt(data,name='pyout.csv',dir='C:/Users/KimSS/Desktop/',debug=False):
    #path = 'C:/Users/KimSS/Desktop/Py_output/ # Work PC
    #path = 'C:/Users/kisud/Desktop/Py_output/ # Home PC
    path = dir+name
    print('\n'+path)
    with open(path,'w') as f:
        for row in data:
            f.write(row)
	
# %%
savetxt(result,name='py_output/160517_JASPAR_CORE_2016_YEAST.meme')