#Reweight the data
initweights(vis="HCG16_C.split",wtmode="nyq")
initweights(vis="HCG16_D.split",wtmode="nyq")



#Subtract the continuum
uvcontsub(vis='HCG16_C.split',field="HCG16",fitspw="0:1~12;51~58",excludechans=False,combine="",
solint="int",fitorder=1,spw="0",want_cont=True)

uvcontsub(vis='HCG16_D.split',field="HCG16",fitspw="0:1~7;12;51~58",excludechans=False,combine="",
solint="int",fitorder=1,spw="0",want_cont=True)

#Make image with manual source mask
tclean(vis=['HCG16_C.split.contsub','HCG16_D.split.contsub'],field="HCG16",spw="0:12~51",
imagename="HCG16_CD_rob2_MS_cleanmask",imsize=[512, 512],cell="4arcsec",specmode="cube",
outframe="bary",veltype="radio",restfreq="1420405751.786Hz",gridder="wproject",
wprojplanes=128,pblimit=0.05,normtype="flatnoise",deconvolver="multiscale",
scales=[0,8,16,24,40],restoringbeam="common",pbcor=True,weighting="briggs",
robust=2.0,niter=100000,gain=0.1,threshold="0.7mJy",cyclefactor=5.0,
interactive=False,usemask="user",mask="HCG16_source_mask")

tclean(vis=['HCG16_C.split.contsub','HCG16_D.split.contsub'],field="HCG16",spw="0:12~51",
imagename="HCG16_CD_rob0_MS_cleanmask",imsize=[512, 512],cell="4arcsec",specmode="cube",
outframe="bary",veltype="radio",restfreq="1420405751.786Hz",gridder="wproject",
wprojplanes=128,pblimit=0.05,normtype="flatnoise",deconvolver="multiscale",
scales=[0,4,8,16,24,40],restoringbeam="common",pbcor=True,weighting="briggs",
robust=0.0,niter=100000,gain=0.1,threshold="0.7mJy",cyclefactor=5.0,
interactive=False,usemask="user",mask="HCG16_source_mask")

tclean(vis=['HCG16_C.split.contsub','HCG16_D.split.contsub'],field="HCG16",spw="0:12~51",
imagename="HCG16_CD_rob2_SC_cleanmask",imsize=[512, 512],cell="4arcsec",specmode="cube",
outframe="bary",veltype="radio",restfreq="1420405751.786Hz",gridder="wproject",
wprojplanes=128,pblimit=0.05,normtype="flatnoise",deconvolver="hogbom",
restoringbeam="common",pbcor=True,weighting="briggs",
robust=2.0,niter=100000,gain=0.1,threshold="0.7mJy",cyclefactor=5.0,
interactive=False,usemask="user",mask="HCG16_source_mask")

#Regrid to J2000
imregrid(imagename="HCG16_CD_rob2_MS_cleanmask.image",template="J2000",output="HCG16_CD_rob2_MS.J2000.image",asvelocity=True,axes=[-1],shape=[-1],interpolation="linear",decimate=10,replicate=False,overwrite=False)

imregrid(imagename="HCG16_CD_rob0_MS_cleanmask.image",template="J2000",output="HCG16_CD_rob0_MS.J2000.image",asvelocity=True,axes=[-1],shape=[-1],interpolation="linear",decimate=10,replicate=False,overwrite=False)

imregrid(imagename="HCG16_CD_rob2_SC_cleanmask.image",template="J2000",output="HCG16_CD_rob2_SC.J2000.image",asvelocity=True,axes=[-1],shape=[-1],interpolation="linear",decimate=10,replicate=False,overwrite=False)

imregrid(imagename="HCG16_CD_rob2_MS_cleanmask.image.pbcor",template="J2000",output="HCG16_CD_rob2_MS.J2000.image.pbcor",asvelocity=True,axes=[-1],shape=[-1],interpolation="linear",decimate=10,replicate=False,overwrite=False)

imregrid(imagename="HCG16_CD_rob0_MS_cleanmask.image.pbcor",template="J2000",output="HCG16_CD_rob0_MS.J2000.image.pbcor",asvelocity=True,axes=[-1],shape=[-1],interpolation="linear",decimate=10,replicate=False,overwrite=False)

imregrid(imagename="HCG16_CD_rob2_SC_cleanmask.image.pbcor",template="J2000",output="HCG16_CD_rob2_SC.J2000.image.pbcor",asvelocity=True,axes=[-1],shape=[-1],interpolation="linear",decimate=10,replicate=False,overwrite=False)


#Save fits files
exportfits(imagename="HCG16_CD_rob2_MS.J2000.image",fitsimage="HCG16_CD_rob2_MS.fits",velocity=True,optical=False,bitpix=-32,
minpix=0,maxpix=-1,overwrite=True,dropstokes=True,stokeslast=True,
history=True,dropdeg=False)

exportfits(imagename="HCG16_CD_rob0_MS.J2000.image",fitsimage="HCG16_CD_rob0_MS.fits",velocity=True,optical=False,bitpix=-32,
minpix=0,maxpix=-1,overwrite=True,dropstokes=True,stokeslast=True,
history=True,dropdeg=False)

exportfits(imagename="HCG16_CD_rob2_SC.J2000.image",fitsimage="HCG16_CD_rob2_SC.fits",velocity=True,optical=False,bitpix=-32,
minpix=0,maxpix=-1,overwrite=True,dropstokes=True,stokeslast=True,
history=True,dropdeg=False)

exportfits(imagename="HCG16_CD_rob2_MS.J2000.image.pbcor",fitsimage="HCG16_CD_rob2_MS.pbcor.fits",velocity=True,optical=False,bitpix=-32,
minpix=0,maxpix=-1,overwrite=True,dropstokes=True,stokeslast=True,
history=True,dropdeg=False)

exportfits(imagename="HCG16_CD_rob0_MS.J2000.image.pbcor",fitsimage="HCG16_CD_rob0_MS.pbcor.fits",velocity=True,optical=False,bitpix=-32,
minpix=0,maxpix=-1,overwrite=True,dropstokes=True,stokeslast=True,
history=True,dropdeg=False)

exportfits(imagename="HCG16_CD_rob2_SC.J2000.image.pbcor",fitsimage="HCG16_CD_rob2_SC.pbcor.fits",velocity=True,optical=False,bitpix=-32,
minpix=0,maxpix=-1,overwrite=True,dropstokes=True,stokeslast=True,
history=True,dropdeg=False)



#Make simple moment 0 map and export it
immoments(imagename="HCG16_CD_rob2_MS_cleanmask.image",moments=[0],axis="spectral",region="",box="",chans="0",stokes="",mask="",includepix=[0.00108,1000000],excludepix=-1,outfile="HCG16_CD_rob2_MS_cleanmask.mom0",stretch=False)

impbcor(imagename="HCG16_CD_rob2_MS_cleanmask.mom0",pbimage="HCG16.pb",outfile="HCG16_CD_rob2_MS_cleanmask.mom0.pbcor",overwrite=False,box="",
region="",chans="",stokes="",mask="",mode="divide",cutoff=-1.0,stretch=False)

imregrid(imagename="HCG16_CD_rob2_MS_cleanmask.mom0.pbcor",template="J2000",output="HCG16_CD_rob2_MS.J2000.mom0.pbcor",asvelocity=True,axes=[-1],shape=[-1],interpolation="linear",decimate=10,replicate=False,overwrite=False)

exportfits(imagename="HCG16_CD_rob2_MS.J2000.mom0.pbcor",fitsimage="HCG16_CD_rob2_MS.mom0.pbcor.fits",velocity=True,optical=False,bitpix=-32,
minpix=0,maxpix=-1,overwrite=True,dropstokes=True,stokeslast=True,history=True,dropdeg=False)
