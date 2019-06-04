#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy,matplotlib,aplpy
from general_functions import *
import matplotlib.pyplot as plt


# In[ ]:


font = {'size'   : 14, 'family' : 'serif', 'serif' : 'cm'}
plt.rc('font', **font)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['lines.linewidth'] = 1
plt.rcParams['axes.linewidth'] = 1

#Set to true to save pdf versions of figures
save_figs = False


# The files used to make the following plot are:

# In[ ]:


r_image_decals = 'HCG16_DECaLS_r_cutout.fits'
grz_image_decals = 'HCG16_DECaLS_cutout.jpeg'


# 1. An $r$-band DECaLS fits image of HCG 16.
# 2. A combined $grz$ jpeg image from DECaLS covering exactly the same field.
# 
# These files were downloaded directly from the [DECaLS public website](http://legacysurvey.org/). The exact parameters defining the region and pixel size of these images is contained in the [pipeline.yml](pipeline.yml) file.

# In[ ]:


#Create aplpy figure using the co-ordinate system defined in fits image
f = aplpy.FITSFigure(r_image_decals,figsize=(10,10),dimensions=[0,1])

#Display the jpeg grz image that covers the same field as the fits image
f.show_rgb(grz_image_decals)

#Re-centre and set size
f.recenter(32.45, -10.225, radius=0.2)

#Add gridlines
f.add_grid()
f.grid.set_color('black')

#Add label for each galaxy
f.add_label(32.28,-10.325,'PGC 8210',horizontalalignment='right',color='yellow',weight='bold')
f.add_label(32.55,-10.3225,'NGC 848',horizontalalignment='left',color='yellow',weight='bold')
f.add_label(32.385,-10.115,'HCG 16a',horizontalalignment='left',color='yellow',weight='bold')
f.add_label(32.315,-10.138,'HCG 16b',horizontalalignment='left',color='yellow',weight='bold')
f.add_label(32.43,-10.147,'HCG 16c',horizontalalignment='right',color='yellow',weight='bold')
f.add_label(32.443,-10.2,'HCG 16d',horizontalalignment='left',color='yellow',weight='bold')

#Add scalebar
length = 100 #kpc
f.add_scalebar((180./numpy.pi)*length/(dist*1000.), label=str(length)+" kpc", color='w')

#Save
if save_figs:
    f.savefig('Fig1-HCG16_DECaLS_image.pdf')

