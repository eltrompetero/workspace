# Workspace functions.
import numpy as np
import hickle,inspect,pickle
import os
import subprocess

# -------#
# Hickle #
# -------#
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


# -------#
# Pickle #
# -------#

def save_plot_pickle(fname,vars,prefix='plotting/',notDill=False):
    """
    Save pickle file for plotting in the local plotting directory. Pickle extension not included by default in fname.
    2014-03-07

    Params:
    -------
    fname (str)
        name of file including suffix
    vars (dict)
        dictionary of variables
    prefix (str)
        name of directory in current directory in which to place pickles
    """
    import inspect
    if notDill:
        import pickle
    else:
        import dill as pickle
    import warnings

    frame = inspect.currentframe()
    backglobals = frame.f_back.f_globals
    locals = frame.f_locals
    d = {}

    for key in vars:
        if key not in list(backglobals.keys()):
            warnings.warn('%s not in workspace.' % s)
        else:
            d[key] = backglobals[key]
    pickle.dump(d,open(prefix+fname,'wb'),-1)
    return

def add_to_pickle(v,fname):
    """
        Add elements in dictionary to existing pickle.
    2014-08-23
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
    return

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

