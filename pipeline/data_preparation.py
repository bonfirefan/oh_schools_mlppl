import pandas as pd

def data_preparation(data, args=None):

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
    data = data.groupby('student_lookup').agg({'ethnicity':'first', 'graduation_date':'max', 'school_name':'first',
                                                'withdraw_reason':'last', 'gpa_8':'mean', 'abs_8':'mean', 'int_8':'mean',
                                                       'grade_min':'min', 'grade_max':'max', 'cohort':'first'})
    data = data.reset_index()

    ethnic_dummies = pd.get_dummies(data['ethnicity'])
    data = data.drop('ethnicity',axis = 1)
    data = data.join(ethnic_dummies)

    school_dummies = pd.get_dummies(data['school_name'])
    data = data.drop('school_name',axis = 1)
    data = data.join(school_dummies)

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

    return data

def train_val_test_split(data, max_train_cohort, min_test_cohort):
    train_data = data[data['cohort']<=max_train_cohort]
    test_data = data[data['cohort']>=min_test_cohort]

    train_data = train_data.drop(columns=['cohort'])
    test_data = test_data.drop(columns=['cohort'])

    return train_data, test_data 
    