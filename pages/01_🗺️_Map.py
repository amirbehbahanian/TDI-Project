from turtle import color
from matplotlib.pyplot import sca
import streamlit as st
from PIL import Image
import pandas as pd
import folium
from streamlit_folium import st_folium, folium_static
from sklearn.preprocessing import MinMaxScaler
import json
from os import path
import copy

from Modification import Data_modifier
from Modification import NLP


if path.exists(r"C:\Users\amirb\Documents\The_Data_Incubator\Project\WebApp\Data\Data_modified_withSentiment.csv"):
    data_modified = pd.read_csv(r"C:\Users\amirb\Documents\The_Data_Incubator\Project\WebApp\Data\Data_modified_withSentiment.csv")
    data_modified['zip_code'] = [str(z) for z in data_modified['zip_code']]
else:
    if path.exists(r"C:\Users\amirb\Documents\The_Data_Incubator\Project\WebApp\Data\Data_modified.csv"):
        data_modified = pd.read_csv(r'C:\Users\amirb\Documents\The_Data_Incubator\Project\WebApp\Data\Data_modified.csv')
        data_modified = pd.merge(data_modified, NLP(), left_on='zip_code', right_on='Zip')
    else:
        data_modified = Data_modifier.modifer()
        data_modified = pd.merge(data_modified, NLP(), left_on='zip_code', right_on='Zip')

f = folium.Figure(width=200, height=200)
m = folium.Map(location=[40.683094, -111.889555] , tiles='CartoDB positron',zoom_start = 10)
boundary_file = r'C:\Users\amirb\Documents\The_Data_Incubator\Project\WebApp\Data\ut_utah_zip_codes_geo.min.json'
with open(boundary_file, 'r') as f:
    zipcode_boundary = json.load(f)
mod_features = [feature for feature in zipcode_boundary['features'] if feature['properties']['ZCTA5CE10'] in list(data_modified['zip_code'].astype('str'))]
zipcode_boundary['features'] = mod_features


# image = Image.open(r'C:\Users\amirb\Documents\The_Data_Incubator\Project\WebApp\Data\NerdRealtor-1.png')
# st.sidebar.image(image, use_column_width=True)
st.sidebar.header('Select a Feature')

data_modified = data_modified.rename({'Sentiment':'Happiness','Percent_Pop_change': '% Population Change', 'House_Hold_with_child' : '% Number of Household with Child' ,
                                     'Avg_Housing_value': 'Avg. Housing Value', 'HHincome_all': 'Household Income', 'Families_below_pov': '% Families below poverty',
                                     'edu_Associate': 'Education: Associate', 'edu_uptoCollege level':'Education: Up to College', 'edu_Bachelor':'Education: Bachelor',
                                      'edu_Maters':'Education: Masters', 'edu_professional':'Education: Professional', 'edu_Doctorate':'Education: Doctorate', '#Housing':'Number of Houses'},axis=1)

features = ['Avg. Housing Value', 'Happiness', 'Population', '% Population Change', '% Number of Household with Child', 'Number of Houses',
            'Household Income', '% Families below poverty','Education:Up to College', 
            'Education: Associate', 'Education: Bachelor', 'Education: Masters', 'Education: Professional','Education: Doctorate', 
            'Children(0-14)','Youth (15-24)', 'Adults (25-64)','Seniors (65+)']

for f in features:
    if f=='Avg. Housing Value':
        globals()['F_{}'.format(f)] = st.sidebar.checkbox('{}'.format(f), value= True)
    else:
        globals()['F_{}'.format(f)] = st.sidebar.checkbox('{}'.format(f))

st.sidebar.markdown("""---""")
st.sidebar.markdown("<h1 style='text-align: center; color: grey; line-height: 0px'>Customize your index</h1> ", unsafe_allow_html=True)
st.sidebar.markdown("<h2 style='text-align: center; color: green;'>Feature effect on your index</h2> ", unsafe_allow_html=True)

F_selected = []
for f in features:
    if globals()['F_{}'.format(f)]:
        F_selected.append(f)
        #st.sidebar.slider("{}".format(f), min_value = -1.00, max_value = 1.00, value = 1.00)
        globals()['slider_string_{}'.format(f)] = st.sidebar.select_slider('{}'.format(f), 
                                                        options= ['Very Low', 'Low', 'None', 'High', 'Very High'], value='High')
        if globals()['slider_string_{}'.format(f)]== 'Very Low':
            globals()['slider_{}'.format(f)] = -2
        elif globals()['slider_string_{}'.format(f)]== 'Low':
            globals()['slider_{}'.format(f)] = -1
        elif globals()['slider_string_{}'.format(f)]== 'None':
            globals()['slider_{}'.format(f)] = 0.0
        elif globals()['slider_string_{}'.format(f)]== 'High':
            globals()['slider_{}'.format(f)] = 1
        elif globals()['slider_string_{}'.format(f)]== 'Very High':
            globals()['slider_{}'.format(f)] = 2

if len(F_selected)==1:
    # selected_feature = st.sidebar.selectbox("Features", F_selected)

    st.sidebar.caption('Made by ***Amir Behbahanian***')

    target = F_selected[0]
    folium.Choropleth(
        geo_data=zipcode_boundary,
        name='choropleth',
        data=data_modified,
        columns=['zip_code', target],
        key_on='feature.properties.ZCTA5CE10',
        fill_color='Spectral',
        fill_opacity=0.3,
        nan_fill_opacity=0,
        line_opacity=1,
        legend_name= target
    ).add_to(m)
elif len(F_selected)>1:
    scaler = MinMaxScaler()
    data_modified_scaled = copy.deepcopy(data_modified)
    temp = pd.DataFrame( scaler.fit_transform(data_modified_scaled[F_selected]), columns = F_selected) #.sum(axis=1)/len(F_selected)
    for col in temp.columns:
        temp[col] = temp[col].apply(lambda x: x*globals()['slider_{}'.format(col)])
    temp = temp.sum(axis=1)/len(F_selected)
    data_modified_scaled['Personalized Index'] = (temp - min(temp))*100/(temp.max()- temp.min())
    
    target = 'Personalized Index'
    folium.Choropleth(
        geo_data=zipcode_boundary,
        name='choropleth',
        data=data_modified_scaled,
        columns=['zip_code', target],
        key_on='feature.properties.ZCTA5CE10',
        fill_color='Spectral',
        fill_opacity=0.3,
        nan_fill_opacity=0,
        line_opacity=1,
        legend_name= target
    ).add_to(m)



st.markdown("<h1 style='text-align: center; color: grey;'>Create your personalized index</h1> ", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>Choose what\'s important to YOU</h2>", unsafe_allow_html=True)

st.markdown(""" 

* ###### Demographic and Economic information 
* ###### **Happiness Index**, which is based on comments people made on the internet about their neighborhood

* ###### Personalized index, which indicates the average of the indecies selected by the user

""")

folium_static(m)