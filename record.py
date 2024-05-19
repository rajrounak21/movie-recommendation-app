import pandas as pd
from joblib import dump, load
import numpy as np
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c496e4f6892c1c41cbb4877b52db7c73&language=en-US".format(movie_id)
    data = requests.get(url).json()

    st.text(str(data))
    #st.text("https://api.themoviedb.org/3/movie/{}?api_key=c496e4f6892c1c41cbb4877b52db7c73&language=en-US".format(movie_id))

    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title']==movie].index
    if len(movie_index) == 0:
        return [], []

    movie_index = movie_index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies_name = []
    recommended_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_name.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies_name, recommended_movies_poster

movies = load('movies.joblib')
similarity = load('similarity.joblib')
movies = pd.DataFrame(movies)

st.title('Movie Recommendation System')
selected_movie_name = st.selectbox('Type to select your movie', movies['title'].values)

if st.button('Recommend'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movies_name[0])
        st.image(recommended_movies_poster[0])

    with col2:
        st.text(recommended_movies_name[1])
        st.image(recommended_movies_poster[1])

    with col3:
        st.text(recommended_movies_name[2])
        st.image(recommended_movies_poster[2])

    with col4:
        st.text(recommended_movies_name[3])
        st.image(recommended_movies_poster[3])

    with col5:
        st.text(recommended_movies_name[4])
        st.image(recommended_movies_poster[4])