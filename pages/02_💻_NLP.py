import streamlit as st


st.markdown("""

### Procedure to Extract Sentiment from User comments

***
""")

st.markdown("""

* Scraped user comments from the **Nextdoor** website, for each zip code in the **Salt Lake County**

* Used two pre-trained models to extract polarity scores. (**Text Blob, NLTK**)

* The polarities are calcualted for each comment and *averaged over each zipcode*

* The polarity values are the *average of both polarities*

""")

st.write("##")
st.write("##")
st.write("##")

st.markdown("""

### About Me

* Amir Behbahanian, PhD.

* amir.behbahanian@mg.thedataincubator.com

* Main Skills:
    * Data Wrangling
    * Machine Learning (Regressioin, Classification, Clustering):

        * Natural Language Processing (**NLP**)
        * Supervised and Unsupervised Models (Tree-Based Models, K-means, K-nearest Neighbors, etc.)
        * Feature Importance
        * Dimensionality Reduction
        * Distributed Computing (Pyspark, AWS)

    * Neural Networks (ANN, CNN)

""")