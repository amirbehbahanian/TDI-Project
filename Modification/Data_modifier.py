import json
import numpy as np
import pandas as pd

def modifer():
    data = pd.read_excel(r'C:\Users\amirb\Documents\The_Data_Incubator\Project\WebApp\Data\zip_code_data.xlsx')

    data_modified = []
    for i in range(len(data)): 
        if data.iloc[i,0]==84138 or data.iloc[i,0]==84150: 
            pass
        else:
            data_modified.append(data.iloc[i,:])
    data_modified = pd.DataFrame(data_modified)
    data_modified['zip_code'] = data_modified['zip_code'].astype(int).astype('str')
    data_modified['Children(0-14)'] = data_modified[['age_0-4','age_5-9', 'age_10-14']].sum(axis=1)/(data_modified['Population'])
    data_modified['Youth (15-24)'] = data_modified[['age_15-17', 'age_18-20', 'age_21-24']].sum(axis=1)/(data_modified['Population'])
    data_modified['Adults (25-64)'] = data_modified[['age_25-34', 'age_35-44','age_45-54', 'age_55-64']].sum(axis=1)/(data_modified['Population'])
    data_modified['Seniors (65+)'] = data_modified[['age_65-74', 'age_75-84', 'age_85+']].sum(axis=1)/(3*data_modified['Population'])
    data_modified = data_modified.drop(columns=['age_0-4', 'age_5-9', 'age_10-14', 'age_15-17', 'age_18-20', 'age_21-24', 'age_25-34', 'age_35-44', 'age_45-54', 'age_55-64', 'age_65-74', 'age_75-84', 'age_85+'])


    data_modified['Families_below_pov'] = data_modified['Families_below_pov']/data_modified['#Families']
    data_modified['Families_below_pov_with_child'] = data_modified['Families_below_pov_with_child']/data_modified['#Families']

    data_modified['House_Hold_with_child'] = data_modified['House_Hold_with_child']/data_modified['#Household']


    data_modified[['race_white', 'race_black','race_indian', 'race_Asian', 'race_Hawaian']] = data[['race_white', 'race_black','race_indian', 'race_Asian', 'race_Hawaian']].div(data['Population'],axis=0)
    data_modified['race_two+'] = data_modified[['race_other', 'race_two']].sum(axis=1)/(data_modified['Population'])
    data_modified = data_modified.drop(columns=['race_other', 'race_two'])

    data_modified['HHincome_two+'] = data_modified[['HHincome_other', 'HHincome_two']].sum(axis=1)/2
    data_modified = data_modified.drop(columns=['HHincome_other', 'HHincome_two'])

    Sum_edu = data_modified[['edu_<9th', 'edu_nodiploma', 'edu_highschool', 'edu_somecollege','edu_Associate', 'edu_Bachelor', 'edu_Maters', 'edu_professional','edu_Doctorate']].sum(axis=1)
    data_modified['edu_uptoCollege level'] = data_modified[['edu_<9th', 'edu_nodiploma', 'edu_highschool', 'edu_somecollege']].sum(axis=1).div(Sum_edu,axis=0)
    data_modified = data_modified.drop(columns=['edu_<9th', 'edu_nodiploma', 'edu_highschool', 'edu_somecollege'])
    data_modified[['edu_Associate', 'edu_Bachelor', 'edu_Maters', 'edu_professional', 'edu_Doctorate']] =data_modified[['edu_Associate', 'edu_Bachelor', 'edu_Maters', 'edu_professional', 'edu_Doctorate']].div(Sum_edu,axis=0)

    return data_modified

if __name__=="__main__":
    data_modified = modifer()
    data_modified.to_csv(r"C:\Users\amirb\Documents\The_Data_Incubator\Project\WebApp\Data\Data_modified.csv", index=False)