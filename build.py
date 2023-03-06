#导入cffi包，并且声明了外部函数接口(FFI)对象
import cffi
ffibuilder = cffi.FFI()
#header字符串中包含了需要调用的函数接口的定义
header = """
extern void save_mskf(float*,float*,float*,float*,float*,float*,float*,float*,float*,float*,float*,float*,float*,int,int,int,int,char*);

"""
#module字符串中包含了真正需要执行的Python程序。
#装饰器@ffi.def_extern用于标记hello_world函数
#extern void save_plot(float*,int,int,int,char*);
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
def save_mskf(u,v,w,t,q,p,dtt,dqv,dqc,dqr,dqi,dqs,rcv,nx,ny,nxy,nz,filename):
    filenam=ffi.string(filename).decode()
    u_array = my_infer_module.PtrAsarray(ffi,u,(nxy,nz))
    v_array = my_infer_module.PtrAsarray(ffi,v,(nxy,nz))
    w_array = my_infer_module.PtrAsarray(ffi,w,(nxy,nz))
    t_array = my_infer_module.PtrAsarray(ffi,t,(nxy,nz))
    q_array = my_infer_module.PtrAsarray(ffi,q,(nxy,nz))
    p_array = my_infer_module.PtrAsarray(ffi,p,(nxy,nz))

    dtt_array = my_infer_module.PtrAsarray(ffi,dtt,(nxy,nz))
    dqv_array = my_infer_module.PtrAsarray(ffi,dqv,(nxy,nz))
    dqc_array = my_infer_module.PtrAsarray(ffi,dqc,(nxy,nz))
    dqr_array = my_infer_module.PtrAsarray(ffi,dqr,(nxy,nz))
    dqi_array = my_infer_module.PtrAsarray(ffi,dqi,(nxy,nz))
    dqs_array = my_infer_module.PtrAsarray(ffi,dqs,(nxy,nz))

    rcv_array = my_infer_module.PtrAsarray(ffi,rcv,(nxy,1))
    np.savez(filenam,u=u_array,v=v_array,w=w_array,t=t_array,q=q_array,p=p_array,\
                    dtt=dtt_array,dqv=dqv_array,dqc=dqc_array,dqr=dqr_array,dqi=dqi_array,dqs=dqs_array,\
           rcv=rcv_array, nx=nx,ny=ny,nxy=nxy,nz=nz)
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
