import censusdata
import pandas as pd

#function to make list of all county ids in state (given by census state id)
def county_list(state_number):
    counties = censusdata.geographies(censusdata.censusgeo([('state', state_number),('county','*')]), 'acs5', 2018)
    county_list = []
    for i in counties.keys():
        county_list.append(counties[i].geo[1][1])
    return county_list

#function to pull defined variables for blocks in specified state, looping over countties
#(input state id and list of variables)
def block_pull(state_id,variable_list):
    c_list = county_list(state_id)
    for i in range(0,len(c_list)):
        geo = censusdata.censusgeo([('state',state_id),('county',c_list[i]),('tract','*'),('block group','*')])
        county_df = censusdata.download('acs5',2018,geo,variable_list)
        if i == 0:
            data = county_df
        else:
            data = pd.concat([data,county_df])
    return data

variables_list = ['B02001_001E']
county = block_pull('39',variables_list)
count.to_csv('test_upload.csv')
