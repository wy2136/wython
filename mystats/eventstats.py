import numpy as np

def find_nonzero_groups(ts, min_len=1, min_interval=1):
    '''From a series of 1 and 0, find where the groups of 1 locates. For example,
    givien the time series [0,1,1,0,1,0], return [1, 4](starts of 1), [2, 1](lengths of groups).'''
    try:
        ts = ts.values
    except:
        pass
    ts = np.array(ts).astype('bool').astype('int')

    d = np.hstack((ts[0], np.diff(ts)))
    ivec = np.arange(d.size)
    istarts = ivec[d==1]
    iends = ivec[d==-1]-1
    if iends.size < istarts.size:
        iends = np.hstack((iends, ivec[-1]))

    # the minimum length of groups of ones equal or greater than min_len
    ilens = iends - istarts + 1
    istarts = istarts[ilens>=min_len]
    iends = iends[ilens>=min_len]

    # start of next group from the end of last group equal to or greater than min_interval (2 by default)
    if istarts.size > 1:
        j = 1
        while j < istarts.size:
            if istarts[j] - iends[j-1] - 1 < min_interval:
                # current group too close to the previous one: delete the current.
                istarts = np.delete(istarts, j)
                iends = np.delete(iends, j)
            else:
                # check the next group
                j += 1

    return istarts, iends-istarts+1
def test_find_nonzeros_groups():
    ts = [0, 1, 1, 0]
    istarts, ilens = find_nonzero_groups(ts)
    assert np.all( istarts == np.array([1,]) )
    assert np.all( ilens == np.array([2,]))

    ts = [1, 1, 1, 0]
    istarts, ilens = find_nonzero_groups(ts)
    assert np.all( istarts == np.array([0,]) )
    assert np.all( ilens == np.array([3,]))

    ts = [0, 1, 1, 1]
    istarts, ilens = find_nonzero_groups(ts)
    assert np.all( istarts == np.array([1,]) )
    assert np.all( ilens == np.array([3,]))

    ts = [0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1]
    istarts, ilens = find_nonzero_groups(ts)
    assert np.all( istarts == np.array([1, 3, 7, 13]) )
    assert np.all( ilens == np.array([1, 2, 3, 4]))
    istarts, ilens = find_nonzero_groups(ts, min_len=2)
    assert np.all( istarts == np.array([3, 7, 13]) )
    assert np.all( ilens == np.array([2, 3, 4]))
    istarts, ilens = find_nonzero_groups(ts, min_len=3)
    assert np.all( istarts == np.array([7, 13]) )
    assert np.all( ilens == np.array([3, 4]))
    istarts, ilens = find_nonzero_groups(ts, min_len=4)
    assert np.all( istarts == np.array([13]) )
    assert np.all( ilens == np.array([4]))
    istarts, ilens = find_nonzero_groups(ts, min_len=5)
    assert np.all( istarts == np.array([]) )
    assert np.all( ilens == np.array([]))
    istarts, ilens = find_nonzero_groups(ts, min_interval=2)
    assert np.all( istarts == np.array([1, 7, 13]) )
    assert np.all( ilens == np.array([1, 3, 4]))
    istarts, ilens = find_nonzero_groups(ts, min_interval=3)
    assert np.all( istarts == np.array([1, 7, 13]) )
    assert np.all( ilens == np.array([1, 3, 4]))
    istarts, ilens = find_nonzero_groups(ts, min_interval=4)
    assert np.all( istarts == np.array([1, 7]) )
    assert np.all( ilens == np.array([1, 3]))
    istarts, ilens = find_nonzero_groups(ts, min_interval=6)
    assert np.all( istarts == np.array([1, 13]) )
    assert np.all( ilens == np.array([1, 4]))
    istarts, ilens = find_nonzero_groups(ts, min_interval=11)
    assert np.all( istarts == np.array([1, 13]) )
    assert np.all( ilens == np.array([1, 4]))
    istarts, ilens = find_nonzero_groups(ts, min_interval=12)
    assert np.all( istarts == np.array([1,]) )
    assert np.all( ilens == np.array([1,]))
    istarts, ilens = find_nonzero_groups(ts, min_interval=13)
    assert np.all( istarts == np.array([1,]) )
    assert np.all( ilens == np.array([1,]))

    print('\n----\nOK!')
