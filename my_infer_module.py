# my_module.py
import numpy as np
import os,logging

# Create the dictionary mapping ctypes to np dtypes.
ctype2dtype = {}

# Integer types
for prefix in ('int', 'uint'):
    for log_bytes in range(4):
        ctype = '%s%d_t' % (prefix, 8 * (2**log_bytes))
        dtype = '%s%d' % (prefix[0], 2**log_bytes)
        # print( ctype )
        # print( dtype )
        ctype2dtype[ctype] = np.dtype(dtype)
# Floating point types
ctype2dtype['float'] = np.dtype('f4')
ctype2dtype['double'] = np.dtype('f8')

def generate_logger(log_file_path):
    #Create the logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    #Create handler for logging data to a file
    logger_handler = logging.FileHandler(log_file_path, mode = 'a')
    logger_handler.setLevel(logging.INFO)

    #Define format for handler
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    logger_handler.setFormatter(formatter)

    #Add logger in the handler
    logger.addHandler(logger_handler)

    return logger

#asarray函数使用CFFI的ffi对象转换指针ptr为给定形状的numpy数组
#def PtrAsarray(ffi, ptr, shape, shape_new = [], **kwargs):
def PtrAsarray(ffi, ptr, shape,  **kwargs):
    length = np.prod(shape)
    # Get the canonical C type of the elements of ptr as a string.
    T = ffi.getctype(ffi.typeof(ptr).item)
#   print("In my_module PtrAsarray")
#   print( T )
#   print( ffi.sizeof( T ) )

    if T not in ctype2dtype:
        raise RuntimeError("Cannot create an array for element type: %s" % T)

    a = np.frombuffer(ffi.buffer(ptr, length * ffi.sizeof(T)), ctype2dtype[T]).reshape(shape,**kwargs)
    shape_new=[1]        
#   if len(shape_new) == 1:
#       if len(shape) == 2:
#           a = a.reshape((shape_new[0], ))
            
#       elif len(shape) == 3:
#           a = a.reshape((shape_new[0], shape[0]))            
        
#   elif len(shape_new) > 1:
#       if len(shape) == 2:
#           a = a.reshape(shape)
#           a = a[shape_new[0]:-(shape_new[0]+1), shape_new[0]:-(shape_new[0]+1)]
#           a = a.reshape((shape_new[1], ))
#           
#       elif len(shape) == 3:
#           a = a.reshape(shape)            
#           a = a[shape_new[0]:-(shape_new[0]+1), shape_new[0]:-(shape_new[0]+1), :]    
#           a = a.reshape((shape_new[1], shape_new[2]))
            
    return a

def reshape_3d(Var, Var_x, Var_y, Var_z):
   # Var = Var.reshape((Var_x, Var_y, Var_z))
    Var = np.swapaxes(Var, 1, 2)
    Var = Var.reshape((Var_x*Var_z, Var_y))

    return Var
