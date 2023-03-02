# weather
steps to modify
suppose working directory(WD) is /home/WRF

1)edit ~/anaconda3/lib/python3.7/my_infer_module.py \
2) edit build.py, phython ./build.py, will have libplugin.so \
3）compile WRFV4.3 (select option 34) as usual, and rename WRFV4\
4) copy WRFV4/phys/module_cumulus_driver.f90 and changed\
5）copy main/wrf.o main/libwrf.a WD/.,  to recompile.bash, linking -lplugin \
6)copy ./wrf.exe to WRFV4/test/em_real\
7)edit namelist.input, cu_physis=11\
8)mpirun -np 1 ./wrf.exe 

will get mskf_0030.npz, mskf_0060.npz..\
output are saved every 30 minutes.\
npz file include (u,v,w,t,q,p,dt,dqv,dqc,dqr,dqi,dqs)\
all three dimensional variables are stored (ims:ime,kms:kme,jms:jme)\

