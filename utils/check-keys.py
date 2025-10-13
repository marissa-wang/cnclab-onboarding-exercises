from scipy.io import loadmat

filename = '../circle-noise-data/aggregate/grating2AFC S11.mat'

data = loadmat(filename)
print(data.keys()) # prints keys of dictionary (filename)