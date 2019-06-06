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
save_figs = True


# The file used to make the following plot is:

# In[ ]:


moment1_sofia = 'HCG16_CD_rob2_MS_ht_mom1.fits'


# 1. A moment 1 map of HCG 16 generated using $5\sigma$ mask made with SoFiA after smoothing over various kernel sizes. This file was generated in the *masking* step of the workflow. The SoFiA parameters file which makes this files is [HCG16_CD_rob2_MS.5.0s.nodil.session](sofia/HCG16_CD_rob2_MS.5.0s.nodil.session).

# In[ ]:


#Initialise figure
fig = plt.figure(figsize=(8.27,2.*3))

#Make axes for plot and colourbar
ax1 = plt.subplot2grid((1, 18), (0, 0), colspan=13)
ax2 = plt.subplot2grid((1, 18), (0, 14), colspan=1)

#Remove axis tickets (aplpy win make its own)
ax1.set_yticks([])
ax1.set_xticks([])
ax2.set_yticks([])
ax2.set_xticks([])

#Make moment 1 plot
#Some trickery is required to get aplpy to accept SoFiA-generated header
hdu = fits.open(moment1_sofia)
wcs = WCS(hdu[0].header,naxis=2)
data = hdu[0].data
bmaj,bmin,bpa = hdu[0].header['bmaj'],hdu[0].header['bmin'],hdu[0].header['bpa']
hdu = fits.PrimaryHDU(data)
hdu.header.update(wcs.to_header())
hdu.header['bmaj'],hdu.header['bmin'],hdu.header['bpa'] = bmaj,bmin,bpa
mom1 = aplpy.FITSFigure(hdu, figure=fig, subplot=list(ax1.get_position(fig).bounds))

#Re-centre and set size
mom1.recenter(32.45, -10.225, radius=0.2)

#Add star markers for the galaxy optical centres
mom1.show_markers(ra_hcg16a,dec_hcg16a,marker='*',c='k',s=50,label='HCG16a')
mom1.show_markers(ra_hcg16b,dec_hcg16b,marker='*',c='k',s=50,label='HCG16b')
mom1.show_markers(ra_hcg16c,dec_hcg16c,marker='*',c='k',s=50,label='HCG16c')
mom1.show_markers(ra_hcg16d,dec_hcg16d,marker='*',c='k',s=50,label='HCG16d')
mom1.show_markers(ra_hcg16n,dec_hcg16n,marker='*',c='k',s=50,label='NGC848')
mom1.show_markers(ra_hcg16p,dec_hcg16p,marker='*',c='k',s=50,label='PGC8210')

#Display the data with the chosen colour map
vel_max = 4050. #km/s
vel_min = 3700. #km/s
#These are radio velocities as that what CASA output to SoFiA
#The colourbar scale will be converted to optical velocity below
mom1.show_colorscale(cmap='jet',vmin=vel_min*1000.,vmax=vel_max*1000.)

#Add grid lines
mom1.add_grid()
mom1.grid.set_color('black')
mom1.grid.set_alpha(0.25)

#Add beam ellipse
mom1.add_beam()
mom1.beam.set_color('k')
mom1.beam.set_corner('bottom right')

#Make the colourbar
cmap = matplotlib.cm.jet
norm = matplotlib.colors.Normalize(vmin=v_opt(vel_min), vmax=v_opt(vel_max))
cbar = matplotlib.colorbar.ColorbarBase(ax2, cmap=cmap,norm=norm,orientation='vertical',label='$v_{opt}$ [km/s]')

#Save
if save_figs:
    fig.savefig('Fig3-HCG16_mom1.pdf',bbox_inches='tight')

