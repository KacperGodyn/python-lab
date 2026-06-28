import sys

print("sitecustomize: Applying Python 3.14 standard pickle dual-mode compatibility patch...", file=sys.stderr)

# Dual-mode patched _getattribute
def patched_getattribute(obj, name):
    if isinstance(name, str):
        # Called by cloudpickle or old pickle (expects string and returns tuple)
        path = name.split('.')
        is_string_path = True
    else:
        # Called by Python 3.14 standard pickle (expects sequence and returns single obj)
        path = name
        is_string_path = False
        
    parent = obj
    for subpath in path:
        if subpath == '<locals>':
            raise AttributeError("Can't get local attribute")
        parent = obj
        obj = getattr(obj, subpath)
        
    if is_string_path:
        return obj, parent
    else:
        return obj

# Patch standard pickle module directly!
import pickle
pickle._getattribute = patched_getattribute
print("sitecustomize: Patched standard pickle._getattribute successfully", file=sys.stderr)

# Also patch pyspark's internal cloudpickle modules
try:
    import pyspark.cloudpickle.cloudpickle as cp_module
    cp_module._getattribute = patched_getattribute
    print("sitecustomize: Patched cp_module successfully", file=sys.stderr)
except Exception as e:
    pass

try:
    import pyspark.cloudpickle.cloudpickle_fast as cp_fast
    cp_fast._getattribute = patched_getattribute
    print("sitecustomize: Patched cp_fast successfully", file=sys.stderr)
except Exception as e:
    pass

print("sitecustomize: Patch application complete!", file=sys.stderr)
