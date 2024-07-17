# Copy and paste the below code 
# for could import normally like:
# import lib.*** ...

''' Add project path to sys.path V1.0'''
import os, sys
__dir_name = os.path.dirname(os.path.realpath(__file__))
for _ in range(5):
    if "lib" not in os.listdir(__dir_name):
        __dir_name =  os.path.dirname(__dir_name)
    else:
        if __dir_name not in sys.path:
            sys.path.insert(0, __dir_name)
        break
