import pprint
import requests
import pandas as pd
from datetime import datetime
from datetime import timedelta
from datetime import date

# Setting Variables - Can be any city and state/country
loc = [\
  [ 'Anchorage', 'Alaska' ],\
  [ 'Chennai', 'India' ],\
  [ 'Jiangbei', 'China' ],\
  [ 'Kathmandu', 'Nepal' ],\
  [ 'Kothagudem', 'India' ],\
  [ 'Lima', 'Peru' ],\
  [ 'Manhasset', 'New York' ],\
  [ 'Mexico City', 'Mexico' ],\
  [ 'Nanaimo', 'Canada' ],\
  [ 'Peterhead', 'Scotland' ],\
  [ 'Polevskoy', 'Russia' ],\
  [ 'Round Rock', 'Texas' ],\
  [ 'Seoul', 'South Korea' ],\
  [ 'Solihull', 'England' ],\
  [ 'Tel Aviv', 'Israel' ]\
]

# Initializing important variables

# 8 blocks in 1 day    
blocksinday = 8

# Temperature converstion from Kelvin to Celcius (divide by this #)
temp_convertor = 273.15

# Variable for iterations
a = 0

# Number of days from Day 2 - Day 4
days = 3

# Variable for Day 5
lastday = 1

# Variable for Day 1
firstday = 1
 
# Initializing a DF where values will be stored at end
weather_df = pd.DataFrame(dtype = float)

# API Key variable (you will need your own)
api_key = 'INSERT YOUR OWN API KEY'

# URL for API pull
URL1 = 'https://api.openweathermap.org/data/2.5/forecast?'
URL2 = 'q='
URL3 = ','
URL4 = '&appid='

# Beginning of the process where we first begin with taking the first location
# and pulling the data from the API for that location
for location in range(len(loc)):
    URL = URL1+URL2+str(loc[a][0])+URL3+str(loc[a][1])+URL4+api_key
    
    response = requests.get( URL )
    if response.status_code == 200:      # Success
        data = response.json()
    
        printer = pprint.PrettyPrinter( width=80, compact=True )
        #printer.pprint( data[ 'list' ][ 0 ] )

        # Initializing starting blocks
        tomorrowstartblock = 0
        startblock = 0
        
        # Creating empty lists for the end variables I want
        min_avg = []
        max_avg = []
        min_1 = []
        min_2 = []
        min_3 = []
        min_4 = []
        min_5 = []
        max_1 = []
        max_2 = []    
        max_3 = []
        max_4 = []
        max_5 = []
        min_avg = []
        max_avg = []


        # Get current data (EST)
        cur_dt = date.today()
        
        # Search for the first block that starts "tomorrow"
        for i in range( 0, len( data[ 'list' ] ) ):
        
          # Convert the current block's date text to a datetime object
          dt_str = data[ 'list' ][ i ][ 'dt_txt' ]
          dt_tm = datetime.strptime( dt_str, '%Y-%m-%d %H:%M:%S' )
        
          # Offset by the timezone offset to get local time, not UTC time
          tz_offset = data[ 'city' ][ 'timezone' ]
          dt_tm = dt_tm + timedelta( seconds=tz_offset )
        
          # Convert the current block's date text to a datetime object - this 
          # will later be used to keep store the current date/time
          dt_str_const = data[ 'list' ][0][ 'dt_txt' ]
          dt_tm_const = datetime.strptime( dt_str_const, '%Y-%m-%d %H:%M:%S' )

          # Offset by the timezone offset to get local time, not UTC time for constant
          tz_offset_const = data[ 'city' ][ 'timezone' ]
          dt_tm_const = dt_tm_const + timedelta( seconds=tz_offset_const )  
        
          # If our day is the same as the block's day, the block is for
          # today and NOT tomorrow, so keep searching, otherwise break
          # out of the loop
        
          if cur_dt.day == dt_tm.day:
            continue
          else:
            startblock = i
            break
            

        # Same process as above but to get tomorrow's start block
        for i in range( 0, len( data[ 'list' ] ) ):
            if cur_dt.day != dt_tm.day:
        
              #  Convert the current block's date text to a datetime object
              dt_str = data[ 'list' ][ i ][ 'dt_txt' ]
              dt_tm = datetime.strptime( dt_str, '%Y-%m-%d %H:%M:%S' )
            
              #  Offset by the timezone offset to get local time, not UTC time
              tz_offset = data[ 'city' ][ 'timezone' ]
              dt_tm = dt_tm + timedelta( seconds=tz_offset )
            
              #  Setting Constant Current Local Time to Determine Startblock
    
              dt_str_const = data[ 'list' ][0][ 'dt_txt' ]
              dt_tm_const = datetime.strptime( dt_str_const, '%Y-%m-%d %H:%M:%S' )
       
              tz_offset_const = data[ 'city' ][ 'timezone' ]
              dt_tm_const = dt_tm_const + timedelta( seconds=tz_offset_const ) 
              
              if dt_tm_const.day == dt_tm.day:
                continue
              else:
                tomorrowstartblock = 8 - i
                break
            else:
              break

        # Calculating the number of blocks that remain for Day 5    
        lastdayblocks = len(data['list']) - (8*4) - startblock
        
        # Calculating number of blocks "today"
        firstdayblocks = blocksinday - startblock
        
        # Calculating starting block for Day 1
        tomorrowfirstdayblocks = blocksinday - tomorrowstartblock

##########################################################################
#                                                                        #                                        
#                        IF NOT ALREADY TOMORROW                         #
#                                                                        #
##########################################################################

# Day 1
        if tomorrowstartblock == 0:
            for x in range(firstday): # firstday = 1, so iterate 1 time.
                # initializing dataframe. Setting extremely high min and low max for first comparison
                temp_df = pd.DataFrame()
                temp_min_final = 100000
                temp_max_final = -100000
                
                for i in range(blocksinday): # blocksinday = 8, so iterate here 8 times
                    
                    # Loops through each block and compares the min and max. Only stores
                    # if new min is lower than whatever min is currently stored and if 
                    # new max is higher than whatever max is currently stored
                    if ((data['list'][startblock]['main']['temp_min']) - temp_convertor) < temp_min_final:
                        temp_min_final = ((data['list'][startblock]['main']['temp_min']) - temp_convertor)
                    
                    if ((data['list'][startblock]['main']['temp_max']) - temp_convertor) > temp_max_final:
                        temp_max_final = ((data['list'][startblock]['main']['temp_max']) - temp_convertor)
                    
                    # Increase the block we iterate through
                    startblock = startblock + 1
                    
                    # Final storage to min_1 and max_1 lists
                    if x == 0 and i == (blocksinday - 1):
                        min_1 = temp_min_final
                        max_1 = temp_max_final
                     
# Day 2-4
            for x in range(days): # days = 3, so iterate 3 times
                # initializing dataframe. Setting extremely high min and low max for first comparison
                temp_df = pd.DataFrame()
                temp_min_final = 100000
                temp_max_final = -100000

                for i in range(blocksinday): # blocksinday = 8, so iterate here 8 times
                    
                    # Loops through each block and compares the min and max. Only stores
                    # if new min is lower than whatever min is currently stored and if 
                    # new max is higher than whatever max is currently stored
                    if ((data['list'][startblock]['main']['temp_min']) - temp_convertor) < temp_min_final:
                        temp_min_final = ((data['list'][startblock]['main']['temp_min']) - temp_convertor)
                    
                    if ((data['list'][startblock]['main']['temp_max']) - temp_convertor) > temp_max_final:
                        temp_max_final = ((data['list'][startblock]['main']['temp_max']) - temp_convertor)
                    
                    # Increase the block we iterate through
                    startblock = startblock + 1
                    
                    # Final storage to min and max lists
                    if x == 0 and i == (blocksinday - 1):
                        min_2 = temp_min_final
                        max_2 = temp_max_final
                    if x == 1 and i == (blocksinday - 1):
                        min_3 = temp_min_final
                        max_3 = temp_max_final
                    if x == 2 and i == (blocksinday - 1):
                        min_4 = temp_min_final
                        max_4 = temp_max_final

# Day 5
            if startblock != 40: # Just to make sure that blocks are still available
                for x in range(lastday): # last day = 1, so iterate 1 time
                    # initializing dataframe. Setting extremely high min and low max for first comparison
                    temp_min_final = 100000
                    temp_max_final = -100000
        
                    for i in range(lastdayblocks): # lastdayblocks is calculated above, and will be different for each timezone
                        
                        # Loops through each block and compares the min and max. Only stores
                        # if new min is lower than whatever min is currently stored and if 
                        # new max is higher than whatever max is currently stored
                        if ((data['list'][startblock]['main']['temp_min']) - temp_convertor) < temp_min_final:
                            temp_min_final = ((data['list'][startblock]['main']['temp_min']) - temp_convertor)
                        if ((data['list'][startblock]['main']['temp_max']) - temp_convertor) > temp_max_final:
                            temp_max_final = ((data['list'][startblock]['main']['temp_max']) - temp_convertor)
        
                        # Increase the block we iterate through
                        startblock = startblock + 1
                        
                        # Final storage for Day 5 if all blocks have been used
                        if x == (lastday - 1) and i == (lastdayblocks - 1):
                            min_5 = temp_min_final
                            max_5 = temp_max_final
                            
                            # calculating the average of all the days
                            max_avg = (((max_1 + max_2 + max_3 + max_4 + max_5)/(firstday + days + lastday)))
                            min_avg = (((min_1 + min_2 + min_3 + min_4 + min_5)/(firstday + days + lastday)))
                            
                            # saving all lists to dataframe
                            temp_data = {"City":[str(loc[a][0])+", "+str(loc[a][1])], "Min 1":[min_1], "Max 1":[max_1], "Min 2":[min_2], "Max 2":[max_2], "Min 3":[min_3], "Max 3":[max_3], "Min 4":[min_4], "Max 4":[max_4], "Min 5":[min_5], "Max 5":[max_5], "Min Avg":[min_avg], "Max Avg":[max_avg]}
                            temp_df = pd.DataFrame(temp_data)
                            weather_df = weather_df.append(temp_df, ignore_index = True)
                            weather_df = round(weather_df, 2)
            
            # If no blocks remain for Day 5, then they should be 0
            else:
                min_5 = 0
                max_5 = 0
                max_avg = (((max_1 + max_2 + max_3 + max_4 + max_5)/5))
                min_avg = (((min_1 + min_2 + min_3 + min_4 + min_5)/5))
                temp_data = {"City":[str(loc[a][0])+", "+str(loc[a][1])], "Min 1":[min_1], "Max 1":[max_1], "Min 2":[min_2], "Max 2":[max_2], "Min 3":[min_3], "Max 3":[max_3], "Min 4":[min_4], "Max 4":[max_4], "Min 5":[min_5], "Max 5":[max_5], "Min Avg":[min_avg], "Max Avg":[max_avg]}
                temp_df = pd.DataFrame(temp_data)
                weather_df = weather_df.append(temp_df, ignore_index = True)
                weather_df = round(weather_df, 2)  
                
        
        
##########################################################################
#                                                                        #                                        
#                        IF ALREADY TOMORROW                             #
#                                                                        #
##########################################################################
    
# DAY 1
        if tomorrowstartblock != 0:
            for x in range(firstday): # firstday = 1, so iterate 1 time.
                # initializing dataframe. Setting extremely high min and low max for first comparison
                temp_df = pd.DataFrame()
                temp_min_final = 100000
                temp_max_final = -100000
                
                for i in range(tomorrowfirstdayblocks): # tomorrowfirstdayblocks = 8, so iterate 8 times
                    
                    # Loops through each block and compares the min and max. Only stores
                    # if new min is lower than whatever min is currently stored and if 
                    # new max is higher than whatever max is currently stored
                    if ((data['list'][i]['main']['temp_min']) - temp_convertor) < temp_min_final:
                        temp_min_final = ((data['list'][i]['main']['temp_min']) - temp_convertor)
                    
                    if ((data['list'][i]['main']['temp_max']) - temp_convertor) > temp_max_final:
                        temp_max_final = ((data['list'][i]['main']['temp_max']) - temp_convertor)  
                    
                    # Increase the block we iterate through
                    startblock = startblock + 1
    
                    # Final storage for min_1 and max_1
                    if x == 0 and i == (tomorrowfirstdayblocks - 1):
                        min_1 = temp_min_final
                        max_1 = temp_max_final

# DAY 2-4
            for x in range(days): # days = 3, so iterate 3 times
                # initializing dataframe. Setting extremely high min and low max for first comparison
                temp_df = pd.DataFrame()
                temp_min_final = 100000
                temp_max_final = -100000
    
                for i in range(blocksinday): # blocksinday = 8, so iterate 8 times
    
                    # Loops through each block and compares the min and max. Only stores
                    # if new min is lower than whatever min is currently stored and if 
                    # new max is higher than whatever max is currently stored
                    if ((data['list'][startblock]['main']['temp_min']) - temp_convertor) < temp_min_final:
                        temp_min_final = ((data['list'][startblock]['main']['temp_min']) - temp_convertor)
                    
                    if ((data['list'][startblock]['main']['temp_max']) - temp_convertor) > temp_max_final:
                        temp_max_final = ((data['list'][startblock]['main']['temp_max']) - temp_convertor)
                    
                    # Increase the block we iterate through
                    startblock = startblock + 1
                    
                    # Final storage to min and max lists
                    if x == 0 and i == (blocksinday - 1):
                        min_2 = temp_min_final
                        max_2 = temp_max_final
                    if x == 1 and i == (blocksinday - 1):
                        min_3 = temp_min_final
                        max_3 = temp_max_final
                    if x == 2 and i == (blocksinday - 1):
                        min_4 = temp_min_final
                        max_4 = temp_max_final


# Looping through for whatever is left of the 40 blocks on Day 5
# Day 5
            if startblock != 40: # Just to make sure that blocks are still available
                # initializing dataframe. Setting extremely high min and low max for first comparison
                for x in range(lastday):
                    temp_min_final = 100000
                    temp_max_final = -100000
        
                    for i in range(blocksinday): # blocksinday = 8, so iterate 8 times
        
                        # Loops through each block and compares the min and max. Only stores
                        # if new min is lower than whatever min is currently stored and if 
                        # new max is higher than whatever max is currently stored
                        if ((data['list'][startblock]['main']['temp_min']) - temp_convertor) < temp_min_final:
                            temp_min_final = ((data['list'][startblock]['main']['temp_min']) - temp_convertor)
                        if ((data['list'][startblock]['main']['temp_max']) - temp_convertor) > temp_max_final:
                            temp_max_final = ((data['list'][startblock]['main']['temp_max']) - temp_convertor)
        
                        # Increase the block we iterate through
                        startblock = startblock + 1
                        
                        # Final storage for Day 5 if all blocks have been used
                        if x == (lastday - 1) and i == (lastdayblocks - 1):
                            min_5 = temp_min_final
                            max_5 = temp_max_final
                            
                            # calculating the average of all the days
                            max_avg = (((max_1 + max_2 + max_3 + max_4 + max_5)/(firstday + days + lastday)))
                            min_avg = (((min_1 + min_2 + min_3 + min_4 + min_5)/(firstday + days + lastday)))
                            
                            # saving all lists to dataframe
                            temp_data = {"City":[str(loc[a][0])+", "+str(loc[a][1])], "Min 1":[min_1], "Max 1":[max_1], "Min 2":[min_2], "Max 2":[max_2], "Min 3":[min_3], "Max 3":[max_3], "Min 4":[min_4], "Max 4":[max_4], "Min 5":[min_5], "Max 5":[max_5], "Min Avg":[min_avg], "Max Avg":[max_avg]}
                            temp_df = pd.DataFrame(temp_data)
                            weather_df = weather_df.append(temp_df, ignore_index = True)
                            weather_df = round(weather_df, 2)
                            
            # If no blocks remain for Day 5, then they should be 0
            else:
                min_5 = 0
                max_5 = 0
                max_avg = (((max_1 + max_2 + max_3 + max_4 + max_5)/5))
                min_avg = (((min_1 + min_2 + min_3 + min_4 + min_5)/5))
                temp_data = {"City":[str(loc[a][0])+", "+str(loc[a][1])], "Min 1":[min_1], "Max 1":[max_1], "Min 2":[min_2], "Max 2":[max_2], "Min 3":[min_3], "Max 3":[max_3], "Min 4":[min_4], "Max 4":[max_4], "Min 5":[min_5], "Max 5":[max_5], "Min Avg":[min_avg], "Max Avg":[max_avg]}
                temp_df = pd.DataFrame(temp_data)
                weather_df = weather_df.append(temp_df, ignore_index = True)
                weather_df = round(weather_df, 2)                        
 

        # Increasing the iterator to get the next location          
        a = a + 1

    else: # Failure
        print( 'Error:', response.status_code )

# creating a csv file
weather_csv = weather_df.to_csv(index=False, float_format='%.2f')

