import censusdata

MY_API_KEY = '1936736258d353a204c8a1f6189f327836630bbc'

# Find states
censusdata.geographies(censusdata.censusgeo([('state', '*')]), 'acs5', 2015)

# Find sample colum
ohbg = censusdata.download('acs5', 2015,
                    censusdata.censusgeo([('state', '30'), ('county', '*'), ('block group', '*')]),
                        ['B23025_003E'])
print(ohbg)
ohbg.to_csv('ohbg_test.csv')
