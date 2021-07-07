import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import sys
import datetime
import time
from bitalino import BITalino

# usage: python ADmonirecBitalino.py <Channels> <Fs> <Tdur>
# e.g. : python ADmonirecBitalino.py 0 1 2 3 4 1000 5.0

# https://github.com/BITalinoWorld/revolution-python-api
# Channels @ Board Kit:
#  0 --A1 (EMG)
#  1 --A2 (ECG)
#  2 --A3 (EDA)
#  3 --A4 (EEG)
#  4 --A5 (ACC)

# Init.
Twin=0.5
#macAddress = '20:18:05:28:62:98' # or 'COMX' on Windows
macAddress = '/dev/tty.BITalino-97-3E-DevB'
batteryThreshold = 30
device = BITalino(macAddress) # Connect to BITalino
device.battery(batteryThreshold) # Set battery threshold
print(device.version()) # Read BITalino version

# Config. from args
args=sys.argv
Nargs=len(args)
Fs=int(args[Nargs-2])
nd=int(Fs*float(args[Nargs-1]))
Channels = [int(args[j]) for j in range(1,len(args)-2)] 
Channels.sort()
Nchan=len(Channels)

print('Nchan='+str(Nchan))

# Detect key event
def onKey(event):
 if event.key=='r':
  print('Recording...')
  t,y=funcDAQ(Nchan, nd, Fs, Channels)
  device.stop()
  device.close()
  df = pd.DataFrame(np.concatenate([t, y], 1))
  now=datetime.datetime.now()
  fname='AD'+now.strftime('%Y%m%d%H%M%S')+'.xlsx'
  df.to_excel(fname,index=False, header=False)
  funcDrawdat(t, y, Nchan)
  plt.pause(5)
  print('...Exported to '+fname)
  sys.exit()
 elif event.key=='q':
  device.stop()
  device.close()
  print('Stopped.')
  sys.exit()

# Plot
def funcDrawdat(t, x, Nchan):
 if Nchan>1:
  for i in range(Nchan):	
   plt.subplot(Nchan,1,i+1)
   plt.cla()
   plt.plot(t,x[:,i])
 else:
  plt.cla()
  plt.plot(t,x)

# Data Acquisition & Plot
def funcDAQ(Nchan, N, Fs, chans):
 tmpdat=device.read(N)
 tmpdat=np.array(tmpdat)
 dat=np.empty((N,0), float)
 for i in range(Nchan):
  x=np.reshape(tmpdat[:,chans[i]+5], (N,1))
  dat=np.append(dat, x, axis=1)
 dt=1/Fs
 t=np.linspace(1/Fs,1/Fs*N,N)
 t=np.reshape(t, (N,1))
 funcDrawdat(t, dat, Nchan)
 plt.pause(1e-9)
 return t, dat

# main
device.start(Fs, Channels)
while True:
 try:
  plt.connect('key_press_event',onKey)
  t,y=funcDAQ(Nchan, int(Fs*Twin), Fs, Channels)
 except KeyboardInterrupt:
  break
device.stop()
device.close()