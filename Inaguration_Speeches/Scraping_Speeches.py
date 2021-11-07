import urllib.request 
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


# webdriver and access website
driver = webdriver.Chrome( 'ENTER DIRECTORY OF YOUR SELENIUM CHROMEDRIVER.EXE HERE' )
driver.get( 'https://avalon.law.yale.edu/subject_menus/inaug.asp' )

# initialize lists
year = []
speech = []

year_list = [1789, 1793, 1797, 1801, 1805, 1809, 1813, 1817, 1821, 1825, 1829, 1833, 1837, 1841, 1845, 1849,
             1853, 1857, 1861, 1865, 1869, 1873, 1877, 1881, 1885, 1893, 1889, 1897, 1901, 1905, 1909, 1913, 
             1917, 1921, 1925, 1929, 1933, 1937, 1941, 1945, 1949, 1953, 1957, 1961, 1965, 1969, 1973, 1977,
             1981, 1985, 1989, 1993, 1997, 2001, 2005, 2009, 2013, 2017, 2021]

# Missing years: 1837, 1857, 1881, 1925, and all years after 2009
missing_speeches = [1837, 1857, 1881, 1925, 2013, 2017, 2021]

for i in year_list:
    driver.maximize_window()
    if i in missing_speeches:
        year.append(i)
        speech.append('')
        continue
    else:
        driver.find_element_by_link_text( str( i ) ).click()
        url = driver.current_url
        html = urllib.request.urlopen(url)
        htmlParse = BeautifulSoup(html, 'html.parser')
        year.append( i )
        individual_speech_paragraphs = []
        for para in htmlParse.find_all("p"):
            individual_speech_paragraphs.append( para.get_text() )
            merged_speech = ' '.join( individual_speech_paragraphs )
        speech.append( merged_speech )
        driver.back()
    
driver.close()

#party affiliation
party = ['Unaffiliated', 'Unaffiliated', 'Federalist', 'Democratic-Republican', 'Democratic-Republican', 'Democratic-Republican', 
         'Democratic-Republican', 'Democratic-Republican', 'Democratic-Republican', 'Democratic-Republican', 
         'Democratic', 'Democratic', 'Democratic', 'Whig', 'Democratic', 'Whig', 'Democratic',  'Democratic', 'Republican', 'National Union',
         'Republican', 'Republican', 'Republican', 'Republican', 'Democratic', 'Republican', 'Democratic', 'Republican', 'Republican', 
         'Republican', 'Republican', 'Democratic', 'Democratic', 'Republican', 'Republican', 'Republican', 'Democratic', 'Democratic', 
         'Democratic', 'Democratic', 'Democratic', 'Republican', 'Republican', 'Democratic', 'Democratic', 'Republican', 'Republican', 
         'Democratic', 'Republican', 'Republican', 'Republican', 'Democratic', 'Democratic', 'Republican', 'Republican', 'Democratic', 
         'Democratic', 'Republican', 'Democratic']

# create dataframe and export data
df = pd.DataFrame(
    {'Year': year,
     'Speech': speech,
     'Party': party
     })

## NOTE: You must manually add speeches to the years in the missing_speeches list. (Just copy and paste)
