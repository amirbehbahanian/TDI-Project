import streamlit as st
from PIL import Image


st.markdown("<h1 style='text-align: center; color: grey;'>  Nerd <span style='text-align: center; color: green;'> Realtor </span> </h1>", unsafe_allow_html=True)
image = Image.open(r'C:\Users\amirb\Documents\The_Data_Incubator\Project\WebApp\Data\Utah-mountains.jpg')
st.image(image, use_column_width=True)

st.write("##")
st.write("##")
st.write("##")

st.markdown("""

* ##### The Utah housing Market is the **number one** housing market in terms of housing price increase Source: [Bankrate](https://www.bankrate.com/mortgages/housing-heat-index/)
* ##### Utah is ranked 9th in the Net Migration by State ranking

***
""")

# image = Image.open(r'C:\Users\amirb\Documents\The_Data_Incubator\Project\WebApp\Data\Utah Housing.png')
# st.image(image, width=500)


image = Image.open(r'C:\Users\amirb\Documents\The_Data_Incubator\Project\WebApp\Data\NerdRealtor-1.png')
st.sidebar.image(image, use_column_width=True)

st.sidebar.caption('Made by ***Amir Behbahanian***')


