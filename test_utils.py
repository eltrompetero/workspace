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
    @cached(10)
    def f(x):
        return x

    for i in range(20):
        f(i)

    assert f.cacheSize[0]==20
    assert np.array_equal([i for i in f.cache.values()], np.arange(10,20))
