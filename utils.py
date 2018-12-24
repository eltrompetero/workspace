# =============================================================================================== #
# Handy workspace functions.
# Written by Eddie Lee, edlee@alumni.princeton.edu
# =============================================================================================== #
import numpy as np
import hickle, inspect, pickle, dill
import os
import subprocess
from functools import wraps
from pickle import PicklingError


# ========== #
# Decorators
# ========== #
def cached(iarg=None, maxsize=128, iprint=False, cache_pickle=None, write=True):
    """Save all last calls to function. This gives access to the cache dict unlike
    functools.lru_cache(). The outermost function is necessary to pass in keywork args
    into the decorator constructor which is really outer_wrap().
    
    NOTE: use inspect.getargspec to read in default keyword arguments as part of call in
    cache

    Parameters
    ----------
    maxsize : int
        Max number of elements allowed in cache.
    iprint : bool, False
        Print when adding to cache.
    cache_pickle : str, None
        Pass in file name from which to load cache.
    write : bool, True
        If True, write cache to file. Only works if cache_pickle is specified.
    """

    def outer_wrap(func):
        # try to load cache from given file
        cache = {}
        cacheSize = [0]
        if not cache_pickle is None:
            try:
                data = pickle.load(open(cache_pickle, 'rb'))
                # must explicitly load each element because hashes are randomized per session
                for k in data['cache'].keys():
                    cache[k] = data['cache'][k]
                cacheSize = [len(cache.keys())]
                if iprint: print("Loaded cache from file.")
            except FileNotFoundError:
                if iprint: print("Pickled cache file not found.")
            except KeyError:
                if iprint: print("Invalid pickled cache file.")

        @wraps(func)  # this makes inner function accessible from outside
        def wrapper(*args, **kwargs):
            # get all default kwargs for func
            argspec = inspect.getfullargspec(func)
            if not argspec.defaults is None:
                # if default kwarg is not specified then put in default kwarg value
                argspeckwargs = argspec.args[-len(argspec.defaults):]
                for i,k in enumerate(argspeckwargs):
                    if not k in kwargs.keys():
                        kwargs[k] = argspec.defaults[i]

            try:
                return cache[(args, frozenset(kwargs))]
            except KeyError:
                if iprint: print("Adding to cache.")
                cache[(args,frozenset(kwargs.items()))] = result = func(*args, **kwargs)
                cacheSize[0] += 1

                if cacheSize[0]>maxsize:
                    if iprint: print("Deleting from cache.")
                    del cache[next(iter(cache.keys()))]
                    cacheSize[0] -= 1

                if write and cache_pickle:
                    try:
                        pickle.dump({'cache':cache}, open(cache_pickle,'wb'), -1)
                    except AttributeError:
                        dill.dump({'cache':cache}, open(cache_pickle,'wb'), -1)
                    except PicklingError:
                        dill.dump({'cache':cache}, open(cache_pickle,'wb'), -1)
                    except FileNotFoundError:
                        if iprint: print("Cannot write to cache file.")
                return result
        wrapper.cache = cache
        wrapper.cacheSize = cacheSize
        return wrapper
    
    # if a kwarg was not set, just return a simple decorator
    if callable(iarg):
        return outer_wrap(iarg)
    return outer_wrap


# ------------------------ #
# Saving workspace objects #
# ------------------------ #
def hickle_pickle(dictOfVars,fileName,compression='lzf'):
    """
    2016-03-22
    """
    if os.path.isfile(fileName):
        os.remove(fileName)
    hickle.dump(dictOfVars,fileName,compression=compression,mode='a')
    return

def load_hickle(dr,squeeze_me=True,variable_names={}):
    """
    Load variables in hickle to global workspace using keys as variable names.
    2016-03-22
    """
    frame = inspect.currentframe()
    backglobals = frame.f_back.f_globals

    if len(variable_names)==0:
        inData = hickle.load(dr)
    else:
        inData = hickle.load(dr)
        for i in list(inData.keys()):
            if i not in variable_names:
                del inData[i]
    for key in list(inData.keys()):
        backglobals[key] = inData[key]
    return list(inData.keys())

def pickle_temp(var_dict):
    """Pickle given variables into local directory with a unique temp file name using uuid.

    Parameters
    ----------
    var_dict : dict
    """
    import pickle
    from os import getcwd
    from uuid import uuid4
    
    fname='%s/temp_%s.p'%(getcwd(),str(uuid4()).replace('-',''))
    pickle.dump(var_dict,open(fname,'wb'),-1)

    print(fname)

def add_to_pickle(v,fname):
    """
    Add elements in dictionary to existing pickle.
    """
    import pickle as pickle
    import warnings

    try:
        data = pickle.load(open(fname,'rb'))
    except err:
        warnings.warn("Pickle file did not exist. Creating it.")
        data = {}
    for key in list(v.keys()):
        if key in list(data.keys()):
            warnings.warn("Overwriting variable \"%s.\"" %key)
        data[key] = v[key]
    out = open(fname,'wb')
    pickle.dump(data,out,-1)
    out.close()

def load_pickle(dr,date=False,variable_names={}):
    """
    Load variables in pickle to global workspace using keys as variable names.

    Parameters:
    -----------
    dr : str
    variable_names : dict
    date : bool,False
        Print file mod date if True.
    """
    if date:
        process = subprocess.Popen(('date -r %s'%dr).split(), stdout=subprocess.PIPE)
        output,error = process.communicate()
        print(output)
    frame = inspect.currentframe()
    backglobals = frame.f_back.f_globals
    
    try:
        try:
            inData=pickle.load(open(dr,'rb'))
        except UnicodeDecodeError:
            inData=pickle.load(open(dr,'rb'),encoding='latin1')
        if len(variable_names)>0:
            for i in list(inData.keys()):
                if i not in variable_names:
                    del inData[i]
        for key in list(inData.keys()):
            backglobals[key] = inData[key]
        return list(inData.keys())
    except AttributeError:
        import dill
        if len(variable_names)==0:
            inData = dill.load(open(dr,"rb"))
        else:
            inData = dill.load(open(dr,"rb"))
            for i in list(inData.keys()):
                if i not in variable_names:
                    del inData[i]
        for key in list(inData.keys()):
            backglobals[key] = inData[key]
        return list(inData.keys())

def load_mat_file(dir,squeeze_me=True,variable_names={},disp=True):
    """
    Load .mat file variables directly into workspace.
    """
    import inspect
    import scipy.io as sio
    import numpy as np

    frame = inspect.currentframe()
    backglobals = frame.f_back.f_globals

    if len(variable_names)==0:
        inData = sio.loadmat(dir,squeeze_me=squeeze_me)
    else:
        inData = sio.loadmat(dir,squeeze_me=squeeze_me,variable_names=variable_names)
    for key in list(inData.keys()):
        backglobals[key] = inData[key]
    if disp:
        print(list(inData.keys()))
    return

