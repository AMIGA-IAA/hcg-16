#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib,aplpy
from astropy.io import fits
from general_functions import *
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS


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


cube_rob0_casa = 'HCG16_CD_rob0_MS.pbcor.fits'


# 1. The primary beam corrected, multi-scale CLEAN HI robust=0 cube generated in the *imaging* step using CASA. The script [imaging.py](casa/imaging.py) contains the commands used to generate it. This cube has better resolution (but worse sensitivity) than the robust=2 cube used for the rest of the analysis.

# Read in the cube.

# In[ ]:


cube,cube_ra,cube_dec,cube_vel,bmaj,bmin,pa,beam_factor = read_fitscube(cube_rob0_casa,need_beam=True)


# Generate the spectral profile at the centre of HCG 16d by weight the pixels with a 2D Gaussian with the demensions of the beam.

# In[ ]:


#Create empyt weights array
pix_wts = numpy.zeros(numpy.shape(cube[0]))

#Calculate the separations in the x and y directions
#Then weight with a 2D Gaussian
for i in range(len(cube_ra)):
    for j in range(len(cube_dec)):
        dec_sep = cube_dec[j]-dec_hcg16d
        ra_sep = (cube_ra[i]-ra_hcg16d)*numpy.cos((cube_dec[j]+dec_hcg16d)*numpy.pi/360.)
        
        #Calculate weights
        pix_wts[j][i] = gaussian2d(ra_sep,dec_sep,0.,0.,bmin/(2.3548*3600.),bmaj/(2.3548*3600.))
        
#Apply pixel weights to the cube
for i in range(len(cube_vel)):
    cube[i] = cube[i]*pix_wts

#Make spectral profile
absorp_spec = 1000.*numpy.nansum(numpy.nansum(cube,axis=1),axis=1)/beam_factor


# In[ ]:


#Initialise figure
fig = plt.subplots(figsize=(8.27,4.))

#Plot the spectrum
plt.step(cube_vel,absorp_spec,where='mid',c='k')

#Add dashed line showing redshift of optical emission lines
plt.axvline(v_hcg16d,c='k',ls='dashed')
plt.axhline(0.,c='k')

#Label axes
plt.xlabel(r'$v_\mathrm{opt}$ [km/s]')
plt.ylabel('Flux Density [mJy]')

#Set axes limits
plt.xlim(3600.,4300.)
plt.ylim(-1.6,1.6)

#Save
if save_figs:
    plt.savefig('Fig12-HCG16d_absorption_spec.pdf',bbox_inches='tight')

