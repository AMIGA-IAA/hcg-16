import numpy, matplotlib, os
import aplpy
import matplotlib.pyplot as plt
import matplotlib as mpl
import astropy.io.fits

font = {'size'   : 14, 'family' : 'serif', 'serif' : 'cm'}
plt.rc('font', **font)
plt.rcParams['text.usetex'] = True
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] ='gray_r'
plt.rcParams['lines.linewidth'] = 1
plt.rcParams['axes.linewidth'] = 1


#Define directories where files are stored
script_dir = os.getcwd()
casa_dir = os.path.join(script_dir,"../casa/")
sofia_dir = os.path.join(script_dir,"../sofia/")


#Read in the moment 0 map and check that casa produced the correct header
filename = 'HCG16_CD_rob2_MS.mom0.pbcor.fits'
tmp = astropy.io.fits.open(casa_dir+filename)
if tmp[0].header['EQUINOX'] != 1950 or mom0[0].header['EQUINOX'] != 2000:
    tmp[0].header['EQUINOX'] = 2000
    tmp.writeto(casa_dir+filename,overwrite=True)
tmp.close()


#Make the moment 0 map figure
fig = plt.figure(figsize=(2.*8.27,2.*3))

ax1 = plt.subplot2grid((1, 36), (0, 0), colspan=13)
ax2 = plt.subplot2grid((1, 36), (0, 14), colspan=1)
ax3 = plt.subplot2grid((1, 36), (0, 22), colspan=13)

ax1.set_yticks([])
ax1.set_xticks([])
ax2.set_yticks([])
ax2.set_xticks([])
ax3.set_yticks([])
ax3.set_xticks([])


mom0 = aplpy.FITSFigure(casa_dir+'HCG16_CD_rob2_MS.mom0.pbcor.fits', figure=fig, subplot=list(ax1.get_position(fig).bounds), slices=[0,0])

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



overlay = aplpy.FITSFigure('HCG16_DECaLS_r_cutout.fits', figure=fig, subplot=list(ax3.get_position(fig).bounds), dimensions=[0, 1])

#Commands for moment 0 map
mom0.recenter(32.45, -10.225, radius=0.2)

viridis_cmap = plt.cm.viridis_r
viridis_cmap.set_under(color='w')

mom0.add_beam()
mom0.beam.set_color('k')
mom0.beam.set_corner('bottom right')

mom0.show_colorscale(cmap=viridis_cmap,vmin=1E-6,vmax=1.,interpolation='none')
mom0.add_grid()
mom0.grid.set_color('black')
mom0.grid.set_alpha(0.25)

mom0.show_markers(32.3804, -10.15833,marker='x',c='r')


#Make the colourbar
cbar = mpl.colorbar.ColorbarBase(ax2, cmap=viridis_cmap,orientation='vertical',label='Flux [Jy km/s per beam]')


#Commands for overlay
overlay.recenter(32.45, -10.225, radius=0.2)

overlay.show_contour(sofia_dir+'HCG16_CD_rob2_MS_mom0.fits',dimensions=[0,1],slices=[0],
               colors='lime',levels=[-0.025,0.025,0.1,0.25,0.5,0.75,1.])

overlay.show_rgb('HCG16_DECaLS_cutout.jpeg')
overlay.add_grid()
overlay.grid.set_color('black')

overlay.add_label(32.25,-10.35,'PGC 8210',horizontalalignment='right',color='yellow',weight='bold')
overlay.add_label(32.535,-10.32,'NGC 848',horizontalalignment='left',color='yellow',weight='bold')
overlay.add_label(32.28,-10.17,'HCG 16a',horizontalalignment='right',color='yellow',weight='bold')
overlay.add_label(32.25,-10.135,'HCG 16b',horizontalalignment='right',color='yellow',weight='bold')
overlay.add_label(32.45,-10.145,'HCG 16c',horizontalalignment='right',color='yellow',weight='bold')
overlay.add_label(32.35,-10.22,'HCG 16d',horizontalalignment='right',color='yellow',weight='bold')

fig.savefig('HCG16_mom0+DECaLS_overlay.pdf',bbox_inches='tight')
