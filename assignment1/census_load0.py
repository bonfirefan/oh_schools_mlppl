import censusdata
import pandas as pd
import numpy as np

#function to make list of all county ids in state (given by census state id)


def county_list(state_number):
    counties = censusdata.geographies(censusdata.censusgeo([('state', state_number), ('county','*')]), 'acs5', 2018)
    county_list = []
    for i in counties.keys():
        county_list.append(counties[i].geo[1][1])
    return county_list

#function to pull defined variables for blocks in specified state, looping over counties (can't pull all blocks in a state)
#(input state id and list of variables)
def block_pull(state_id, variable_list):
    c_list = county_list(state_id)
    for i in range(0, len(c_list)):
        geo = censusdata.censusgeo([('state', state_id), ('county', c_list[i]), ('tract','*'),('block group','*')])
        county_df = censusdata.download('acs5', 2018, geo, variable_list)
        if i == 0:
            data = county_df
        else:
            data = pd.concat([data, county_df], sort=True)
    return data

def data_prep(dtb, var_dict):
    # Get row information
    bg_index = dtb.index
    state_id = [bg.geo[0][1] for bg in bg_index]
    county_id = [bg.geo[1][1] for bg in bg_index]
    tract_id = [bg.geo[2][1] for bg in bg_index]
    bgroup_id= [bg.geo[3][1] for bg in bg_index]
    countyname = [bg.name.split(',')[2] for bg in bg_index]
    statename = [bg.name.split(',')[3] for bg in bg_index]
    schdistr_id = [bg.sumleveldict.get('state> school district (unified)') for bg in bg_index]
    dtb['state_id'] = state_id
    dtb['county_id'] = county_id
    dtb['tract_id'] = tract_id
    dtb['bgroup_id'] = bgroup_id
    dtb['countyname'] = countyname
    dtb['statename'] = statename
    dtb['schdistr_id'] = schdistr_id
    cnames = dtb.columns.tolist()
    dtb['pk'] = dtb.state_id + '_'+ dtb.county_id + '_' +  dtb.tract_id + '_'+ dtb.bgroup_id + '_' + dtb.schdistr_id
    dtb = dtb[['pk']+cnames]
    # Rename columns for humans
    dtb = dtb.rename(columns=var_dict)

    return(dtb)

# Printing Data
def main():
    # Selected Variables
    var_dict = {  'B02001_001E' : 'Pop_All',
         'B02001_002E' : 'Pop_White',
         'B02001_003E' : 'Pop_Black_or_AA',
         'B02001_005E' : 'Pop_Asian',
         'B03002_012E' : 'Pop_Hispanic_Latino',
         'B28006_001E' : 'Edu_All',
         'B28006_002E' : 'Edu_Less_Than_High_School',
         'B28006_008E' : 'Edu_High_School_Grad',
         'B28006_014E' : 'Edu_Bach_Or_Higher',
         'B19013_001E' : 'Median_Income',
         'B17010_001E' : 'Pov_All',
         'B17010_001E' : 'Pov_Total',
         'B17010_002E' : 'Pov_Poverty'
         }

    var_list = list(var_dict.keys())

    print('Reading data...')
    block_data = block_pull('39', var_list)

    print('Cleaning data...')
    block_data = data_prep(block_data, var_dict)

    # SAVE DATA, INDEX IS JUST FOR TESTING
    block_data.to_csv('data.csv', index=False)

if __name__ == '__main__':
  main()
