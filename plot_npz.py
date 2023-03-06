import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
data = np.load('mskf_0720.npz')
print(data.files)
print(data['t'][:,:].shape)
print(data['t'][:,:])
nx=90
ny=80
nz=44
for item in data.files:
    print(item)
    if item not in  ['rcv','nx','ny','nxy','nz']:
        print(item)
        t = data[item].reshape((nx,ny,nz),order='c')
        print(t[84,19,9])
        plt.contour(t[:,:,2].T,8,cmap='RdGy')
        plt.legend(item)
        plt.show()     
