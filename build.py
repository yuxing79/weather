#导入cffi包，并且声明了外部函数接口(FFI)对象
import cffi
ffibuilder = cffi.FFI()
#header字符串中包含了需要调用的函数接口的定义
header = """
extern void hello_world(void);
extern void myname(float);
extern void save_fortran_array2(float*,int,int,char*);
extern void save_mskf(float*,float*,float*,float*,float*,float*,float*,float*,float*,float*,float*,float*,int,int,int,char*);

"""
#module字符串中包含了真正需要执行的Python程序。
#装饰器@ffi.def_extern用于标记hello_world函数
module = """
from my_plugin import ffi
import numpy as np
import datetime
import my_infer_module
import os,threading
import time


runner_list= []
pidname = os.getpid()
main_threadid = threading.currentThread()
logger_file_name = "./wrf_plugin_python_pid"+str(pidname)+ "_tid_"+ main_threadid.getName() +str(main_threadid.ident)+".log"
#plugin_logger = my_infer_module.generate_logger(logger_file_name)

@ffi.def_extern()
def hello_world():
    print("Hello World! yux's first fortran python")

@ffi.def_extern()
def myname(u):
    arr = np.array(u)
    np.save("firstnpfile.npy",arr)

@ffi.def_extern()
def save_fortran_array2(data,nx,ny,filename):
    filenam=ffi.string(filename).decode()
    pres_array = my_infer_module.PtrAsarray(ffi,data,(nx,ny))
    arr = np.array(pres_array)
    np.savez(filenam,pres=arr,nx=nx,ny=ny)

@ffi.def_extern()
def save_mskf(u,v,w,t,q,p,dt,dqv,dqc,dqr,dqi,dqs,nx,ny,nz,filename):
    filenam=ffi.string(filename).decode()
    u_array = my_infer_module.PtrAsarray(ffi,u,(nx,nz,ny))
    v_array = my_infer_module.PtrAsarray(ffi,v,(nx,nz,ny))
    w_array = my_infer_module.PtrAsarray(ffi,w,(nx,nz,ny))
    t_array = my_infer_module.PtrAsarray(ffi,t,(nx,nz,ny))
    q_array = my_infer_module.PtrAsarray(ffi,q,(nx,nz,ny))
    p_array = my_infer_module.PtrAsarray(ffi,p,(nx,nz,ny))

    dt_array = my_infer_module.PtrAsarray(ffi,dt,(nx,nz,ny))
    dqv_array = my_infer_module.PtrAsarray(ffi,dqv,(nx,nz,ny))
    dqc_array = my_infer_module.PtrAsarray(ffi,dqc,(nx,nz,ny))
    dqr_array = my_infer_module.PtrAsarray(ffi,dqr,(nx,nz,ny))
    dqi_array = my_infer_module.PtrAsarray(ffi,dqi,(nx,nz,ny))
    dqs_array = my_infer_module.PtrAsarray(ffi,dqs,(nx,nz,ny))
    np.savez(filenam,u=u_array,v=v_array,w=w_array,t=t_array,q=q_array,p=p_array,\
                    dt=dt_array,dqv=dqv_array,dqc=dqc_array,dqr=dqr_array,dqi=dqi_array,dqs=dqs_array,\
            nx=nx,ny=ny,nz=nz)

"""
with open("plugin.h", "w") as f:
    f.write(header)
#定义了API   
ffibuilder.embedding_api(header)
ffibuilder.set_source("my_plugin", r'''
    #include "plugin.h"
''')
#定义了Python代码。
ffibuilder.embedding_init_code(module)
ffibuilder.compile(target="libplugin.so", verbose=True)
