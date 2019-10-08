#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib,aplpy
from astropy.io import fits
from general_functions import *
import matplotlib.pyplot as plt


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
obj_list = ['NW_clump','E_clump','S_clump']
#+'_mom0th.fits' or +'_mom1st.fits'


# 1. An $r$-band DECaLS fits image of HCG 16.
# 2. A combined $grz$ jpeg image from DECaLS covering exactly the same field.
# 
# These files were downloaded directly from the [DECaLS public website](http://legacysurvey.org/). The exact parameters defining the region and pixel size of these images is contained in the [pipeline.yml](pipeline.yml) file.
# 
# 3. Moment 0 and 1 maps of each candidate tidal dwarf galaxy.
# 
# The moment 0 and 1 maps of the galaxies were generated in the *imaging* step of the workflow using CASA. The exact steps are included in the [imaging.py](casa/imaging.py) script. The masks used to make these moment maps were constructed manually using the [SlicerAstro](http://github.com/Punzo/SlicerAstro) software package. They were downloaded along with the raw data from the EUDAT service [B2SHARE](http://b2share.eudat.eu) at the beginnning of the workflow execution. The exact location of the data are given in the [pipeline.yml](pipeline.yml) file.

# Make moment 0 contour overlays and moment 1 maps.

# In[ ]:


#Initialise figure using DECaLS r-band image
f = aplpy.FITSFigure(r_image_decals,figsize=(6.,4.3),dimensions=[0,1])

#Display DECaLS grz image
f.show_rgb(grz_image_decals)

#Recentre and resize
f.recenter(32.356,  -10.125, radius=1.5/60.)

#Overlay HI contours
f.show_contour(data='NW_clump'+'_mom0th.fits',dimensions=[0,1],slices=[0],
               colors='lime',levels=numpy.arange(0.1,5.,0.05))

#Add grid lines
f.add_grid()
f.grid.set_color('black')

#Save
if save_figs:
    plt.savefig('Fig15-NW_clump_mom0_cont.pdf')


# In[ ]:


#Clip the moment 1 map
mask_mom1(gal='NW_clump',level=0.1)

#Initialise figure for clipped map
f = aplpy.FITSFigure('tmp.fits',figsize=(6.,4.3),dimensions=[0,1])

#Recentre and resize
f.recenter(32.356,  -10.125, radius=1.5/60.)

#Set colourbar scale
f.show_colorscale(cmap='jet',vmin=3530.,vmax=3580.)

#Add grid lines
f.add_grid()
f.grid.set_color('black')

#Show and label colourbar 
f.add_colorbar()
f.colorbar.set_axis_label_text('$V_\mathrm{opt}$ [km/s]')

#Add beam ellipse
f.add_beam()
f.beam.set_color('k')
f.beam.set_corner('bottom right')

#Save
if save_figs:
    plt.savefig('Fig15-NW_clump_mom1.pdf')


# In[ ]:


#Initialise figure using DECaLS r-band image
f = aplpy.FITSFigure(r_image_decals,figsize=(6.,4.3),dimensions=[0,1])

#Display DECaLS grz image
f.show_rgb(grz_image_decals)

#Recentre and resize
f.recenter(32.463,  -10.181, radius=1.5/60.)

#Overlay HI contours
f.show_contour(data='E_clump'+'_mom0th.fits',dimensions=[0,1],slices=[0],
               colors='lime',levels=numpy.arange(0.1,5.,0.05))

#Add grid lines
f.add_grid()
f.grid.set_color('black')

#Save
if save_figs:
    plt.savefig('Fig15-E_clump_mom0_cont.pdf')


# In[ ]:


#Clip the moment 1 map
mask_mom1(gal='E_clump',level=0.1)

#Initialise figure for clipped map
f = aplpy.FITSFigure('tmp.fits',figsize=(6.,4.3),dimensions=[0,1])

#Recentre and resize
f.recenter(32.463,  -10.181, radius=1.5/60.)

#Set colourbar scale
f.show_colorscale(cmap='jet',vmin=3875.,vmax=3925.)

#Add grid lines
f.add_grid()
f.grid.set_color('black')

#Show and label colourbar 
f.add_colorbar()
f.colorbar.set_axis_label_text('$V_\mathrm{opt}$ [km/s]')

#Add beam ellipse
f.add_beam()
f.beam.set_color('k')
f.beam.set_corner('bottom right')

#Save
if save_figs:
    plt.savefig('Fig15-E_clump_mom1.pdf')


# In[ ]:


#Initialise figure using DECaLS r-band image
f = aplpy.FITSFigure(r_image_decals,figsize=(6.,4.3),dimensions=[0,1])

#Display DECaLS grz image
f.show_rgb(grz_image_decals)

#Recentre and resize
f.recenter(32.475,  -10.215, radius=1.5/60.)

#Overlay HI contours
f.show_contour(data='S_clump'+'_mom0th.fits',dimensions=[0,1],slices=[0],
               colors='lime',levels=numpy.arange(0.1,5.,0.05))

#Add grid lines
f.add_grid()
f.grid.set_color('black')

#Save
if save_figs:
    plt.savefig('Fig15-S_clump_mom0_cont.pdf')


# In[ ]:


#Clip the moment 1 map
mask_mom1(gal='S_clump',level=0.1)

#Initialise figure for clipped map
f = aplpy.FITSFigure('tmp.fits',figsize=(6.,4.3),dimensions=[0,1])

#Recentre and resize
f.recenter(32.475,  -10.215, radius=1.5/60.)

#Set colourbar scale
f.show_colorscale(cmap='jet',vmin=4050.,vmax=4100.)

#Add grid lines
f.add_grid()
f.grid.set_color('black')

#Show and label colourbar 
f.add_colorbar()
f.colorbar.set_axis_label_text('$V_\mathrm{opt}$ [km/s]')

#Add beam ellipse
f.add_beam()
f.beam.set_color('k')
f.beam.set_corner('bottom right')

#Save
if save_figs:
    plt.savefig('Fig15-S_clump_mom1.pdf')

