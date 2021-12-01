# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28  2014

@author: yang
"""

import numpy as np
from numpy import ma
import scipy as sp
from scipy import stats
from sklearn.linear_model import LinearRegression

def corr(Y,x):
    '''calculate the correlation coefficients between Y and x along the last axis.'''
    if Y.size==x.size:
        X = x
    elif Y.shape[-1]==x.size:
        X = x.reshape((Y.ndim-1)*(1,)+(x.size,))
        # print Y.shape, x.shape,X.shape
    else:
        raise
    Xm = X.mean(axis=-1).reshape(X.shape[:-1]+(1,))
    Ym = Y.mean(axis=-1).reshape(Y.shape[:-1]+(1,))
    Xa = X - Xm
    Ya = Y - Ym
    Xvar = np.sum((X-Xm)**2,axis=-1)
    Yvar = np.sum((Y-Ym)**2,axis=-1)
    rNum = np.sum(Xa*Ya,axis=-1)
    rDen = np.sqrt(Xvar*Yvar)
    r = rNum/rDen
    # print r.shape
    return r
def get_t_from_two_samples(x1_mean, x2_mean, x1_square_mean, x2_square_mean, n1, n2, return_df=False):
    '''Calculate the t statistics in the two-sample t test given the mean, mean square, and sample size of the two samples. '''
    s1s1 = (x1_square_mean - x1_mean**2)*n1/(n1-1)
    s2s2 = (x2_square_mean - x2_mean**2)*n2/(n2-1)
    s = np.sqrt(
        s1s1/n1 + s2s2/n2
    )
    t = (x1_mean - x2_mean)/s

    if not return_df:
        return t
    else:
        df = (s1s1/n1 + s2s2/n2)**2 / ( (s1s1/n1)**2/(n1-1) + (s2s2/n2)**2/(n2-1) )
        return t, df

def p2r(p,df,twoside=True):
    '''Calculate r corresponding to the p value in the t test of correlation
         coefficient.
         t = sp.stats.t.ppf(1-p/2,df)
         t = r*sqrt(n-2)/sqrt(1-r**2)
         r = t*sqrt(1/(t**2 + n - 2))
    '''
    if twoside is True:
        t = sp.stats.t.ppf(1-p/2,df)
    else:
        t = sp.stats.t.ppf(1-p,df)
    r = t/np.sqrt(t**2 + df)
    return r
def p2t(p,df,twoside=True):
    '''Calculate the statistics t corresponding to the p value in the t test.
         t = sp.stats.t.ppf(1-p/2,df)
    '''
    if twoside is True:
        t = sp.stats.t.ppf(1-p/2,df)
    else:
        t = sp.stats.t.ppf(1-p,df)
    return t
def rms(Y,axis=None):
    rmsY = np.sqrt( (Y**2).mean(axis=axis) )
    return rmsY
def rmsa(Y,axis=None):
    Ya = Y.anom(axis=axis)
    rmsaY = np.sqrt( (Ya**2).mean(axis=axis) )
    return rmsaY
def corr_mon_lags(x1, x2=None, maxlags=12, maxleads=None, p=None):
    '''Calculate the correlation coeficient array of month-lags.
    x1: monthly time series;
    x2: monthly time series (equal to x1 by default);
    maxlags: max lags (18 by default);
    maxleads: max leads (equal to maxlags by default)'''
    if x2 is None:
        x2 = x1
    if maxleads is None:
        maxleads = maxlags
    if p is None:
        p = 0.05
    mon = np.arange(1, 13) # month vector
    lags = np.arange(-maxleads, maxlags+1) # lags vector
    r = np.zeros( (12, len(lags)) ) # corrcoef array
    r_p = np.zeros( (12, len(lags)) ) # corrcoef threshold array
    for i,_ in enumerate(mon):
        for j,lag in enumerate(lags):
            if lag<0: # x1 leads x2
                x1_ = x1[i::12]
                x2_ = x2[i-lag::12]
            else: # x2 leads x1; lag>=0
                x1_ = x1[i-12::-12]
                x2_ = x2[i-12-lag::-12]
            N = min(len(x2_), len(x2_))
            r[i,j] = np.corrcoef(x1_[:N], x2_[:N])[0,1]
            r_p[i, j] = p2r(p, df=N-1)
    return r, lags, mon, r_p
def regress(x, y, **kw):
    '''Regress y on x.

    ** parameters **
        x: array-like, shape (n_sample, n_feature).

        y: array-like, shape (n_sample, *grid_shape).

        normalize_x: bool, whether x is to be normalized (default False).

        normalize_y: bool, whether y is to be normalized (default False).
            If both normalize_x and normalize_y are True and n_feature == 1, then
            it is equivalent to calculate the correlation coefficient.

        normalize_xy: bool, whether both x and y are normalized (default False)

        cal_pvalue: bool, whether to calculate and return p values (default False).


    ** return **
        regression coefficients: array-like, shape (*grid_shape, n_feature).

        If cal_pvalue is True, then return both the regression coefficients and
        the associated p values.'''

    # normalize_x is False by default, and can be overridden by parameter `normalize`, then by `normalize_x`.
    normalize_x = kw.pop('normalize', False)
    normalize_x = kw.pop('normalize_x', normalize_x)
    # normalize_y is False by default, and can be overridden by parameter `normalize_y`.
    normalize_y = kw.pop('normalize_y', False)
    # normalize_x and normalize_y can be overridden by `normalize_xy`.
    normalize_xy = kw.pop('normalize_xy', False)
    if normalize_xy:
        normalize_x = normalize_xy
        normalize_y = normalize_xy
    cal_pvalue = kw.pop('cal_pvalue', False)
    n_jobs = kw.pop('n_jobs', -1)

    # x
    if x.ndim == 1:
        x = x[:,np.newaxis]
    assert x.ndim == 2, 'x must be two dimensional.'
    n_sample = x.shape[0]
    n_feature = x.shape[1]
    if normalize_x:
        x = ( x - x.mean(axis=0, keepdims=True))/x.std(axis=0, keepdims=True)

    # y
    if y.ndim == 1:
        y = y[:, np.newaxis]
    assert n_sample == y.shape[0], \
        'x and y must have the same sample size, which is along the first axis.'
    y_original_shape = y.shape
    # number of target (e.g. grid points in the lon-lat map)
    n_target = np.prod( y_original_shape[1:] )
    # reshape y to be two-dimensional
    y = np.reshape(y, (n_sample, n_target ) )
    # remove invalid values (e.g. NaN) of y
    Lvalid = ~ma.masked_invalid(y.sum(axis=0)).mask
    y = y[:, Lvalid]
    # normalize y if specified
    if normalize_y:
        y = ( y - y.mean(axis=0, keepdims=True))/y.std(axis=0, keepdims=True)

    # regression model
    model = LinearRegression(n_jobs=n_jobs, **kw)
    model.fit(x, y)

    # coefficients
    coef = np.zeros( (n_target, n_feature) ) + np.nan
    coef[Lvalid, :] = model.coef_
    coef = coef.reshape(y_original_shape[1:] + (n_feature,)).squeeze()

    if cal_pvalue:
        # calculate and return p values
        # see: https://gist.github.com/brentp/5355925
        # model explanation: http://reliawiki.org/index.php/Multiple_Linear_Regression_Analysis
        sse = np.sum( (model.predict(x) - y)**2, axis=0 )[:, np.newaxis]
        dof = n_sample - n_feature - 1
        xa = x - x.mean(axis=0, keepdims=True)
        ssx_inv = np.diagonal( np.linalg.inv( np.dot(xa.T, xa) ) )[np.newaxis,:]
        se = np.sqrt( sse * ssx_inv / dof )

        t = model.coef_ / se
        p_ = 2 * (1 - stats.t.cdf(np.abs(t), dof))
        p = np.zeros( (n_target, n_feature) ) + np.nan
        p[Lvalid, :] = p_
        p = p.reshape( y_original_shape[1:] + (n_feature,) ).squeeze()

        return coef, p
    else:
        return coef
def cal_pvalue_from_one_sample(x_mean, xx_mean, n, mu=0):
    '''Calculate the p values of the two-sample Student's t test given their mean, mean square and sample size. See:
        https://en.wikipedia.org/wiki/Student%27s_t-test'''
    s2 = (xx_mean - x_mean**2)*n/(n-1)
    s = np.sqrt( s2/n )
    t = ( x_mean -  mu )/s
    df = n - 1
    pvalue = ( 1 - sp.stats.t.cdf( np.abs(t), df=df ) ) * 2
    return pvalue
def cal_pvalue_from_two_samples(x1_mean, x2_mean,
    x1x1_mean, x2x2_mean, n1, n2):
    '''Calculate the p values of the two-sample Student's t test given their mean, mean square and sample size. See:
        https://en.wikipedia.org/wiki/Student%27s_t-test'''
    s1s1 = (x1x1_mean - x1_mean**2)*n1/(n1-1)
    s2s2 = (x2x2_mean - x2_mean**2)*n2/(n2-1)
    s = np.sqrt( s1s1/n1 + s2s2/n2 )
    t = (x1_mean - x2_mean)/s
    df = (s1s1/n1 + s2s2/n2)**2 \
        / ( (s1s1/n1)**2/(n1-1) + (s2s2/n2)**2/(n2-1) )
    pvalue = ( 1 - sp.stats.t.cdf( np.abs(t), df=df ) ) * 2
    return pvalue
