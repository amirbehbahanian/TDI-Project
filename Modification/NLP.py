from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

def NLP():
    zip_codes = [84006, 84020, 84044, 84047, 84065, 84070, 84081,
                84084, 84088, 84092, 84093, 84094, 84095, 84096, 
                84101, 84102, 84103, 84104, 84105, 84106, 84107, 
                84108, 84109, 84111, 84112, 84113, 84115, 84116, 
                84117, 84118, 84119, 84120, 84121, 84123, 84124,
                84128]


    def parser(zipcode):
        if zipcode==84112 or zipcode==84113:
            zipcode = '84112-84113'
        with open(r"C:\Users\amirb\Documents\The_Data_Incubator\Project\WebApp\Data\{}.txt".format(zipcode), encoding="utf-8") as f:
            soup = BeautifulSoup(f.read())
        module = soup.find_all('span', attrs={'class':'Linkify'})
        comments = []
        for m in module:
            comments.append(m.text)

        globals()['com_{}'.format(zipcode)] = []
        for comment in comments:
            if 'just joined' not in comment:
                globals()['com_{}'.format(zipcode)].append(comment)
        return globals()['com_{}'.format(zipcode)]    
    Result = []
    for z in zip_codes:
        Result.append(parser(z))

    nltk.download('vader_lexicon')
    sid = SentimentIntensityAnalyzer()
    sentiment_nltk = []
    for z, i  in zip(zip_codes, range(len(zip_codes))):
        temp = []
        for r in Result[i]:
            temp.append( sid.polarity_scores( r )['compound'] )
        sentiment_nltk.append( [z, round(np.mean(temp), 3)] )

    sentiment_text = []
    for z, i  in zip(zip_codes, range(len(zip_codes))):
        temp = []
        for r in Result[i]:
            temp.append( TextBlob(r).sentiment.polarity )
        sentiment_text.append( [z, round(np.mean(temp), 3) ] )

    Final = pd.DataFrame( list(zip(zip_codes, [j for i,j in sentiment_text], [j for i,j in sentiment_nltk])), columns=['Zip', 'Text_blob', 'NLTK'])
    scaler = MinMaxScaler()
    Final['NLTK'] = scaler.fit_transform(Final['NLTK'].values.reshape(-1,1))
    Final['Text_blob'] = scaler.fit_transform(Final['Text_blob'].values.reshape(-1,1))
    Final = Final.sort_values(by=['Text_blob'])
    P = np.polyfit(Final["Text_blob"], Final['NLTK'], 1)
    Final['Sentiment'] = np.polyval(P, Final["Text_blob"])
    Final.drop(['Text_blob', 'NLTK'], axis=1, inplace=True)
    return Final


if __name__=='__main__':
    df = pd.read_csv(r'C:\Users\amirb\Documents\The_Data_Incubator\Project\WebApp\Data\Data_modified.csv')
    pd.merge(df, NLP(), left_on='zip_code', right_on='Zip').to_csv(r"C:\Users\amirb\Documents\The_Data_Incubator\Project\WebApp\Data\Data_modified_withSentiment.csv", index=False)