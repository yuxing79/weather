import numpy as np
import netCDF4
import matplotlib.pyplot as plt
import xarray as xr
from netCDF4 import Dataset
from wrf import getvar, ALL_TIMES, interplevel
import cartopy.crs as ccrs
import cartopy.feature as cfeature# ### 使用 cat 方法合并多个文件




wrfin = Dataset('./wrfout_d01_2022-05-20_12_20_00')
# print(wrfin)
# 提取位势高度和压力场
z = getvar(wrfin, 'z')  # 提取WRF netCDF 变量 # model height
p = getvar(wrfin, 'pressure')    # 单位hPa (29, 216, 216)
q = 1000.*getvar(wrfin, 'QVAPOR')    # 单位hPa (29, 216, 216)
qn=np.array(q)
RTHCUTEN = getvar(wrfin,'RTHCUTEN')
wo_dtt = np.array(RTHCUTEN*86400)
print(RTHCUTEN.shape)
plt.style.use('seaborn-whitegrid')
data = np.load('mskf_0020.npz')
print(data.files)
nx=data['nx']
ny=data['ny']
nz=data['nz']

print(data['dtt'][:,:].shape)
dtt=data['dtt'].reshape((nx,ny,nz),order='c')*86400
unpz=data['u'].reshape((nx,ny,nz),order='c')
qnpz=1000.*data['q'].reshape((nx,ny,nz),order='c')
qt=1000.*data['q'].reshape((nx,ny,nz),order='c')


print(unpz.shape)
#print(unpz[0,21,22])
#print(u[22,21,0])
plt.pcolor(dtt[:,:,10].T,cmap='RdGy')
plt.show()
plt.pcolor(wo_dtt[10,:,:],cmap='RdGy')
plt.show()
plt.pcolor(qt[:,:,0].T,cmap='RdGy')
plt.show()
for i in range(0,219):
    #print(max(qn[0,:,i]-qnpz[i,:,0]),max(wo_dtt[10,:,i]-dtt[i,:,10]))
    for j in range(0,199):
        if(wo_dtt[10,j,i] > 0.0001):
            print(wo_dtt[10,j,i],dtt[i,j,10],wo_dtt[10,j,i]-dtt[i,j,10])
