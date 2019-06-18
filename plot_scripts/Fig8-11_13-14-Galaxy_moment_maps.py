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


# The files used to make the following plot are:

# In[ ]:


r_image_decals = 'HCG16_DECaLS_r_cutout.fits'
grz_image_decals = 'HCG16_DECaLS_cutout.jpeg'
gal_list = ['HCG16a','HCG16b','HCG16c','HCG16d','NGC848','PGC8210']
#+'_mom0th.fits' or +'_mom1st.fits'


# 1. An $r$-band DECaLS fits image of HCG 16.
# 2. A combined $grz$ jpeg image from DECaLS covering exactly the same field.
# 
# These files were downloaded directly from the [DECaLS public website](http://legacysurvey.org/). The exact parameters defining the region and pixel size of these images is contained in the [pipeline.yml](pipeline.yml) file.
# 
# 3. Moment 0 and 1 maps of each galaxy.
# 
# The moment 0 and 1 maps of the galaxies were generated in the *imaging* step of the workflow using CASA. The exact steps are included in the [imaging.py](casa/imaging.py) script. The masks used to make these moment maps were constructed manually using the [SlicerAstro](github.com/Punzo/SlicerAstro) software package. They were downloaded along with the raw data from the EUDAT service [B2SHARE](b2share.eudat.eu) at the beginnning of the workflow execution. The exact location of the data are given in the [pipeline.yml](pipeline.yml) file.

# Make moment 0 maps.

# In[ ]:


#Initialise figure
f = aplpy.FITSFigure('HCG16a'+'_mom0th.fits',figsize=(8.27,2.*3),dimensions=[0,1])

#Recentre and set size
f.recenter(32.34583,  -10.1375, radius=2./60.)

#Add markers for the galaxies in the field
f.show_markers(ra_hcg16a,  dec_hcg16a,marker='*',c='w',s=100,label='HCG16a')
f.show_markers(ra_hcg16b,  dec_hcg16b,marker='*',c='k',s=100,label='HCG16b')

#Set colourbar and background colour
viridis_cmap = plt.cm.viridis_r
viridis_cmap.set_under(color='w')
f.show_colorscale(cmap=viridis_cmap,vmin=0.1,vmax=1.)

#Make grid lines
f.add_grid()
f.grid.set_color('black')

#Make and label colourbar
f.add_colorbar()
f.colorbar.set_axis_label_text('Flux [Jy km/s per beam]')

#Add beam
f.add_beam()
f.beam.set_color('k')
f.beam.set_corner('bottom right')

#Save
if save_figs:
    plt.savefig('Fig8-HCG16a_mom0.pdf',bbox_inches='tight')


# In[ ]:


#Initialise figure
f = aplpy.FITSFigure('HCG16b'+'_mom0th.fits',figsize=(8.27,2.*3),dimensions=[0,1])

#Recentre and set size
f.recenter(32.34583,  -10.1375, radius=2./60.)

#Add markers for the galaxies in the field
f.show_markers(ra_hcg16a,  dec_hcg16a,marker='*',c='k',s=100,label='HCG16a')
f.show_markers(ra_hcg16b,  dec_hcg16b,marker='*',c='k',s=100,label='HCG16b')

#Set colourbar and background colour
viridis_cmap = plt.cm.viridis_r
viridis_cmap.set_under(color='w')
f.show_colorscale(cmap=viridis_cmap,vmin=0.1,vmax=1.)

#Make grid lines
f.add_grid()
f.grid.set_color('black')

#Make and label colourbar
f.add_colorbar()
f.colorbar.set_axis_label_text('Flux [Jy km/s per beam]')

#Add beam
f.add_beam()
f.beam.set_color('k')
f.beam.set_corner('bottom right')

#Save
if save_figs:
    plt.savefig('Fig9-HCG16b_mom0.pdf',bbox_inches='tight')


# In[ ]:


#Initialise figure
f = aplpy.FITSFigure('HCG16c'+'_mom0th.fits',figsize=(8.27,2.*3),dimensions=[0,1])

#Recentre and set size
f.recenter(32.427083,  -10.16667, radius=2.5/60.)

#Add markers for the galaxies in the field
f.show_markers(ra_hcg16c,  dec_hcg16c,marker='*',c='w',s=100,label='HCG16c')
f.show_markers(ra_hcg16d,  dec_hcg16d,marker='*',c='k',s=100,label='HCG16d')

#Set colourbar and background colour
viridis_cmap = plt.cm.viridis_r
viridis_cmap.set_under(color='w')
f.show_colorscale(cmap=viridis_cmap,vmin=0.1,vmax=1.)

#Make grid lines
f.add_grid()
f.grid.set_color('black')

#Make and label colourbar
f.add_colorbar()
f.colorbar.set_axis_label_text('Flux [Jy km/s per beam]')

#Add beam
f.add_beam()
f.beam.set_color('k')
f.beam.set_corner('bottom right')

#Save
if save_figs:
    plt.savefig('Fig10-HCG16c_mom0.pdf',bbox_inches='tight')


# In[ ]:


#Initialise figure
f = aplpy.FITSFigure('HCG16d'+'_mom0th.fits',figsize=(8.27,2.*3),dimensions=[0,1])

#Recentre and set size
f.recenter(32.427083,  -10.16667, radius=3./60.)

#Add markers for the galaxies in the field
f.show_markers(ra_hcg16c,  dec_hcg16c,marker='*',c='k',s=100,label='HCG16c')
f.show_markers(ra_hcg16d,  dec_hcg16d,marker='*',c='w',s=100,label='HCG16d')

#Set colourbar and background colour
viridis_cmap = plt.cm.viridis_r
viridis_cmap.set_under(color='w')
f.show_colorscale(cmap=viridis_cmap,vmin=0.1,vmax=1.)

#Make grid lines
f.add_grid()
f.grid.set_color('black')

#Make and label colourbar
f.add_colorbar()
f.colorbar.set_axis_label_text('Flux [Jy km/s per beam]')

#Add beam
f.add_beam()
f.beam.set_color('k')
f.beam.set_corner('bottom right')

#Save
if save_figs:
    plt.savefig('Fig11-HCG16d_mom0.pdf',bbox_inches='tight')


# In[ ]:


#Initialise figure
f = aplpy.FITSFigure('NGC848'+'_mom0th.fits',figsize=(8.27,2.*3),dimensions=[0,1])

#Recentre and set size
f.recenter(32.56935,  -10.321447, radius=2./60.)

#Add markers for the galaxies in the field
f.show_markers(ra_hcg16n,  dec_hcg16n,marker='*',c='w',s=100,label='NGC848')

#Set colourbar and background colour
viridis_cmap = plt.cm.viridis_r
viridis_cmap.set_under(color='w')
f.show_colorscale(cmap=viridis_cmap,vmin=0.1,vmax=1.)

#Make grid lines
f.add_grid()
f.grid.set_color('black')

#Make and label colourbar
f.add_colorbar()
f.colorbar.set_axis_label_text('Flux [Jy km/s per beam]')

#Add beam
f.add_beam()
f.beam.set_color('k')
f.beam.set_corner('bottom right')

#Save
if save_figs:
    plt.savefig('Fig13-NGC848_mom0.pdf',bbox_inches='tight')


# In[ ]:


#Initialise figure
f = aplpy.FITSFigure('PGC8210'+'_mom0th.fits',figsize=(8.27,2.*3),dimensions=[0,1])

#Recentre and set size
f.recenter(32.275081,  -10.320226, radius=2./60.)

#Add markers for the galaxies in the field
f.show_markers(ra_hcg16p,  dec_hcg16p,marker='*',c='w',s=100,label='NGC848')

#Set colourbar and background colour
viridis_cmap = plt.cm.viridis_r
viridis_cmap.set_under(color='w')
f.show_colorscale(cmap=viridis_cmap,vmin=0.1,vmax=1.)

#Make grid lines
f.add_grid()
f.grid.set_color('black')

#Make and label colourbar
f.add_colorbar()
f.colorbar.set_axis_label_text('Flux [Jy km/s per beam]')

#Add beam
f.add_beam()
f.beam.set_color('k')
f.beam.set_corner('bottom right')

#Save
if save_figs:
    plt.savefig('Fig14-PGC8210_mom0.pdf',bbox_inches='tight')


# Make iso-velocity contour maps.

# In[ ]:


#Clip the moment 1 map
mask_mom1(gal='HCG16a',level=0.25)

#Use coordinate system from r-band image
f = aplpy.FITSFigure(r_image_decals,figsize=(8.27,2.*3),dimensions=[0,1])

#Show DECaLS grz image
f.show_rgb(grz_image_decals)

#Re-centre
f.recenter(32.34583,  -10.1375, radius=2./60.)

#Plot contours with a spacing of 20 km\s
f.show_contour(data='tmp.fits',dimensions=[0,1],slices=[0],
               colors='lime',levels=numpy.arange(3980.,4205.,20.))

#Add manual labels
f.add_label(32.356,-10.149,'3980',horizontalalignment='left',color='lime')
f.add_label(32.345,-10.139,'4000',horizontalalignment='left',color='lime')
f.add_label(32.360,-10.146,'4020',horizontalalignment='right',color='lime')
f.add_label(32.345,-10.134,'4040',horizontalalignment='left',color='lime')
f.add_label(32.362,-10.141,'4060',horizontalalignment='right',color='lime')
f.add_label(32.347,-10.130,'4080',horizontalalignment='left',color='lime')
f.add_label(32.363,-10.134,'4100',horizontalalignment='right',color='lime')
f.add_label(32.350,-10.126,'4120',horizontalalignment='left',color='lime')
f.add_label(32.361,-10.130,'4140',horizontalalignment='right',color='lime')

#Add grid lines
f.add_grid()
f.grid.set_color('black')

#Save
if save_figs:
    plt.savefig('Fig8-HCG16a_mom1_cont.pdf',bbox_inches='tight')


# In[ ]:


#Clip the moment 1 map
mask_mom1(gal='HCG16b',level=0.1)

#Use coordinate system from r-band image
f = aplpy.FITSFigure(r_image_decals,figsize=(8.27,2.*3),dimensions=[0,1])

#Show DECaLS grz image
f.show_rgb(grz_image_decals)

#Re-centre
f.recenter(32.34583,  -10.1375, radius=2./60.)

#Plot contours with a spacing of 20 km\s
f.show_contour(data='tmp.fits',dimensions=[0,1],slices=[0],
               colors='lime',levels=numpy.arange(3860.,4400.,20.))

#Add manual labels
f.add_label(32.332,-10.138,'3860',horizontalalignment='left',color='lime')
f.add_label(32.331,-10.128,'3880',horizontalalignment='left',color='lime')
f.add_label(32.337,-10.141,'3900',horizontalalignment='right',color='lime')
f.add_label(32.3345,-10.122,'3920',horizontalalignment='left',color='lime')
f.add_label(32.344,-10.122,'3940',horizontalalignment='right',color='lime')

#Add grid lines
f.add_grid()
f.grid.set_color('black')

#Save
if save_figs:
    plt.savefig('Fig9-HCG16b_mom1_cont.pdf',bbox_inches='tight')


# In[ ]:


#Clip the moment 1 map
mask_mom1(gal='HCG16c',level=0.25)

#Use coordinate system from r-band image
f = aplpy.FITSFigure(r_image_decals,figsize=(8.27,2.*3),dimensions=[0,1])

#Show DECaLS grz image
f.show_rgb(grz_image_decals)

#Re-centre
f.recenter(32.427083,  -10.16667, radius=2.5/60.)

#Plot contours with a spacing of 20 km\s
f.show_contour(data='tmp.fits',dimensions=[0,1],slices=[0],
               colors='lime',levels=numpy.arange(3760.,4400.,20.))

#Add manual labels
f.add_label(32.427,-10.157,'3760',horizontalalignment='right',color='lime')
f.add_label(32.422,-10.161,'3780',horizontalalignment='left',color='lime')
f.add_label(32.431,-10.151,'3800',horizontalalignment='right',color='lime')
f.add_label(32.412,-10.160,'3820',horizontalalignment='left',color='lime')
f.add_label(32.427,-10.141,'3840',horizontalalignment='right',color='lime')
f.add_label(32.420,-10.136,'3860',horizontalalignment='right',color='lime')
f.add_label(32.401,-10.152,'3880',horizontalalignment='left',color='lime')
f.add_label(32.400,-10.147,'3900',horizontalalignment='left',color='lime')
f.add_label(32.401,-10.143,'3920',horizontalalignment='left',color='lime')

#Add grid lines
f.add_grid()
f.grid.set_color('black')

#Save
if save_figs:
    plt.savefig('Fig10-HCG16c_mom1_cont.pdf',bbox_inches='tight')


# In[ ]:


#Clip the moment 1 map
mask_mom1(gal='HCG16d',level=0.25)

#Use coordinate system from r-band image
f = aplpy.FITSFigure(r_image_decals,figsize=(8.27,2.*3),dimensions=[0,1])

#Show DECaLS grz image
f.show_rgb(grz_image_decals)

#Re-centre
f.recenter(32.427083,  -10.16667, radius=3./60.)

#Remove pixels within one beam of the optical centre
mom1_fits = astropy.io.fits.open('tmp.fits')
mom1 = mom1_fits[0].data
mom1_head = mom1_fits[0].header
mom1_wcs = WCS(mom1_head,naxis=2)



#Plot contours with a spacing of 20 km\s
f.show_contour(data='tmp.fits',dimensions=[0,1],slices=[0],
               colors='lime',levels=numpy.arange(3900.,3945.,20.))

#Add manual labels
f.add_label(32.444,-10.203,'3900',horizontalalignment='right',color='lime')
f.add_label(32.445,-10.197,'3920',horizontalalignment='right',color='lime')
f.add_label(32.438,-10.172,'3900',horizontalalignment='left',color='lime')
f.add_label(32.443,-10.179,'3920',horizontalalignment='right',color='lime')
f.add_label(32.426,-10.168,'3920',horizontalalignment='right',color='lime')
f.add_label(32.417,-10.172,'3940',horizontalalignment='left',color='lime')

#Add grid lines
f.add_grid()
f.grid.set_color('black')

#Save
if save_figs:
    plt.savefig('Fig11-HCG16d_mom1_cont.pdf',bbox_inches='tight')


# Repeat the plot for HCG 16d with the central region blanked to avoid the HI absorption feature.

# In[ ]:


#Clip the moment 1 map
mask_mom1(gal='HCG16d',level=0.25)

#Remove pixels within one beam of the optical centre
#Define the optical centre 
HCG16d_cen = SkyCoord(ra_hcg16d, dec_hcg16d, frame='icrs', equinox='J2000', unit='deg')
#Read masked moment 1 file
mom1_fits = astropy.io.fits.open('tmp.fits')
mom1 = mom1_fits[0].data
mom1_head = mom1_fits[0].header
mom1_ra = mom1_head['CRVAL1'] + mom1_head['CDELT1'] * numpy.arange(1,1+mom1_head['NAXIS1']) - mom1_head['CDELT1'] * mom1_head['CRPIX1'] # RA
mom1_dec = mom1_head['CRVAL2'] + mom1_head['CDELT2'] * numpy.arange(1,1+mom1_head['NAXIS2']) - mom1_head['CDELT2'] * mom1_head['CRPIX2'] # Dec

#Calculate the beam response in every pixel
for i in range(mom1_head['NAXIS1']):
    #Define the pixel positions of a column of pixels in the WCS
    pix_pos = SkyCoord(numpy.repeat(mom1_ra[i],len(mom1_dec)), mom1_dec, frame='icrs', equinox='J2000', unit='deg')
    #Calculate the separations
    sep = HCG16d_cen.separation(pix_pos)
    #Blank sections within a beam width of the central source
    if min(sep.degree) < float(mom1_head['BMAJ']):
        for j in range(len(mom1_fits[0].data[i])):
            if sep.degree[j] < float(mom1_head['BMAJ']):
                mom1_fits[0].data[j][i] = numpy.nan

#Write the blanked moment 1 map to a temporary file
mom1_fits.writeto('tmp.fits',overwrite=True,output_verify='warn')


# In[ ]:


#Use coordinate system from r-band image
f = aplpy.FITSFigure(r_image_decals,figsize=(8.27,2.*3),dimensions=[0,1])

#Show DECaLS grz image
f.show_rgb(grz_image_decals)

#Re-centre
f.recenter(32.427083,  -10.16667, radius=3./60.)

#Remove pixels within one beam of the optical centre
mom1_fits = astropy.io.fits.open('tmp.fits')
mom1 = mom1_fits[0].data
mom1_head = mom1_fits[0].header
mom1_wcs = WCS(mom1_head,naxis=2)

#Plot contours with a spacing of 20 km\s
f.show_contour(data='tmp.fits',dimensions=[0,1],slices=[0],
               colors='lime',levels=numpy.arange(3900.,3945.,20.))

#Add manual labels
f.add_label(32.444,-10.203,'3900',horizontalalignment='right',color='lime')
f.add_label(32.445,-10.197,'3920',horizontalalignment='right',color='lime')
f.add_label(32.438,-10.172,'3900',horizontalalignment='left',color='lime')
f.add_label(32.443,-10.179,'3920',horizontalalignment='right',color='lime')
f.add_label(32.426,-10.168,'3920',horizontalalignment='right',color='lime')
f.add_label(32.417,-10.172,'3940',horizontalalignment='left',color='lime')

#Add grid lines
f.add_grid()
f.grid.set_color('black')

#Save
if save_figs:
    plt.savefig('Fig11-HCG16d_noabs_mom1_cont.pdf',bbox_inches='tight')


# In[ ]:


#Clip the moment 1 map
mask_mom1(gal='NGC848',level=0.25)

#Use coordinate system from r-band image
f = aplpy.FITSFigure(r_image_decals,figsize=(8.27,2.*3),dimensions=[0,1])

#Show DECaLS grz image
f.show_rgb(grz_image_decals)

#Re-centre
f.recenter(32.56935,  -10.321447, radius=2./60.)

#Plot contours with a spacing of 20 km\s
f.show_contour(data='tmp.fits',dimensions=[0,1],slices=[0],
               colors='lime',levels=numpy.arange(3940.,4085.,20.))

#Add manual labels
f.add_label(32.557,-10.304,'3940',horizontalalignment='left',color='lime')
f.add_label(32.557,-10.315,'3960',horizontalalignment='left',color='lime')
f.add_label(32.575,-10.309,'3980',horizontalalignment='right',color='lime')
f.add_label(32.565,-10.332,'4000',horizontalalignment='left',color='lime')
f.add_label(32.582,-10.313,'4020',horizontalalignment='right',color='lime')
f.add_label(32.572,-10.340,'4040',horizontalalignment='left',color='lime')
f.add_label(32.584,-10.317,'4060',horizontalalignment='right',color='lime')
f.add_label(32.585,-10.324,'4080',horizontalalignment='right',color='lime')

#Add grid lines
f.add_grid()
f.grid.set_color('black')

#Save
if save_figs:
    plt.savefig('Fig13-NGC848_mom1_cont.pdf',bbox_inches='tight')


# In[ ]:


#Clip the moment 1 map
mask_mom1(gal='PGC8210',level=0.25)

#Use coordinate system from r-band image
f = aplpy.FITSFigure(r_image_decals,figsize=(8.27,2.*3),dimensions=[0,1])

#Show DECaLS grz image
f.show_rgb(grz_image_decals)

#Re-centre
f.recenter(32.275081,  -10.320226, radius=2./60.)

#Plot contours with a spacing of 20 km\s
f.show_contour(data='tmp.fits',dimensions=[0,1],slices=[0],
               colors='lime',levels=numpy.arange(3960.,4200.,20.))

#Add manual labels
f.add_label(32.267,-10.322,'3960',horizontalalignment='left',color='lime')
f.add_label(32.269,-10.315,'3980',horizontalalignment='left',color='lime')
f.add_label(32.275,-10.312,'4000',horizontalalignment='left',color='lime')

#Add grid lines
f.add_grid()
f.grid.set_color('black')

#Save
if save_figs:
    plt.savefig('Fig14-PGC8210_mom1_cont.pdf',bbox_inches='tight')


# In[ ]:




