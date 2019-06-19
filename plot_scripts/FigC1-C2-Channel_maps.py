#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib,aplpy
from astropy.io import fits
from general_functions import *
import matplotlib.pyplot as plt
from astropy.wcs import WCS


# In[ ]:


font = {'size'   : 14, 'family' : 'serif', 'serif' : 'cm'}
plt.rc('font', **font)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['lines.linewidth'] = 1
plt.rcParams['axes.linewidth'] = 1

#Set to true to save pdf versions of figures
save_figs = True


# The files used to make the following plot are:

# In[ ]:


r_image_decals = 'HCG16_DECaLS_r_cutout.fits'
grz_image_decals = 'HCG16_DECaLS_cutout.jpeg'
cube_casa = 'HCG16_CD_rob2_MS.pbcor.fits'


# 1. An $r$-band DECaLS fits image of HCG 16.
# 2. A combined $grz$ jpeg image from DECaLS covering exactly the same field.
# 
# These files were downloaded directly from the [DECaLS public website](http://legacysurvey.org/). The exact parameters defining the region and pixel size of these images is contained in the [pipeline.yml](pipeline.yml) file.
# 
# 3. The primary beam corrected, multi-scale CLEAN HI cube generated in the *imaging* step using CASA. The script [imaging.py](casa/imaging.py) contains the commands used to generate it.

# First make channel maps in the group centre.

# In[ ]:


#Load the cube
cube,cube_ra,cube_dec,cube_vel = read_fitscube(cube_casa)

#Make map for each channel
for i in range(len(cube_vel)):
    #Initialise background figure
    f = aplpy.FITSFigure(r_image_decals,figsize=(12,9),dimensions=[0,1])

    f.recenter(32.385,  -10.1584, height=9./60., width=12./60.)

    #Aplpy cannot properly read the header and slice the cube
    #So we have to read it with astropy and pass it to aplpy
    hdu = fits.open(cube_casa)
    wcs = WCS(hdu[0].header,naxis=2)
    data = hdu[0].data[i]
    hdu = fits.PrimaryHDU(data)
    hdu.header.update(wcs.to_header())
    
    #Overlay HI channel contours
    f.show_contour(hdu,
                   colors='r',levels=numpy.array([-2,2,4,6,8,10,12,14,16,18,20])*0.45E-3)

    #Set colour stretch of background image
    f.show_colorscale(cmap='Greys',vmin=0.0001,vmax=5.,stretch='log')
    
    #Add grid lines
    f.add_grid()
    f.grid.set_color('black')
    
    #Add velcoity label
    f.add_label(0.85,0.95,str(int(numpy.round(cube_vel[i],0)))+' km/s',horizontalalignment='left',
                relative='axes', color='r', size='large')

    #Save
    if save_figs:
        f.savefig(out_dir+'FigC1-HCG16_core_chnmap_'+str(i)+'.pdf')


# Now make channel maps near the SE tail.

# In[ ]:


#Load the cube
cube,cube_ra,cube_dec,cube_vel = read_fitscube(cube_casa)

#Make map for each channel
for i in range(len(cube_vel)):
    #Initialise background figure
    f = aplpy.FITSFigure(r_image_decals,figsize=(14,12),dimensions=[0,1])

    f.recenter(32.52,  -10.27, height=12./60., width=14./60.)

    #Aplpy cannot properly read the header and slice the cube
    #So we have to read it with astropy and pass it to aplpy
    hdu = fits.open(cube_casa)
    wcs = WCS(hdu[0].header,naxis=2)
    data = hdu[0].data[i]
    hdu = fits.PrimaryHDU(data)
    hdu.header.update(wcs.to_header())
    
    #Overlay HI channel contours
    f.show_contour(hdu,
                   colors='r',levels=numpy.array([-2,2,4,6,8,10,12,14,16,18,20])*0.45E-3)

    #Set colour stretch of background image
    f.show_colorscale(cmap='Greys',vmin=0.0001,vmax=5.,stretch='log')
    
    #Add grid lines
    f.add_grid()
    f.grid.set_color('black')
    
    #Add velcoity label
    f.add_label(0.85,0.05,str(int(numpy.round(cube_vel[i],0)))+' km/s',horizontalalignment='left',
                relative='axes', color='r', size='large')

    #Save
    if save_figs:
        f.savefig(out_dir+'FigC2-HCG16_tail_chnmap_'+str(i)+'.pdf')

