#Import the VLA archive data files
importvla(archivefiles=['AW500_C990113.xp1','AW500_D990114.xp1'],vis='HCG16_C')
importvla(archivefiles=['AW234_B891206.xp1'],vis='HCG16_D')

#Plot antennae locations
#plotants(vis='HCG16_C',figfile='ant_loc_C.png')
#plotants(vis='HCG16_D',figfile='ant_loc_D.png')



#Calibration of C-array data
#Flag dummy scan and bad RFI
flagdata(vis='HCG16_C',field='2',timerange='04:32:40~04:32:50')
flagdata(vis='HCG16_C',field='2',spw='0:10',antenna='VA07;VA10')

#Flag shadowed antennae
flagdata(vis='HCG16_C', mode='shadow', tolerance=5.0, flagbackup=False)

#Flag zero-amplitude data
flagdata(vis='HCG16_C', mode='clip', clipzeros=True, flagbackup=False)

#Quack
flagdata(vis='HCG16_C', mode='quack', quackinterval=5.0, quackmode='beg', flagbackup=False)

#Print flag summary
flagInfo = flagdata(vis='HCG16_C', mode='summary')

#Save with just the inital flags
flagmanager(vis='HCG16_C', mode='save', versionname='initial_flags')

#Gaincurve (elevation) calibration
gencal(vis='HCG16_C',caltable='gaincurve.cal',caltype='gceff')

#Set gain calibrator flux (will use current model, Perley & Butler 2013 find it only varies by ~2% in L-band)
setjy(vis='HCG16_C',field='2',spw='0',scalebychan=True,model='3C48_L.im')

#plotms(vis='HCG16_C',field='2',
#       xaxis='time',yaxis='phase',correlation='RR',
#       avgchannel='64',spw='0:4~58',antenna='VA11', coloraxis='antenna2')

#Fit delay calibration for the bandpass calibrator
#Use VA11 as reference antenna
gaincal(vis='HCG16_C',field='2',caltable='delays.cal',refant='VA11',gaintype='K',gaintable=['gaincurve.cal'])

#Make the bandpass calibration table
gaincal(vis='HCG16_C',field='2',caltable='bpphase.gcal',spw='0:5~55',refant='VA11',calmode='p',solint='10s',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal'])

#plotcal(caltable='bpphase.gcal',xaxis='time',yaxis='phase',
#        iteration='antenna',subplot=331,plotrange=[0,0,-180,180])

#Bandpass solution
bandpass(vis='HCG16_C',field='2',caltable='bandpass.bcal',refant='VA11',solnorm=True,solint='inf',gaintable=['gaincurve.cal','delays.cal','bpphase.gcal'])

#plotcal(caltable='bandpass.bcal',xaxis='chan',yaxis='amp',
#        iteration='antenna',subplot=331)

#plotcal(caltable='bandpass.bcal',xaxis='chan',yaxis='phase',
#        iteration='antenna',subplot=331)

#Apply initial solutions
applycal(vis='HCG16_C',field='2',gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'],gainfield=['','2','2'])

#plotms(vis='HCG16_C',field='2',
#       xaxis='channel',yaxis='phase',ydatacolumn='corrected',
#       correlation='RR',
#       avgtime='1e8',spw='0:4~58',antenna='VA11', coloraxis='antenna2')

#plotms(vis='HCG16_C',field='2',
#       xaxis='channel',yaxis='amp',ydatacolumn='corrected',
#       correlation='RR',
#       avgtime='1e8',spw='0:4~58',antenna='VA11', coloraxis='antenna2')

#Gain calibration
#Integration phase
gaincal(vis='HCG16_C',field='1,2',caltable='intphase.gcal',refant='VA11',spw='0:5~55',calmode='p',solint='10s',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'])

#plotcal(caltable='intphase.gcal',xaxis='time',yaxis='phase',
#        iteration='antenna',subplot=331,plotrange=[0,0,-180,180])

#Scan phase
gaincal(vis='HCG16_C',field='1,2',caltable='scanphase.gcal',refant='VA11',spw='0:5~55',calmode='p',solint='inf',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'])

#plotcal(caltable='scanphase.gcal',xaxis='time',yaxis='phase',
#        iteration='antenna',subplot=331,plotrange=[0,0,-180,180])

#Amplitude solutions
gaincal(vis='HCG16_C',field='1,2',caltable='amp.gcal',refant='VA11',spw='0:5~55',calmode='ap',solint='inf',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal','intphase.gcal'])

#plotcal(caltable='amp.gcal',xaxis='time',yaxis='phase',
#        iteration='antenna',subplot=331,plotrange=[-1,-1,-20,20])

#Scale fluxes
fluxscale(vis='HCG16_C',caltable='amp.gcal',
          fluxtable='flux.cal',reference='2',incremental=True)

#Apply calibration to bandpass/flux calibrator
applycal(vis='HCG16_C',field='2',
        gaintable=['gaincurve.cal','delays.cal','bandpass.bcal','intphase.gcal','amp.gcal','flux.cal'],
        gainfield=['','2','2','2','2','2'],
        calwt=False)

#plotms(vis='HCG16_C',field='2',ydatacolumn='corrected',
#       xaxis='time',yaxis='amp',correlation='RR,LL',
#       avgchannel='64',spw='0:4~58',antenna='', coloraxis='antenna1')

#Gain of first sample seems to be low - flag it
flagdata(vis='HCG16_C',field='2',timerange='04:32:50~04:33:00')

#Do a better job of flagging the RFI in channel 10
flagdata(vis='HCG16_C',field='2',spw='0:10',antenna='VA01&VA03;VA04&VA11;VA05&VA24;VA05&VA25;VA06&VA09')
flagdata(vis='HCG16_C',field='2',spw='0:10',antenna='VA03&VA20;VA04&VA23;VA05&VA23')
flagdata(vis='HCG16_C',field='2',spw='0:10',antenna='VA04&VA05;VA04&VA24;VA05&VA11;VA05&VA14;VA09&VA14;VA09&VA28;VA14&VA24;VA14&VA28')
flagdata(vis='HCG16_C',field='2',spw='0:10',antenna='VA03&VA15;VA11&VA24;VA23&VA24')
flagdata(vis='HCG16_C',field='2',spw='0:10',antenna='VA03&VA12;VA11&VA14;VA24&VA25')

flagdata(vis='HCG16_C',field='2',spw='0:11',antenna='VA05&VA07;VA05&VA10;VA07&VA10;VA07&VA14;VA07&VA24;VA10&VA23;VA10&VA24')

flagdata(vis='HCG16_C',field='2',spw='0:09',antenna='VA05&VA07;VA05&VA10;VA07&VA10;VA07&VA14;VA07&VA24;VA10&VA23;VA10&VA24')

#Repeat calibration with improved flagging
gaincal(vis='HCG16_C',field='2',caltable='delays.cal',refant='VA11',gaintype='K',gaintable=['gaincurve.cal'])
gaincal(vis='HCG16_C',field='2',caltable='bpphase.gcal',spw='0:5~55',refant='VA11',calmode='p',solint='10s',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal'])
bandpass(vis='HCG16_C',field='2',caltable='bandpass.bcal',refant='VA11',solnorm=True,solint='inf',gaintable=['gaincurve.cal','delays.cal','bpphase.gcal'])
applycal(vis='HCG16_C',field='2',gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'],gainfield=['','2','2'])
gaincal(vis='HCG16_C',field='1,2',caltable='intphase.gcal',refant='VA11',spw='0:5~55',calmode='p',solint='10s',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'])
gaincal(vis='HCG16_C',field='1,2',caltable='scanphase.gcal',refant='VA11',spw='0:5~55',calmode='p',solint='inf',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'])
gaincal(vis='HCG16_C',field='1,2',caltable='amp.gcal',refant='VA11',spw='0:5~55',calmode='ap',solint='inf',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal','intphase.gcal'])
fluxscale(vis='HCG16_C',caltable='amp.gcal',
          fluxtable='flux.cal',reference='2',incremental=True)
applycal(vis='HCG16_C',field='2',
        gaintable=['gaincurve.cal','delays.cal','bandpass.bcal','intphase.gcal','amp.gcal','flux.cal'],
        gainfield=['','2','2','2','2','2'],
        calwt=False)

#plotms(vis='HCG16_C',field='2',ydatacolumn='corrected',
#       xaxis='time',yaxis='amp',correlation='RR,LL',
#       avgchannel='64',spw='0:4~58',antenna='', coloraxis='antenna1')

#There are still some very low flux spikes at particular times
flagdata(vis='HCG16_C',field='2',spw='0',antenna='VA26',timerange='04:35:00~04:35:10')
flagdata(vis='HCG16_C',field='2',spw='0',antenna='VA19',timerange='04:34:50~04:35:00')
flagdata(vis='HCG16_C',field='2',spw='0',antenna='VA21',timerange='04:36:20~04:36:30')
flagdata(vis='HCG16_C',field='2',spw='0',antenna='VA17',timerange='04:35:10~04:35:20')

#Repeat calibration steps again
gaincal(vis='HCG16_C',field='2',caltable='delays.cal',refant='VA11',gaintype='K',gaintable=['gaincurve.cal'])
gaincal(vis='HCG16_C',field='2',caltable='bpphase.gcal',spw='0:5~55',refant='VA11',calmode='p',solint='10s',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal'])
bandpass(vis='HCG16_C',field='2',caltable='bandpass.bcal',refant='VA11',solnorm=True,solint='inf',gaintable=['gaincurve.cal','delays.cal','bpphase.gcal'])
applycal(vis='HCG16_C',field='2',gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'],gainfield=['','2','2'])
gaincal(vis='HCG16_C',field='1,2',caltable='intphase.gcal',refant='VA11',spw='0:5~55',calmode='p',solint='10s',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'])
gaincal(vis='HCG16_C',field='1,2',caltable='scanphase.gcal',refant='VA11',spw='0:5~55',calmode='p',solint='inf',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'])
gaincal(vis='HCG16_C',field='1,2',caltable='amp.gcal',refant='VA11',spw='0:5~55',calmode='ap',solint='inf',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal','intphase.gcal'])
fluxscale(vis='HCG16_C',caltable='amp.gcal',
          fluxtable='flux.cal',reference='2',incremental=True)
applycal(vis='HCG16_C',field='2',
        gaintable=['gaincurve.cal','delays.cal','bandpass.bcal','intphase.gcal','amp.gcal','flux.cal'],
        gainfield=['','2','2','2','2','2'],
        calwt=False)

#plotms(vis='HCG16_C',field='2',ydatacolumn='corrected',
#       xaxis='time',yaxis='amp',correlation='RR,LL',
#       avgchannel='64',spw='0:4~58',antenna='', coloraxis='antenna1')

#Apply calibration to phase calibrator
applycal(vis='HCG16_C',field='1',
        gaintable=['gaincurve.cal','delays.cal','bandpass.bcal','intphase.gcal','amp.gcal','flux.cal'],
        gainfield=['','2','2','1','1','1'],
        calwt=False)

#plotms(vis='HCG16_C',field='1',ydatacolumn='corrected',
#       xaxis='time',yaxis='amp',correlation='RR,LL',
#       avgchannel='64',spw='0:4~58',antenna='', coloraxis='antenna2')

#Flag RFI and bad data
flagdata(vis='HCG16_C',field='1',spw='0',antenna='VA22&VA23',timerange='1999/01/14/03:38:00~1999/01/14/03:38:10')
flagdata(vis='HCG16_C',field='1',spw='0:44',antenna='VA25;VA28',timerange='1999/01/13/23:28:00~1999/01/13/23:38:00')

#For the really bad RFI use the automated proceedures
#flagdata(vis='HCG16_C', mode='tfcrop', field='1,2', spw='0',
#         datacolumn='corrected', action='calculate',
#         display='both', flagbackup=False)

flagdata(vis='HCG16_C', mode='tfcrop', field='1,2', spw='0',
         datacolumn='corrected', action='apply',
         display='none', flagbackup=False)

#flagdata(vis='HCG16_C', mode='rflag', field='1,2', spw='0', datacolumn='corrected',
#         action='calculate', display='both', flagbackup=False)

flagdata(vis='HCG16_C', mode='rflag', field='1,2', spw='0', datacolumn='corrected',
         action='apply', display='none', flagbackup=False)

#Recalculate calibration
gaincal(vis='HCG16_C',field='2',caltable='delays.cal',refant='VA11',gaintype='K',gaintable=['gaincurve.cal'])
gaincal(vis='HCG16_C',field='2',caltable='bpphase.gcal',spw='0:5~55',refant='VA11',calmode='p',solint='10s',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal'])
bandpass(vis='HCG16_C',field='2',caltable='bandpass.bcal',refant='VA11',solnorm=True,solint='inf',gaintable=['gaincurve.cal','delays.cal','bpphase.gcal'])
applycal(vis='HCG16_C',field='2',gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'],gainfield=['','2','2'])
gaincal(vis='HCG16_C',field='1,2',caltable='intphase.gcal',refant='VA11',spw='0:5~55',calmode='p',solint='10s',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'])
gaincal(vis='HCG16_C',field='1,2',caltable='scanphase.gcal',refant='VA11',spw='0:5~55',calmode='p',solint='inf',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'])
gaincal(vis='HCG16_C',field='1,2',caltable='amp.gcal',refant='VA11',spw='0:5~55',calmode='ap',solint='inf',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal','intphase.gcal'])
fluxscale(vis='HCG16_C',caltable='amp.gcal',
          fluxtable='flux.cal',reference='2',incremental=True)
applycal(vis='HCG16_C',field='2',
        gaintable=['gaincurve.cal','delays.cal','bandpass.bcal','intphase.gcal','amp.gcal','flux.cal'],
        gainfield=['','2','2','2','2','2'],
        calwt=False)

#plotms(vis='HCG16_C',field='2',ydatacolumn='corrected',
#       xaxis='time',yaxis='amp',correlation='RR,LL',
#       avgchannel='64',spw='0:4~58',antenna='', coloraxis='antenna1')

applycal(vis='HCG16_C',field='1',
        gaintable=['gaincurve.cal','delays.cal','bandpass.bcal','intphase.gcal','amp.gcal','flux.cal'],
        gainfield=['','2','2','1','1','1'],
        calwt=False)

#plotms(vis='HCG16_C',field='1',ydatacolumn='corrected',
#       xaxis='time',yaxis='amp',correlation='RR,LL',
#       avgchannel='64',spw='0:4~58',antenna='', coloraxis='antenna2')

#Looks ok now apply to target data
applycal(vis='HCG16_C',field='0',
        gaintable=['gaincurve.cal','delays.cal','bandpass.bcal','intphase.gcal','amp.gcal','flux.cal'],
        gainfield=['','2','2','1','1','1'],
        calwt=False)








#Calibration of D-array data

#Flag shadowed antennae
flagdata(vis='HCG16_D', mode='shadow', tolerance=5.0, flagbackup=False)

#Flag zero-amplitude data
flagdata(vis='HCG16_D', mode='clip', clipzeros=True, flagbackup=False)

#Quack
flagdata(vis='HCG16_D', mode='quack', quackinterval=5.0, quackmode='beg', flagbackup=False)

#Print flag summary
flagInfo = flagdata(vis='HCG16_D', mode='summary')

#Save with just the inital flags
flagmanager(vis='HCG16_D', mode='save', versionname='initial_flags')

#Gaincurve (elevation) calibration
gencal(vis='HCG16_D',caltable='gaincurve.cal',caltype='gceff')

#Set gain calibrator flux (will use current model, Perley & Butler 2013 find it only varies by ~2% in L-band)
setjy(vis='HCG16_D',field='2',spw='0',scalebychan=True,model='3C48_L.im')

#plotms(vis='HCG16_D',field='2',
#       xaxis='time',yaxis='phase',correlation='RR',
#       avgchannel='64',spw='0:4~58',antenna='VA06', coloraxis='antenna2')

#Fit delay calibration for the bandpass calibrator
#Use VA06 as reference antenna
gaincal(vis='HCG16_D',field='2',caltable='delays.cal',refant='VA06',gaintype='K',gaintable=['gaincurve.cal'])

#Make the bandpass calibration table
gaincal(vis='HCG16_D',field='2',caltable='bpphase.gcal',spw='0:5~55',refant='VA06',calmode='p',solint='10s',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal'])

#plotcal(caltable='bpphase.gcal',xaxis='time',yaxis='phase',
#        iteration='antenna',subplot=331,plotrange=[0,0,-180,180])

#Bandpass solution
bandpass(vis='HCG16_D',field='2',caltable='bandpass.bcal',refant='VA06',solnorm=True,solint='inf',gaintable=['gaincurve.cal','delays.cal','bpphase.gcal'])

#plotcal(caltable='bandpass.bcal',xaxis='chan',yaxis='amp',
#        iteration='antenna',subplot=331)

#plotcal(caltable='bandpass.bcal',xaxis='chan',yaxis='phase',
#        iteration='antenna',subplot=331)

#Apply initial solutions
applycal(vis='HCG16_D',field='2',gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'],gainfield=['','2','2'])

#plotms(vis='HCG16_D',field='2',
#       xaxis='channel',yaxis='phase',ydatacolumn='corrected',
#       correlation='RR',
#       avgtime='1e8',spw='0:4~58',antenna='VA06', coloraxis='antenna2')

#plotms(vis='HCG16_D',field='2',
#       xaxis='channel',yaxis='amp',ydatacolumn='corrected',
#       correlation='RR',
#       avgtime='1e8',spw='0:4~58',antenna='VA06', coloraxis='antenna2')

#Gain calibration
#Integration phase
gaincal(vis='HCG16_D',field='0,2',caltable='intphase.gcal',refant='VA06',spw='0:5~55',calmode='p',solint='10s',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'])

#plotcal(caltable='intphase.gcal',xaxis='time',yaxis='phase',
#        iteration='antenna',subplot=331,plotrange=[0,0,-180,180])

#Scan phase
gaincal(vis='HCG16_D',field='0,2',caltable='scanphase.gcal',refant='VA06',spw='0:5~55',calmode='p',solint='inf',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'])

#plotcal(caltable='scanphase.gcal',xaxis='time',yaxis='phase',
#        iteration='antenna',subplot=331,plotrange=[0,0,-180,180])

#Amplitude solutions
gaincal(vis='HCG16_D',field='0,2',caltable='amp.gcal',refant='VA06',spw='0:5~55',calmode='ap',solint='inf',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal','intphase.gcal'])

#plotcal(caltable='amp.gcal',xaxis='time',yaxis='phase',
#        iteration='antenna',subplot=331,plotrange=[-1,-1,-20,20])

#Scale fluxes
fluxscale(vis='HCG16_D',caltable='amp.gcal',
          fluxtable='flux.cal',reference='2',incremental=True)

#Apply calibration to bandpass/flux calibrator
applycal(vis='HCG16_D',field='2',
        gaintable=['gaincurve.cal','delays.cal','bandpass.bcal','intphase.gcal','amp.gcal','flux.cal'],
        gainfield=['','2','2','2','2','2'],
        calwt=False)

#plotms(vis='HCG16_D',field='2',ydatacolumn='corrected',
#       xaxis='time',yaxis='amp',correlation='RR,LL',
#       avgchannel='64',spw='0:4~58',antenna='', coloraxis='antenna1')

#Flag RFI
flagdata(vis='HCG16_D',field='2',spw='0',timerange='08:03:10~08:03:20')

#Use tfcrop to get rid of bad RFI
#flagdata(vis='HCG16_D', mode='tfcrop', field='2', spw='0',
#         datacolumn='corrected', action='calculate',
#         display='both', flagbackup=False)

flagdata(vis='HCG16_D', mode='tfcrop', field='2', spw='0',
         datacolumn='corrected', action='apply',
         display='none', flagbackup=False)

#Repeat calibration
gaincal(vis='HCG16_D',field='2',caltable='delays.cal',refant='VA06',gaintype='K',gaintable=['gaincurve.cal'])
gaincal(vis='HCG16_D',field='2',caltable='bpphase.gcal',spw='0:5~55',refant='VA06',calmode='p',solint='10s',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal'])
bandpass(vis='HCG16_D',field='2',caltable='bandpass.bcal',refant='VA06',solnorm=True,solint='inf',gaintable=['gaincurve.cal','delays.cal','bpphase.gcal'])
applycal(vis='HCG16_D',field='2',gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'],gainfield=['','2','2'])
gaincal(vis='HCG16_D',field='0,2',caltable='intphase.gcal',refant='VA06',spw='0:5~55',calmode='p',solint='10s',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'])
gaincal(vis='HCG16_D',field='0,2',caltable='scanphase.gcal',refant='VA06',spw='0:5~55',calmode='p',solint='inf',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'])
gaincal(vis='HCG16_D',field='0,2',caltable='amp.gcal',refant='VA06',spw='0:5~55',calmode='ap',solint='inf',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal','intphase.gcal'])
fluxscale(vis='HCG16_D',caltable='amp.gcal',
          fluxtable='flux.cal',reference='2',incremental=True)
applycal(vis='HCG16_D',field='2',
        gaintable=['gaincurve.cal','delays.cal','bandpass.bcal','intphase.gcal','amp.gcal','flux.cal'],
        gainfield=['','2','2','2','2','2'],
        calwt=False)

#plotms(vis='HCG16_D',field='2',ydatacolumn='corrected',
#       xaxis='time',yaxis='amp',correlation='RR,LL',
#       avgchannel='64',spw='0:4~58',antenna='', coloraxis='antenna1')

#Apply calibration to phase calibrator
applycal(vis='HCG16_D',field='0',
        gaintable=['gaincurve.cal','delays.cal','bandpass.bcal','intphase.gcal','amp.gcal','flux.cal'],
        gainfield=['','2','2','0','0','0'],
        calwt=False)

#plotms(vis='HCG16_D',field='0',ydatacolumn='corrected',
#       xaxis='time',yaxis='amp',correlation='RR,LL',
#       avgchannel='64',spw='0:4~58',antenna='', coloraxis='antenna2')

#Flag obvious RFI
flagdata(vis='HCG16_D',field='0',spw='0',timerange='04:35:10~04:35:20')
flagdata(vis='HCG16_D',field='0',spw='0',timerange='04:35:40~04:35:50')
flagdata(vis='HCG16_D',field='0',spw='0',timerange='05:20:40~05:20:50')
flagdata(vis='HCG16_D',field='0',spw='0',timerange='05:20:10~05:20:20')
flagdata(vis='HCG16_D',field='0',spw='0',timerange='06:04:40~06:04:50')
flagdata(vis='HCG16_D',field='0',spw='0',timerange='06:04:10~06:04:20')
flagdata(vis='HCG16_D',field='0',spw='0',antenna='VA02&VA24',scan='5')
flagdata(vis='HCG16_D',field='0',spw='0',antenna='VA09&VA10;VA09&VA12',scan='7')
flagdata(vis='HCG16_D',field='0',spw='0',antenna='VA13&VA27;VA25&VA27',scan='3')
flagdata(vis='HCG16_D',field='0',spw='0',antenna='VA09&VA12;VA10&VA12',scan='19')

#Use automated methods to get rid of really bad RFI
#flagdata(vis='HCG16_D', mode='tfcrop', field='0', spw='0',
#         datacolumn='corrected', action='calculate',
#         display='both', flagbackup=False)

flagdata(vis='HCG16_D', mode='tfcrop', field='0', spw='0',
         datacolumn='corrected', action='apply',
         display='none', flagbackup=False)

#flagdata(vis='HCG16_D', mode='rflag', field='0', spw='0', datacolumn='corrected',
#         action='calculate', display='both', flagbackup=False)

flagdata(vis='HCG16_D', mode='rflag', field='0', spw='0', datacolumn='corrected',
         action='apply', display='none', flagbackup=False)

#Repeat calibration
gaincal(vis='HCG16_D',field='2',caltable='delays.cal',refant='VA06',gaintype='K',gaintable=['gaincurve.cal'])
gaincal(vis='HCG16_D',field='2',caltable='bpphase.gcal',spw='0:5~55',refant='VA06',calmode='p',solint='10s',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal'])
bandpass(vis='HCG16_D',field='2',caltable='bandpass.bcal',refant='VA06',solnorm=True,solint='inf',gaintable=['gaincurve.cal','delays.cal','bpphase.gcal'])
applycal(vis='HCG16_D',field='2',gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'],gainfield=['','2','2'])
gaincal(vis='HCG16_D',field='0,2',caltable='intphase.gcal',refant='VA06',spw='0:5~55',calmode='p',solint='10s',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'])
gaincal(vis='HCG16_D',field='0,2',caltable='scanphase.gcal',refant='VA06',spw='0:5~55',calmode='p',solint='inf',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal'])
gaincal(vis='HCG16_D',field='0,2',caltable='amp.gcal',refant='VA06',spw='0:5~55',calmode='ap',solint='inf',minsnr=2.0,gaintable=['gaincurve.cal','delays.cal','bandpass.bcal','intphase.gcal'])
fluxscale(vis='HCG16_D',caltable='amp.gcal',
          fluxtable='flux.cal',reference='2',incremental=True)
applycal(vis='HCG16_D',field='2',
        gaintable=['gaincurve.cal','delays.cal','bandpass.bcal','intphase.gcal','amp.gcal','flux.cal'],
        gainfield=['','2','2','2','2','2'],
        calwt=False)
applycal(vis='HCG16_D',field='0',
        gaintable=['gaincurve.cal','delays.cal','bandpass.bcal','intphase.gcal','amp.gcal','flux.cal'],
        gainfield=['','2','2','0','0','0'],
        calwt=False)

#plotms(vis='HCG16_D',field='0',ydatacolumn='corrected',
#       xaxis='time',yaxis='amp',correlation='RR,LL',
#       avgchannel='64',spw='0:4~58',antenna='', coloraxis='antenna2')

#Looks ok now apply to target data
applycal(vis='HCG16_D',field='1',
        gaintable=['gaincurve.cal','delays.cal','bandpass.bcal','intphase.gcal','amp.gcal','flux.cal'],
        gainfield=['','2','2','0','0','0'],
        calwt=False)










#Split the target fields off
split(vis='HCG16_C',outputvis='HCG16_C.split',field='0')
split(vis='HCG16_D',outputvis='HCG16_D.split',field='1')




#Now flag the target data
flagInfo = flagdata(vis='HCG16_C.split', mode='summary')
flagmanager(vis='HCG16_C.split', mode='save', versionname='start_flags')

#Flag obvious problems by hand
flagdata(vis='HCG16_C.split',spw='0:61~62')
flagdata(vis='HCG16_C.split',spw='0',antenna='VA17&VA22',timerange='1999/01/13/01:00:00~1999/01/14/01:10:00')
flagdata(vis='HCG16_C.split',spw='0',antenna='VA01&VA22;VA04&VA22;VA10&VA22;VA20&VA22;VA22&VA23;VA22&VA25')
flagdata(vis='HCG16_C.split',spw='0',antenna='VA01&VA28',timerange='1999/01/14/02:13:25~1999/01/14/02:13:35')
flagdata(vis='HCG16_C.split',spw='0:43~45',antenna='VA07;VA28',timerange='1999/01/13/01:00:00~1999/01/14/00:23:23')

#Save these flags before automatic steps
flagInfo = flagdata(vis='HCG16_C.split', mode='summary')
flagmanager(vis='HCG16_C.split', mode='save', versionname='manual_flags')

#For the really bad RFI use the automated proceedures
flagdata(vis='HCG16_C.split', mode='tfcrop', spw='0', action='calculate',
         display='none', flagbackup=False)

flagdata(vis='HCG16_C.split', mode='tfcrop', spw='0', action='apply',
         display='none', flagbackup=False)

flagdata(vis='HCG16_C.split', mode='rflag', spw='0', timedevscale=4.0, freqdevscale=4.0,
         action='calculate', display='none', flagbackup=False)

flagdata(vis='HCG16_C.split', mode='rflag', spw='0', timedevscale=4.0, freqdevscale=4.0,
         action='apply', display='none', flagbackup=False)

flagInfo = flagdata(vis='HCG16_C.split', mode='summary')
flagmanager(vis='HCG16_C.split', mode='save', versionname='final_flags')




flagInfo = flagdata(vis='HCG16_D.split', mode='summary')
flagmanager(vis='HCG16_D.split', mode='save', versionname='start_flags')

#Flag
flagdata(vis='HCG16_D.split',spw='0:0')
flagdata(vis='HCG16_D.split',spw='0:62')

flagdata(vis='HCG16_D.split',spw='0',antenna='VA09&VA12;VA14&VA20',timerange='04:26:55~04:27:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA04&VA10;VA09&VA12;VA14&VA20',timerange='04:44:55~04:45:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA04&VA10',timerange='03:30:00~12:00:00')

flagdata(vis='HCG16_D.split', spw='0', antenna='', mode='manual', flagbackup=False, timerange='1989/12/06/04:49:55~1989/12/06/04:50:05,1989/12/06/06:25:55~1989/12/06/06:26:05,1989/12/06/07:44:55~1989/12/06/07:46:05,1989/12/06/06:21:55~1989/12/06/06:22:05,1989/12/06/06:13:55~1989/12/06/06:14:05,1989/12/06/06:47:55~1989/12/06/06:48:05,1989/12/06/05:47:55~1989/12/06/05:48:05,1989/12/06/05:37:55~1989/12/06/05:38:05,1989/12/06/05:29:55~1989/12/06/05:30:05,1989/12/06/05:11:55~1989/12/06/05:12:05,1989/12/06/04:45:55~1989/12/06/04:46:05,1989/12/06/04:19:55~1989/12/06/04:20:05,1989/12/06/04:09:55~1989/12/06/04:10:05,1989/12/06/04:01:55~1989/12/06/04:02:05,1989/12/06/03:45:55~1989/12/06/03:46:05,1989/12/06/03:27:55~1989/12/06/03:28:05,1989/12/06/00:27:55~1989/12/06/00:28:05')

flagdata(vis='HCG16_D.split', spw='0:8~11', antenna='', mode='manual', flagbackup=False, timerange='')

flagdata(vis='HCG16_D.split',spw='0',antenna='VA02&VA24',timerange='01:38:55~01:45:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA02&VA04;VA02&VA11;VA02&VA19;VA03&VA04;VA03&VA19;VA04&VA11;VA04&VA13;VA04&VA19;VA11&VA13;VA11&VA19;VA13&VA19;VA17&VA19',timerange='06:22:55~06:23:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA04&VA11;VA04&VA12;VA06&VA17;VA09&VA10;VA09&VA12;VA10&VA11;VA10&VA12;VA11&VA19',timerange='06:12:55~06:13:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA02&VA05;VA03&VA27;VA04&VA11;VA09&VA10;VA10&VA11;VA10&VA12;VA11&VA19',timerange='05:28:55~05:29:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='',timerange='04:44:55~04:49:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA02&VA10;VA09&VA10;VA09&VA12;VA10&VA12',timerange='06:30:55~06:31:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA02&VA10;VA09&VA10;VA09&VA12',timerange='06:20:55~06:21:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA02&VA04;VA02&VA10;VA02&VA11;VA03&VA11;VA03&VA19;VA04&VA19;VA14&VA20',timerange='06:12:55~06:13:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA02&VA04',timerange='06:10:55~06:11:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA02&VA04',timerange='06:08:55~06:09:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA01&VA11;VA01&VA19;VA02&VA04;VA02&VA11;VA04&VA11;VA09&VA10;VA10&VA12;VA11&VA19;VA14&VA20',timerange='05:54:55~05:55:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA02&VA04;VA02&VA05;VA02&VA10;VA02&VA11;VA04&VA11;VA09&VA10;VA09&VA12;VA10&VA11;VA10&VA12',timerange='05:46:55~05:47:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA02&VA10;VA04&VA11;VA10&VA11;VA10&VA12',timerange='05:44:55~05:45:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA02&VA04;VA02&VA05;VA02&VA11;VA03&VA17;VA04&VA11;VA05&VA11;VA09&VA12;VA10&VA12;VA17&VA27',timerange='05:36:55~05:37:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA02&VA04;VA02&VA10;VA02&VA11',timerange='05:28:55~05:29:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA02&VA11;VA04&VA11;VA09&VA10',timerange='05:10:55~05:11:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA04&VA11;VA09&VA12',timerange='04:52:55~04:53:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA01&VA08;VA01&VA11;VA06&VA17;VA08&VA16;VA08&VA28;VA17&VA27;VA17&VA28',timerange='04:50:55~04:51:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA09&VA10;VA09&VA12',timerange='04:18:55~04:19:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA02&VA17;VA02&VA20;VA02&VA28;VA09&VA10;VA11&VA19;VA17&VA20;VA20&VA28',timerange='04:08:55~04:09:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA01&VA02;VA01&VA19;VA02&VA03;VA02&VA17;VA02&VA20;VA02&VA28;VA09&VA10;VA09&VA12',timerange='04:00:55~04:01:05')
flagdata(vis='HCG16_D.split',spw='0',antenna='VA01&VA19;VA11&VA19',timerange='03:26:55~03:27:05')





#Save final flags
flagInfo = flagdata(vis='HCG16_C.split', mode='summary')
flagmanager(vis='HCG16_C.split', mode='save', versionname='final_flags')

flagInfo = flagdata(vis='HCG16_D.split', mode='summary')
flagmanager(vis='HCG16_D.split', mode='save', versionname='final_flags')


