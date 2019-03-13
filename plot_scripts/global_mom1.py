import numpy, matplotlib, os
import aplpy
import matplotlib.pyplot as plt
import matplotlib as mpl
import astropy.io.fits

font = {'size'   : 14, 'family' : 'serif', 'serif' : 'cm'}
plt.rc('font', **font)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] ='gray_r'
plt.rcParams['lines.linewidth'] = 1
plt.rcParams['axes.linewidth'] = 1



c = 299792.458 #km/s

def v_opt(v_rad):
    '''Conversion from radio to optical velocity.'''
    
    return c*((1./(1.-(v_rad/c))) - 1.)

def v_rad(v_opt):
    '''Conversion from radio to optical velocity.'''
    
    return c*(1. - (1./(1.+(v_opt/c))))




#Define directories where files are stored
script_dir = os.getcwd()
casa_dir = os.path.join(script_dir,"../casa/")
sofia_dir = os.path.join(script_dir,"../sofia/")


#Read in the moment 1 map and check that casa produced the correct header
filename = 'HCG16_CD_rob2_MS_ht_mom1.fits'
tmp = astropy.io.fits.open(sofia_dir+filename)
if tmp[0].header['EQUINOX'] != 1950 or mom0[0].header['EQUINOX'] != 2000:
    tmp[0].header['EQUINOX'] = 2000
    tmp.writeto(sofia_dir+filename,overwrite=True)
tmp.close()



#Make moment 1 figure
fig = plt.figure(figsize=(8.27,2.*3))

ax1 = plt.subplot2grid((1, 18), (0, 0), colspan=13)
ax2 = plt.subplot2grid((1, 18), (0, 14), colspan=1)

ax1.set_yticks([])
ax1.set_xticks([])
ax2.set_yticks([])
ax2.set_xticks([])

mom1 = aplpy.FITSFigure(sofia_dir+filename, figure=fig, subplot=list(ax1.get_position(fig).bounds), slices=[0,0])

#Commands for moment 1 map
mom1.recenter(32.45, -10.225, radius=0.2)

mom1.show_markers(32.352519,  -10.135923,marker='*',c='grey',s=50,label='HCG16a')
mom1.show_markers(32.336845,  -10.133093,marker='*',c='grey',s=50,label='HCG16b')
mom1.show_markers(32.4105329, -10.1466869,marker='*',c='grey',s=50,label='HCG16c')
mom1.show_markers(32.428870,  -10.184086,marker='*',c='grey',s=50,label='HCG16d')
mom1.show_markers(32.573518,  -10.321447,marker='*',c='grey',s=50,label='NGC848')
mom1.show_markers(32.275081, -10.320226,marker='*',c='grey',s=50,label='PGC8210')


mom1.show_colorscale(cmap='jet',vmin=3700000.,vmax=4050000.)
mom1.add_grid()
mom1.grid.set_color('black')
mom1.grid.set_alpha(0.25)

mom1.add_beam()
mom1.beam.set_color('k')
mom1.beam.set_corner('bottom right')


#Make the colourbar
cmap = mpl.cm.jet
norm = mpl.colors.Normalize(vmin=v_opt(3700), vmax=v_opt(4050))

cbar = mpl.colorbar.ColorbarBase(ax2, cmap=cmap,norm=norm,orientation='vertical',label=r'$v_{\mathrm{opt}}$ [km/s]')


fig.savefig('HCG16_mom1.pdf',bbox_inches='tight')

