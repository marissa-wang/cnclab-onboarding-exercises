from scipy.io import loadmat

# This was used really early on in the code haha, doesn't have much use now, but I will
# keep it here for archive purposes

filename = '../circle-noise-data/aggregate/grating2AFC S11.mat'

data = loadmat(filename)
print(data.keys()) # prints keys of dictionary (filename)