# Workspace functions.

def save_plot_pickle(fname,vars,prefix='plotting/'):
    """
    Save pickle file for plotting in the local plotting directory.
    2014-03-07
    """
    import inspect
    import pickle
    import warnings

    frame = inspect.currentframe()
    backglobals = frame.f_back.f_globals
    locals = frame.f_locals
    d = {}

    for key in vars:
        if key not in backglobals.keys():
            warnings.warn('%s not in workspace.' % s)
        else:
            d[key] = backglobals[key]
    pickle.dump(d,open(prefix+fname,'wb'))
    return

def add_to_pickle(v,fname):
    """
        Add elements in dictionary to existing pickle.
    2014-05-30
    """
    import cPickle as pickle
    data = pickle.load(fname)
    for key in v.keys():
        data[key] = v[key]
    pickle.dump(data,open(fname,'wb'))
    return

def load_pickle(dir,squeeze_me=True,variable_names={}):
    """
        Load variables in pickle to global workspace using keys as variable names.
    2014-05-07
    """
    import inspect
    import cPickle

    frame = inspect.currentframe()
    backglobals = frame.f_back.f_globals

    if len(variable_names)==0:
        inData = cPickle.load(open(dir,"rb"))
    else:
        inData = cPickle.load(open(dir,"rb"))
        for i in inData.keys():
            if i not in variable_names:
                del inData[i]
    for key in inData.keys():
        backglobals[key] = inData[key]
    return inData.keys()

def save_vars(fname):
    """
    2013-08-06
        Save all int, float and numpy variables.
    """
    import inspect
    import scipy.io as sio
    import numpy as np

    mdict = {}
    frame = inspect.currentframe()
    backglobals = frame.f_back.f_globals
    for key in backglobals.keys():
        t = type(backglobals[key])
        if (not str.isupper(key) and not str.istitle(key)) and \
            (t==np.ndarray or t==float or t==int):
            exec('mdict['+'\''+key+'\'] = backglobals[\''+key+'\']')
            print key
    sio.savemat(fname,mdict)

    return

def load_mat_file(dir,squeeze_me=True,variable_names={}):
    import inspect
    import scipy.io as sio
    import numpy as np

    frame = inspect.currentframe()
    backglobals = frame.f_back.f_globals

    if len(variable_names)==0:
        inData = sio.loadmat(dir,squeeze_me=squeeze_me)
    else:
        inData = sio.loadmat(dir,squeeze_me=squeeze_me,variable_names=variable_names)
    for key in inData.keys():
        backglobals[key] = inData[key]
    return

def save_vars_v0(file):
    import shelve
    import inspect

    frame = inspect.currentframe()
    keys = []
    my_shelf = shelve.open(file,'n')
    for key in (frame.f_back.f_locals).keys():
        if not key.startswith('_'):
            try:
                if (not inspect.ismodule((frame.f_back.f_locals)[key])) and (not inspect.isroutine((frame.f_back.f_locals)[key])) and (not inspect.isclass((frame.f_back.f_locals)[key])):
                    print(type(key))
                    my_shelf[key] = (frame.f_back.f_locals)[key]
                    keys.append(key)
            except:
               print('ERROR shelving: {0}'.format(key))
    del frame
    print(len(keys))
    my_shelf.close()

def load_vars_v0(file):
    import shelve
    import inspect

    frame = inspect.currentframe()
    my_shelf = shelve.open(file)
    print("Loading...")
    for key in my_shelf:
        frame.f_back.f_globals[key] = my_shelf[key]
        print(key)
    del frame
    my_shelf.close()
