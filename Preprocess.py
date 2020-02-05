import pandas as pd
import numpy as np
from collections import Counter
import nltk
import re
import csv

stopwords = nltk.corpus.stopwords.words('english')
RE_stopwords = r'\b(?:{})\b'.format('|'.join(stopwords))


fname = 'output_15miles07-16--08-16.csv'
f2name = 'output_15miles01-01--07-15.csv'
JulToOctdf = pd.read_csv(fname,
                 names=['username', 'date', 'retweets', 'favorites', 'text', 'geo', 'mentions', 'hashtags', 'id', 'permalink'], sep=';', skiprows = 1)
JanToJuldf = pd.read_csv(f2name,
                 names=['username', 'date', 'retweets', 'favorites', 'text', 'geo', 'mentions', 'hashtags', 'id', 'permalink'], sep=';', skiprows = 1, low_memory=False)

#drop all columns except 'username' and 'text' column
JulToOctdf2 = JulToOctdf[['username', 'text']].copy()
JanToJuldf2 = JanToJuldf[['username', 'text']].copy()
JulToOctdf2['label'] = JulToOctdf['text'].str.lower().str.contains('#hurricaneharvey|#harvey|flooding.|flooding|hurricane|#hurricane|#prayforhouston|#houstonstrong|flood|harvey|#houstonflood|flooded|water|#harvey2017|safe|#hurricaneharvey2017|#flood|need|center|#flooding|#prayfortexas|#texasstrong|victims|storm|affected|prayers|#harveyrelief|#help|rescue|#hurricanharvey|pray|helping|praying|donations|#rain|relief|help' , na=False)

JanToJuldf2['label'] = JanToJuldf['text'].str.lower().str.contains('#hurricaneharvey|#harvey|flooding.|flooding|hurricane|#hurricane|#prayforhouston|#houstonstrong|flood|harvey|#houstonflood|flooded|water|#harvey2017|safe|#hurricaneharvey2017|#flood|need|center|#flooding|#prayfortexas|#texasstrong|victims|storm|affected|prayers|#harveyrelief|#help|rescue|#hurricanharvey|pray|helping|praying|donations|#rain|relief|help' , na=False)

#df2 has only 3 columns with all usernames, tweets and labels(1 or 0)
#replace (true or false) in 'label' to (1's and 0's)
JulToOctdf2['label'] = JulToOctdf2['label'].astype(int)
JanToJuldf2['label'] = JanToJuldf2['label'].astype(int)
#df3 has unique names and sum of label
JulToOctdf3 = JulToOctdf2.groupby(['username'], as_index=False, sort=True)['label'].sum()

#df4 has unique names with keywords present
JulToOctdf4 = JulToOctdf3[JulToOctdf3['label'] > 0]


JulToOctdf5 = pd.merge(JulToOctdf2, JulToOctdf4, on=['username'], how='left')
JulToOctdf5['label_y'].fillna(0, inplace=True)
JulToOctdf5['label_y'] = JulToOctdf5['label_y'].where(~(JulToOctdf5['label_y']>0),other=1)

JanToJuldf5 = pd.merge(JanToJuldf2, JanToJuldf4, on=['username'], how='left')
JanToJuldf5['label_y'].fillna(0, inplace=True)
JanToJuldf5['label_y'] = JanToJuldf5['label_y'].where(~(JanToJuldf5['label_y']>0),other=1)

JulToOctdf6 = JulToOctdf5.sort_values(by='username')
JanToJuldf6 = JanToJuldf5.sort_values(by='username')

#combine two dataframe (Dataset1 and Dataset2)
combineddf = pd.concat([JulToOctdf6, JanToAugdf6], ignore_index=True)
combineddf = combineddf.sort_values(by='username')
combineddf = combineddf.iloc[np.random.permutation(len(df6))]
#combineddf1 = JunToAugdf6.groupby(['username'], as_index=False, sort=True)['label_y'].sum()

#remove links, URLs
combineddf['text'] = combineddf['text'].str.replace('http\S+|www.\S+|\S+.com\S+', '', case=False)

#remove stopwords
combineddf['text'] = combineddf['text'].str.replace(RE_stopwords, '')
#randomcombineddf = randomcombineddf.dropna()
combineddf['text'] = combineddf['text'].astype(str)

#remove punctuations
combineddf['text'] = combineddf['text'].str.replace('[^\w\s]','')
print combineddf['text'].head(5)

#remove emojis
emoji_pattern = re.compile(
                           u"(\ud83d[\ude00-\ude4f])|"  # emoticons
                           u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
                           u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
                           u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
                           u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
                           "+", flags=re.UNICODE)
for row in combineddf['text']:
    emoji_pattern.sub(r'', row)


combineddf.to_csv('combineddf', sep='\t')
