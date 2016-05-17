# 2016-01-28 THU
# Debug listin function
## get clipboard data
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
data = listIn()