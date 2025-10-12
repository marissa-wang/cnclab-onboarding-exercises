
import scipy as sp
import scipy.io

# mat = scipy.io.loadmat('file.mat')




import scipy.io as sio

try:
    mat = sio.loadmat('grating2AFC S11.mat')
    print("Loaded with scipy.io:", mat.keys())

except NotImplementedError:
    import h5py
    with h5py.File('grating2AFC S11.mat', 'r') as f:
        print("HDF5 keys:", list(f.keys()))

except Exception as e:
    raise ValueError(f"Could not read file at all: {e}")



