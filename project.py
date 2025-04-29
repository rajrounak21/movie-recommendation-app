import ast

import pandas as pd
import numpy as np
movies=pd.read_csv("C:\\Users\\rouna\\Desktop\\projects\\tmdb_5000_movies.csv")
credits=pd.read_csv("C:\\Users\\rouna\\Desktop\\projects\\tmdb_5000_credits.csv")
print(movies.keys())
print(credits.keys())

#merge the data on basis of title
movies=movies.merge(credits,on='title')
#print(movies.shape)
print(movies.keys())

#only choose useful data according to importance and create new dataframe
movies=movies[['movie_id','title','genres','overview','keywords','cast','crew']]
print(movies.keys())

print(movies.head())
# remove missing data
nul=movies.isnull().sum()
print(nul)
print(movies.dropna(inplace=True))
dup=movies.duplicated().sum()
print(dup)

# convert the genres data in list
print(movies.iloc[0].genres)
def convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L
movies['genres']=movies['genres'].apply(convert)

# convert keywords data in list
print(movies.iloc[0].keywords)

movies['keywords']=movies['keywords'].apply(convert)
print(movies['keywords'])

# in cast we want starting three name only in list form
def convert3(obj):
    L=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter !=3:
            L.append(i['name'])
            counter+=1
        else:
            break
    return L

movies['cast']=movies['cast'].apply(convert3)
print(movies['cast'])

# In crew we want only director
print(movies.iloc[0].crew)
def fetch_director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director' :
            L.append(i['name'])
            break

    return L

movies['crew']=movies['crew'].apply(fetch_director)
print(movies['crew'])
# edit the overview section
movies['overview']=movies['overview'].apply(lambda x:x.split())
print(movies['overview'])
# remove the space
movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","")for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","")for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","")for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","")for i in x])

#concat the data
movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']
print(movies.keys())
new_df=movies[['movie_id','title','tags']]
new_df['tags']=new_df['tags'].apply(lambda x:" ".join(x))
new_df['tags']=new_df['tags'].apply(lambda x:x.lower())
print(new_df['tags'][0])
# convert  into vectorization
from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_df=5000,stop_words='english')
vector=cv.fit_transform(new_df['tags']).toarray()
# convert tag data into list
import nltk
from nltk.stem.porter import PorterStemmer

from nltk.tokenize import word_tokenize

ps = PorterStemmer()
def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))

    return " ".join(y)
new_df['tags']=new_df['tags'].apply(stem)
print(new_df['tags'][0])

# recommend a movie
from sklearn.metrics.pairwise import cosine_similarity
similarity=cosine_similarity(vector)
def recommend(movie):
    movie_index=new_df[new_df['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    for i in movies_list:

        print(i[0])

recommend('Avatar')

from joblib import dump,load
dump(
    new_df.to_dict(),"movie.joblib"
)

dump(similarity,"similarity.joblib")