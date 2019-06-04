#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib,aplpy
from astropy.wcs import WCS
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
save_figs = False


# The files used to make the following plot are:

# In[ ]:


moment0_casa = 'HCG16_CD_rob2_MS.mom0.pbcor.fits'
moment0_sofia = 'HCG16_CD_rob2_MS_mom0.fits'
r_image_decals = 'HCG16_DECaLS_r_cutout.fits'


# 1. A moment 0 map of HCG 16 generated using a simple $3\sigma$ threshold in each channel (made with CASA). This file was generated in the *imaging* step of the workflow, which is described in the script [imaging.py](casa/imaging.py).
# 2. A moment 0 map of HCG 16 generated using $3.5\sigma$ mask made with SoFiA after smoothing over various kernel sizes. This file was generated in the *masking* step of the workflow. The SoFiA parameters file which makes this files is [HCG16_CD_rob2_MS.3.5s.dil.session](sofia/HCG16_CD_rob2_MS.3.5s.dil.session).
# 3. An $r$-band DECaLS fits image of HCG 16. This file was downloaded directly from the [DECaLS public website](http://legacysurvey.org/). The exact parameters defining the region and pixel size of this images is contained in the [pipeline.yml](pipeline.yml) file.

# In[ ]:


#Initialise figure
fig = plt.figure(figsize=(2.*8.27,2.*3))

#Make subplots for moment 0, colour bar, and r-band image width HI contours
ax1 = plt.subplot2grid((1, 36), (0, 0), colspan=13)
ax2 = plt.subplot2grid((1, 36), (0, 14), colspan=1)
ax3 = plt.subplot2grid((1, 36), (0, 22), colspan=13)

#Remove axis tickets (aplpy win make its own)
ax1.set_yticks([])
ax1.set_xticks([])
ax2.set_yticks([])
ax2.set_xticks([])
ax3.set_yticks([])
ax3.set_xticks([])

#Make CASA moment 0 plot
mom0 = aplpy.FITSFigure(moment0_casa, figure=fig, subplot=list(ax1.get_position(fig).bounds), slices=[0,0])

#Add arrows labelling features
mom0.show_arrows([32.5650,32.4848,32.3674,32.4498,32.5119,32.5367],
              [-10.3841,-10.3197,-10.1808,-10.0575,-10.1530,-10.2141],
              [0.0407,0.0248,0.0079,-0.0260,-0.0362,-0.0350],
              [0.0212,0.0512,0.0389,-0.0433,-0.0189,0.0011],color='k',width=0.5)

mom0.add_label(32.5630,-10.3841,'NGC848S tail',horizontalalignment='left')
mom0.add_label(32.4828,-10.3197,'SE tail',horizontalalignment='left')
mom0.add_label(32.3654,-10.1808,'NW tail',horizontalalignment='left')
mom0.add_label(32.4538,-10.0575,'NE tail',horizontalalignment='right')
mom0.add_label(32.5139,-10.1530,'E clump',horizontalalignment='right')
mom0.add_label(32.5387,-10.2141,'S clump',horizontalalignment='right')

#Re-centre and set size
mom0.recenter(32.45, -10.225, radius=0.2)

#Set colour map for moment 0
viridis_cmap = plt.cm.viridis_r
viridis_cmap.set_under(color='w')

#Add beam ellipse
mom0.add_beam()
mom0.beam.set_color('k')
mom0.beam.set_corner('bottom right')

#Display the data with the chosen colour map
mom0.show_colorscale(cmap=viridis_cmap,vmin=1E-6,vmax=1.,interpolation='none')

#Add gridlines
mom0.add_grid()
mom0.grid.set_color('black')
mom0.grid.set_alpha(0.25)

#Show GBT pointing centre
mom0.show_markers(32.3804, -10.15833,marker='x',c='r')


#Make the colourbar
cbar = matplotlib.colorbar.ColorbarBase(ax2, cmap=viridis_cmap,orientation='vertical',label='Flux [Jy km/s per beam]')


#Make r-band image plot
overlay = aplpy.FITSFigure(r_image_decals, figure=fig, subplot=list(ax3.get_position(fig).bounds), dimensions=[0, 1])

#Re-centre and set size (identical to above command)
overlay.recenter(32.45, -10.225, radius=0.2)

#Add contours of the SoFiA moment 0 map
#Aplpy cannot read the SoFiA-generated header (but astropy can) so some tricks are required
hdu = fits.open(moment0_sofia)
wcs = WCS(hdu[0].header,naxis=2)
data = hdu[0].data
hdu = fits.PrimaryHDU(data)
hdu.header.update(wcs.to_header())
overlay.show_contour(hdu,
               colors='r',levels=[-0.025,0.025,0.1,0.25,0.5,0.75,1.])
#Contour values in Jy km/s per beam

#Display r-band image
overlay.show_colorscale(cmap='Greys',vmin=0.0001,vmax=5.,stretch='log')

#Add gridlines
overlay.add_grid()
overlay.grid.set_color('black')

#Save
if save_figs:
    fig.savefig('Fig2-HCG16_mom0+DECaLS_overlay.pdf',bbox_inches='tight')

