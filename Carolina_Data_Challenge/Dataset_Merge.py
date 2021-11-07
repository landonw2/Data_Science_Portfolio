import pandas as pd
import numpy as np


##############################################################################
#                                                                            #
#                                 LOAD DATA                                  #
#                                                                            #
##############################################################################

svi = pd.read_csv(r'SVI_2014.csv')
nri = pd.read_csv(r'NRI Data/NRI_Table_CensusTracts.csv')


##############################################################################
#                                                                            #
#                                 DATA CLEANING                              #
#                                                                            #
##############################################################################

# add population density and area designation
svi['pop_density'] = svi['E_TOTPOP']/svi['AREA_SQMI']
svi['area_type'] = np.where((svi['pop_density'] > 1000) & (svi['E_GROUPQ']/svi['E_TOTPOP'] < 0.4), 'Urbanized Area', 'Rural')

# count of urban and rural
svi.groupby('area_type').size()

# remove columns with E_TOTPOP = 0 and SPL_THEMES = -999
svi = svi[(svi['E_TOTPOP'] != 0) & (svi['SPL_THEMES']!=-999)].reset_index()


##############################################################################
#                                                                            #
#                                Merge Datasets                              #
#                                                                            #
##############################################################################

combined = pd.merge(svi.iloc[:, np.r_[1,4:10,11:78,82:84,88:90,92:94,99:132,-1]], nri.iloc[:, np.r_[10:366,-1]], how = 'inner', left_on = 'FIPS', right_on = 'TRACTFIPS')
