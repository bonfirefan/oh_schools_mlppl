import pandas as pd
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import re

def schMatcher(placelist, schList):
    '''
    Takes in a district column and returns a matcher to ODE district
    '''
    # List for dicts for easy dataframe creation
    dict_list = []

    unusual_match = {'': ''}
    for place in placelist:
        # New dict for storing data
        if place:
            dict_ = {}
            aMatch = process.extractOne(place, schList,  scorer=fuzz.ratio)

            dict_.update({"orig_distr" : place})
            dict_.update({"ode_distr" : aMatch[0]})
            dict_.update({"labelScore" : aMatch[1]})
            dict_list.append(dict_)

    matches_all = pd.DataFrame(dict_list)
    return(matches_all)

def find_sch_match(dFrame, col, schoolDF, schcol):
    '''
    Takes a cleaned dataframe and appends school typology
    By fuzzy matching on the name
    '''
    loc_list = set(dFrame[col])
    schMatch = schMatcher(loc_list, schoolDF[schcol])
    dataLoc = pd.merge(dFrame, schMatch,  how='left', left_on=[col], right_on = ['orig_distr'])
    dataLoc = pd.merge(dataLoc, schoolDF,  how='left', left_on=['ode_distr'], right_on = [schcol])
    dataLoc = dataLoc.drop(['district_x', 'district_y', 'orig_distr', 'labelScore', 'fyear'], axis=1)
    return(dataLoc)

def data_preparation(data, ode, args=None):
    # Variables in 8th grade
    data.loc[data['grade']==8,'gpa_8'] = data['new_gpa']
    data.loc[data['grade']==8,'abs_8'] = data['days_absent']
    data.loc[data['grade']==8,'int_8'] = data['intervention_count']


    # Cohort and aux grade_min and grade_max
    data.loc[data['grade']==9,'cohort'] = data['school_year']
    data['grade_max'] = data['grade']
    data['grade_min'] = data['grade']

    data['graduation_date'] = pd.to_datetime(data['graduation_date'])

    # Groupby each student
    data = data.groupby('student_lookup').agg({'ethnicity':'first', 'graduation_date':'max', 'district':'first',
                                                'withdraw_reason':'last', 'gpa_8':'mean', 'abs_8':'sum', 'int_8':'sum',
                                                'discipline_incidents':'mean',
                                                       'grade_min':'min', 'grade_max':'max', 'cohort':'first'})
    data = data.reset_index()

    ethnic_dummies = pd.get_dummies(data['ethnicity'])
    data = data.drop('ethnicity',axis = 1)
    data = data.join(ethnic_dummies)

    data = find_sch_match(data, 'district', ode, 'district_name')

    # Filter data to relevant students
    data = data[data['cohort'].notnull()]
    data = data[data['cohort']<=2012]

    # Graduate variable
    data['graduated_time'] = data['graduation_date'].dt.year-data['cohort']
    data['graduated'] = data['graduated_time']<=4
    data.loc[data['withdraw_reason']=='transferred - in state', 'graduated'] = None
    data.loc[data['withdraw_reason']=='transferred - out of state', 'graduated'] = None
    data.loc[data['withdraw_reason']=='transferred - transferred - out of country', 'graduated'] = None
    data.loc[data['withdraw_reason']=='transferred - private', 'graduated'] = None
    data.loc[data['withdraw_reason']=='transferred - homeschool', 'graduated'] = None
    data.loc[data['withdraw_reason']=='withdrew - death', 'graduated'] = None
    data = data[data['graduated'].notnull()]

    # Drop aux variables
    data = data.drop(columns=['student_lookup','graduation_date','withdraw_reason','grade_min','grade_max', 'graduated_time'])
    data = data.dropna()
    print(data.dtypes)
    data = data.select_dtypes(exclude=['object'])

    return data

def train_val_test_split(data, min_train_cohort, min_test_cohort):
    train_data = data[(data['cohort']>=min_train_cohort)&(data['cohort']< min_test_cohort)]
    test_data = data[data['cohort']>=min_test_cohort]

    train_data = train_data.drop(columns=['cohort'])
    test_data = test_data.drop(columns=['cohort'])

    return train_data, test_data
