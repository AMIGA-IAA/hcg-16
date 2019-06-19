#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy,matplotlib
from astropy.io import fits
from general_functions import *
import matplotlib.pyplot as plt


# In[2]:


font = {'size'   : 14, 'family' : 'serif', 'serif' : 'cm'}
plt.rc('font', **font)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['lines.linewidth'] = 1
plt.rcParams['axes.linewidth'] = 1

#Set to true to save pdf versions of figures
save_figs = False


# In[ ]:




