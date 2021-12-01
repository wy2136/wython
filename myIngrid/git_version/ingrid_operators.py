# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24, 2015
 
@author: Wenchang Yang 
"""
from __future__ import print_function

# 
##### general functions
def get_months(season='Annual'):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
              'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    if season.lower()=='annual': # 12 months array
        months = months[:12]
    elif season in months: # season contains only one month
        months = [season]
    else: # season defined by consecutive month initials
        months_short = 'JFMAMJJASONDJFMAMJ'
        i = months_short.find(season)
        N = len(season)
        months = months[i:i+N]
    return months
# 
# ######## basic functions that generate a string of Ingrid commands wrapped in a list, e.g. '[T]average'
# ---- data selection
def grid(gridName,grid1,grid2,dgrid=1):
    '''Example: \n if gridName='X',grid1=30, grid2=50 and dgrid=1 \n then grid(gridName,grid1,grid2,dgrid) returns '/X/30/1/52/GRID'. '''
    return '/'+'/'.join( [str(s) for s in (gridName,grid1,dgrid,grid2,'GRID')] )
def range(dimName,r1,r2=None):
    '''Example: \n if dimName='T',r1='Jan 1979', r2='Dec 2012' \n then range(dimName,r1,r2) returns '/T(Jan 1979)(Dec 2012)RANGE'. '''
    if r2 is None:
        return '/' + dimName + '(' + str(r1) + ')RANGE'
    else:
        return '/' + dimName + '(' + str(r1) + ')(' + str(r2) + ')RANGE'
def values(dimName,*args):
    '''Example: \n if dimName='T',args=['Jan 1979', 'Dec 2012'] \n then values(dimName,*args) returns '/T(Jan 1979)(Dec 2012)VALUES'. '''
    return '/' + dimName + ''.join( ['('+str(arg)+')' for arg in args] ) + 'VALUES'
def step(dimName,N):
    '''Example: \n if dimName='T', N=3 \n then step(dimName,N) returns 'T/3/STEP'.'''
    return '/' + '/'.join( [dimName,str(N),'STEP'] )
def flag(comparisonString,value=0):
    '''Example: \n if comparisonString='gt' or '>', value=0 \n then flag(comparisonString,value) returns ['0','flaggt'].'''
    s = comparisonString
    if s in ['>','gt']:
        fs = 'flaggt'
    elif s in ['<','lt']:
        fs = 'flaglt'
    elif s in ['>=','ge']:
        fs = 'flagge'
    elif s in ['<=','le']:
        fs = 'flagle'
    else:
        print ("Please provide correct comparison string.")
        fs = None
    return '/' + str(value) + '/' + fs
def mask(comparisonString,value=0):
    '''Example: \n if comparisonString='gt' or '>', value=0 \n then mask(comparisonString,value) returns '/0/maskgt'.'''
    s = comparisonString
    if s in ['>','gt']:
        fs = 'maskgt'
    elif s in ['<','lt']:
        fs = 'masklt'
    elif s in ['>=','ge']:
        fs = 'maskge'
    elif s in ['<=','le']:
        fs = 'maskle'
    else:
        print ("Please provide correct comparison string.")
        fs = None
    return '/' + str(value) + '/' + fs
def maskrange(n1,n2):
    '''return '/' + '/'.join([str(n1), str(n2), 'maskrange']) '''
    return  '/' + '/'.join([str(n1), str(n2), 'maskrange'])
def masknotrange(n1,n2):
    '''return '/' + '/'.join([str(n1), str(n2), 'masknotrange']) '''
    return '/' + '/'.join([str(n1), str(n2), 'masknotrange'])
# ---- arithmetic
def get_arith_name_list():
    '''return ['add','sub','mul','div','sqrt','eexp','ln','log']'''
    return ['add','sub','mul','div','sqrt','eexp','ln','log']
def arith(name):
    if name in get_arith_name_list():
        return '/' + name
    else:
        print ("Please select correct arithmetic operators from:\n ",
            get_arith_name_list()
        )
def num(aNum):
    '''return '/' + str(aNum) '''
    return '/' + str(aNum)
def add(aNum=None):
    ''' '/' + str(aNum) + '/' + 'add' '''
    if aNum is not None:
        return '/' + str(aNum) + '/add'
    else:
        return '/add'
def sub(aNum=None):
    ''' '/' + str(aNum) + '/' + 'sub' '''
    if aNum is not None:
        return '/' + str(aNum) + '/sub'
    else:
        return '/sub'
def mul(aNum=None):
    ''' '/' + str(aNum) + '/' + 'mul' '''
    if aNum is not None:
        return '/' + str(aNum) + '/mul'
    else:
        return '/mul'
def div(aNum=None):
    ''' '/' + str(aNum) + '/' + 'div' '''
    if aNum is not None:
        return '/' + str(aNum) + '/div'
    else:
        return '/div'
def sqrt():
    '''return '/sqrt' '''
    return '/sqrt'
def exp():
    '''return '/eexp' '''
    return '/eexp'
def power():
    '''return '/exch/ln/mul/eexp'''
    return '/exch/ln/mul/eexp'
# ---- statistics
def average(*dimNames):
    '''return '[' + ' '.join(dimNames) + ']average' '''
    if 'Y' in dimNames:
        return '/{Y/cosd}[' + '/'.join(dimNames) + ']weighted-average'
    else:
        return '/[' + ','.join(dimNames) + ']average'
def sum(*dimNames):
    '''return '[' + ' '.join(dimNames) + ']sum' '''
    return '/[' + ','.join(dimNames) + ']sum'
def runningAverage(dimName,N):
    '''return '/' + '/'.join( [dimName, str(N), 'runningAverage'] )'''
    return '/' + '/'.join( [dimName, str(N), 'runningAverage'] )
def boxAverage(dimName,N):
    '''return '/' + '/'.join( [dimName, str(N), 'boxAverage'] )'''
    return '/' + '/'.join( [dimName, str(N), 'boxAverage'] )  
def climatology(typeString='monthly'):
    '''Monthly (or pentadly) climatology of var based on all selected years. '''
    if typeString=='monthly':
        return '/yearly-climatology'
    elif typeString=='pentad':
        return '/T/pentadAverage/T/73/splitstreamgrid' + average('T2')
def yearly_anomalies():
    '''yearly-anomalies: var with monthly climatology subtracted. 
   See:  http://iridl.ldeo.columbia.edu/dochelp/Documentation/details/index.html?func=yearly-anomalies.'''
    return '/yearly-anomalies'
def rmsover(*dimNames):
    '''return '[' + ' '.join(dimNames) + ']rmsover' '''
    return '/[' + ','.join(dimNames) + ']rmsover'
def rmsaover(*dimNames):
    '''return '[' + ' '.join(dimNames) + ']rmsaover' '''
    return '/[' + ','.join(dimNames) + ']rmsaover'
def maxover(*dimNames):
    '''return '[' + ' '.join(dimNames) + ']maxover' '''
    return '/[' + ','.join(dimNames) + ']maxover'
def minover(*dimNames):
    '''return '[' + ' '.join(dimNames) + ']minover' '''
    return '/[' + ','.join(dimNames) + ']minover'
def detrend(dimName='T'):
    '''return '/[' + dimName + ']detrend-bfl' '''
    return '/[' + dimName + ']detrend-bfl'
# ---- advanced analysis
def standardize(dimName='T'):
    '''return '/[' + dimName + ']standardize' '''
    return '/[' + dimName + ']standardize'
def correlate(dimName='T'):
    '''return '/[' + dimName + ']correlate' '''
    return '/[' + dimName + ']correlate'
def ddx(xName='X',yName='Y'):
    '''return '/' + '/'.join( ['a:',xName,'partial',yName,'cosd','div',xName,':a:','.'+xName,'REGRID',':a',
        '110000.','div'] )'''
    return '/' + '/'.join ( ['a:',xName,'partial',yName,'cosd','div',xName,':a:','.'+xName,'REGRID',':a',
        '110000.','div'] )
def ddy(yName='Y'):
    '''return ['a:',yName,'partial',yName,':a:','.'+yName,'REGRID',':a','110000.','div']'''
    return '/' + '/'.join( ['a:',yName,'partial',yName,':a:','.'+yName,'REGRID',':a','110000.','div'] )
def ddp(pName='P',pUnit='hPa'):
    ''' '/' + '/'.join( ['a:',pName,'partial',pName,':a:','.'+pName,'REGRID',':a'] ) '''
    chain = ['a:',pName,'partial',pName,':a:','.'+pName,'REGRID',':a']
    if pUnit in ['hPa','mb']:
        chain += ['100.','div']
    return '/' + '/'.join(chain)
def ddt(tName='T',timeStepUnit='month'):
    ''' '/' + '/'.join( ['a:',tName,'partial',tName,':a:','.'+tName,'REGRID',':a'] )'''
    chain = ['a:',tName,'partial',tName,':a:','.'+tName,'REGRID',':a']
    if timeStepUnit in ['month','monthly']:
        chain += ['30.','div','86400.','div']
    elif timeStepUnit in ['day','daily']:
        chain += ['86400.','div']
    return '/' + '/'.join(chain)
# ---- miscellaneous
def renameGrid(oldName,newName):
    '''return '/' + oldName + '(' + newName + ')renameGRID' '''
    return '/' + oldName + '(' + newName + ')renameGRID'
def replaceGrid(gridName,units,grid1,grid2,dgrid):
    return '/' + '/'.join( [gridName,'('+gridName+')', '('+units+')', 'ordered', 
        str(grid1), str(dgrid), str(grid2), 'NewEvenGRID', 'replaceGRID'] )
def select(vname):
    '''return '/.' + vname '''
    return '/.' + vname
def param(name):
    return '/' + name
def units(name):
    '''return '/units(' + name + ')def' '''
    return '/units(' + name + ')def'
    
def dup():
    '''return '/dup' '''
    return '/dup'
def exch():
    '''return '/exch' '''
    return '/exch'
def nip():
    '''return '/nip' '''
    return '/nip'
def appendstream():
    '''return '/appendstream' '''
    return '/appendstream'
def define(dataString,name):
    ''' '//' + name + '{' + dataString + '}def' '''
    return '//' + name + '{' + dataString + '}def'
def readdods(dataurl):
    '''return ['(' + dataurl + ')readdods']'''
    if '%' in dataurl:
        dataurl = dataurl.replace('%','%25')
    if 'columbia.edu' in dataurl and not dataurl.endswith('/dods'):
        dataurl += '/dods'
    return '/(' + dataurl + ')readdods'
def T_splitstreamgrid(N=12):
    '''return '/' + '/'.join( ['T',str(N),'splitstreamgrid'] )'''
    return '/' + '/'.join( ['T', str(N), 'splitstreamgrid'] )
#
# ---- miscellaneous
def shiftdata(dim_name, *args):
    '''Ingrid shiftdata command. See http://iridl.ldeo.columbia.edu/dochelp/Documentation/details/index.html?func=shiftdata'''
    return '/'+dim_name + '/' + '/'.join([str(arg) for arg in args])
def renameGrid(oldName,newName):
    '''return '/' + oldName + '(' + newName + ')renameGRID' '''
    return '/' + oldName + '(' + newName + ')renameGRID'
def replaceGrid(gridName,units,grid1,grid2,dgrid):
    return '/' + '/'.join( [gridName,'('+gridName+')', '('+units+')', 'ordered', 
        str(grid1), str(dgrid), str(grid2), 'NewEvenGRID', 'replaceGRID'] )
def select(vname):
    '''return '/.' + vname '''
    return '/.' + vname
def param(name):
    return '/' + name
def units(name):
    '''return '/units(' + name + ')def' '''
    return '/units(' + name + ')def'
    
def dup():
    '''return '/dup' '''
    return '/dup'
def exch():
    '''return '/exch' '''
    return '/exch'
def nip():
    '''return '/nip' '''
    return '/nip'
def appendstream():
    '''return '/appendstream' '''
    return '/appendstream'
def define(dataString,name):
    ''' '//' + name + '{' + dataString + '}def' '''
    return '//' + name + '{' + dataString + '}def'
def readdods(dataurl):
    '''return ['(' + dataurl + ')readdods']'''
    if '%' in dataurl:
        dataurl = dataurl.replace('%','%25')
    if 'columbia.edu' in dataurl and not dataurl.endswith('/dods'):
        dataurl += '/dods'
    return '/(' + dataurl + ')readdods'
def T_splitstreamgrid(N=12):
    '''return '/' + '/'.join( ['T',str(N),'splitstreamgrid'] )'''
    return '/' + '/'.join( ['T', str(N), 'splitstreamgrid'] )
#
# ######## complex functions based on the basic functions
def std(*dim_names):
    '''Multiply rmsaover by sqrt( N/(N-1) ).'''
    s = dup() \
        + '/dataflag' + sum(*dim_names) + dup() + sub(1) + div() + sqrt() \
        + exch() + rmsaover(*dim_names) \
        + mul()
    return s
def anomaly(*dimNames):
    return dup() + average(*dimNames) + sub()
def eof(eigval=None, option=None):
    '''return '/{Y/cosd}[X/Y][T]svd' '''
    # default option is Ss, except when eigval == 'all'
    if eigval == 'all' and option is None:
        option = 'evaln'
    elif option is None:
        option = 'Ss'
    s = '/{Y/cosd}[X/Y][T]svd'
    if eigval is not None:
        if option in ['Ss', 'spatial structure']:
            s = ''.join([
                s, select('Ss'), values('ev', eigval), average('ev')
            ])
        elif option in ['Ts', 'time series']:
            s = ''.join([
                s, select('Ts'), values('ev', eigval), average('ev')
            ])
        elif option in ['evaln', 'normalized eigen value']:
            if eigval == 'all':
                s = ''.join([
                    s, select('evaln')
                ])
            else:
                s = ''.join([
                    s, select('evaln'), values('ev', eigval), average('ev')
                ])
    return s
def trend(dimName):
    s = ''.join([
        dup(), detrend(dimName), sub(),
        dup(), values(dimName, 'last'), 
        exch(), values(dimName, 'first'), 
        sub()
    ])
    return s
def season_clim(season='annual', yearRange=(1979,2008), xgrid=(0,360,2), ygrid=(-90,90,2), isSquared=False):
    '''Seasonal (including annual) climatology over specified years. '''
    # get time range
    months = get_months(season)
    Nmon = len(months)
    tRange = (
        ' '.join([months[0], str(yearRange[0])]),
        ' '.join([months[-1], str(yearRange[-1])])
    )
    s = ''.join([
        range('T', *tRange),
        runningAverage('T', Nmon), step('T', 12), average('T'),
        grid('X', *xgrid), grid('Y', *ygrid),
    ])
    if isSquared: # squared before time average, useful in stats test
        s = s.replace(
            average('T'),
            dup() + mul() + average('T')
        )
    return s
def season_series(season=None, yearRange=None, xgrid=(0,360,2), ygrid=(-90, 90,2)):
    '''Spatially averaged seasonal time series. '''
    s = ''.join([
        grid('X', *xgrid), grid('Y', *ygrid), average('X', 'Y'),
    ])
    if yearRange is not None:
        s += range('T', str(yearRange[0]), str(yearRange[-1]))
    if season is not None:
        months = get_months(season)
        Nmon = len(months)
        s = ''.join([
            s,
            range('T', months[0], months[-1]),
            runningAverage('T', Nmon), step('T', 12)
        ])
    return s
def mask_of_EA(xgrid=(30,52,2), ygrid=(-10,12,2), isReadingDods=False):
    '''prMAM>prJF and prMAM>prJJAS and prAnnual<2mm/day'''
    gpcc = '/SOURCES/.WCRP/.GCOS/.GPCC/.FDP/.version6/.0p5/.prcp/30/div'
    pr_EA_climatology = gpcc + range('T', 'Jan 1979', 'Dec 2009') \
            + grid('X', *xgrid) + grid('Y', *ygrid) \
            + climatology();
    EA_mask = define(pr_EA_climatology,'prEAClim') \
            + param('prEAClim') \
            + range('T', 'Mar-May') + average('T') \
            + param('prEAClim') \
            + range('T', 'Jun-Sep') + average('T') \
            + sub() \
            + mask('lt',0) + mul(0) \
            + param('prEAClim') \
            + range('T', 'Mar-May') + average('T') \
            + param('prEAClim') \
            + range('T', 'Jan-Feb') + average('T') \
            + sub() \
            + mask('lt',0) + mul(0) \
            + add() \
            + param('prEAClim') \
            + average('T') + mask('gt',2) + mul(0) \
            + add()
    if isReadingDods:
        dodsurl = 'http://iridl.ldeo.columbia.edu/expert' + define(EA_mask,'EAmask') + param('EAmask') + dods()
        return readdods(dodsurl) + sel('prcp')
    else:
        return define(EA_mask,'EAmask') + param('EAmask')
def mask_of_land(xgrid=(0,359,2),ygrid=(-90,90,2),server='iri'):
    if server=='iri':
        dataPath = '/SOURCES/.NASA/.ISLSCP/.GDSLAM/.Miscellaneous/.land_sea_mask'
    elif server=='strega':
        dataPath = '/CMIP5/.byScenario/.fixed/.atmos/.GFDL-HIRAM-C180/.sftlf.nc/.sftlf'
        dataPath += renameGrid('lon','X') + renameGrid('lat','Y')
    elif server=='kage':
        dataPath = '/home .OTHER .mm_analysis .run1 .models .m24 .fixed .sftlf.nc .sftlf'
        dataPath += renameGrid('lon','X') + renameGrid('lat','Y') + div(100)
    msk = dataPath + grid('X',*xgrid) + grid('Y',*ygrid) + mask('lt',0.5) + mul(0)
    return msk
def mask_of_ocean(xgrid=(0,359,2),ygrid=(-90,90,2),server='iri'):
    if server=='iri':
        dataPath = '/SOURCES/.NASA/.ISLSCP/.GDSLAM/.Miscellaneous/.land_sea_mask'
    elif server=='strega':
        dataPath = '/CMIP5/.byScenario/.fixed/.atmos/.GFDL-HIRAM-C180/.sftlf.nc/.sftlf'
        dataPath += renameGrid('lon','X') + renameGrid('lat','Y')
    elif server=='kage':
        dataPath = '/home .OTHER .mm_analysis .run1 .models .m24 .fixed .sftlf.nc .sftlf'
        dataPath += renameGrid('lon','X') + renameGrid('lat','Y') + div(100)
    msk = dataPath + grid('X',*xgrid) + grid('Y',*ygrid) + mask('gt',0.5) + mul(0)
    return msk
def ta2q_star(P='P'):
    '''Transform temperature into saturated specific humidity.'''
    s = num(-1) + exch() + div() \
        + num(1) + num(273.15) + div() + add() \
        + mul(2500*1000) + div(461) \
        + exp() \
        + mul(6.11) + '/' + P + div() \
        + mul(0.622)
    return s

