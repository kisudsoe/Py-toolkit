# -*- coding: utf-8 -*-
"""
Created on Mon May  8 23:16:01 2017

@author: kisud
"""
# %%
from pygoogle import pygoogle
g = pygoogle('안암 맛집')
g.pages = 5
print ('*Found %s results*'%(g.get_result_count()))
g.get_urls()

# %%
from xml.etree import ElementTree