
from HggStarHelpers import weightscale_hyystar,SherpaKfactor1p3,SF_80fb,SF_139fb,YEAR
from HggStarHelpers import GetFbForMCNormalization

treename = 'CollectionTree'

theyear = YEAR.y201516
fb = GetFbForMCNormalization(theyear)

def weightscale(tfile) :
    weight = weightscale_hyystar(tfile)

    if theyear == YEAR.y20151617 :
        weight = weight* SF_80fb(tfile)

    if theyear == YEAR.y2015161718 :
        weight = weight* SF_139fb(tfile)

    return weight

