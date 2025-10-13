import scipy as sp
import scipy.io as sio
import numpy as np


filename = '../circle-noise-data/aggregate/grating2AFC S11.mat'

data = sio.loadmat(filename) #loads in data from .mat
for key in ['__header__', '__version__', '__globals__']: #matlab metadata not needed,
    data.pop(key, None) #is popped out (removed), if none then does nothing

np.savez('../circle-noise-data/aggregate/grating2AFC_npz.npz', **data)
# writes remaining items in data dictionary to .npz
# **data unpacks dict so each key is a new var in .npz

print("Done. Open with np.load('grating2AFC_npz.npz')") #indicates completion