from .utils import *


def test_cached():
    # test use of maxsize setting
    @cached
    def f(x):
        return x

    for i in range(20):
        f(i)
    
    assert np.array_equal([i for i in f.cache.values()], np.arange(20))

    # test use of maxsize setting
    @cached(maxsize=10)
    def f(x):
        return x

    for i in range(20):
        f(i)

    assert f.cacheSize[0]==10
    assert np.array_equal([i for i in f.cache.values()], np.arange(10,20))

    # test use of function with a kwarg
    @cached(maxsize=10)
    def f(x, a=1, b=2):
        return x

    f(0, 1, 3)
    assert f.cache[((0,), frozenset({'a':1,'b':3}.items()))]==0

    for i in range(1,20):
        f(i, b=3)
    
    assert f.cacheSize[0]==10
    assert np.array_equal([i for i in f.cache.values()], np.arange(10,20))
