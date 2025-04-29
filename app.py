import pandas as pd
import requests
import streamlit as st
from joblib import load

# ------------------ Utility Function to Fetch Poster ------------------ #
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c496e4f6892c1c41cbb4877b52db7c73&language=en-US"
    response = requests.get(url)
    data = response.json()

    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# ------------------ Recommendation Function ------------------ #
def recommend(movie_title):
    try:
        index = movies[movies['title'] == movie_title].index[0]
    except IndexError:
        st.error("Selected movie not found in database.")
        return [], []

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movies = []
    recommended_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movies.append(movies.iloc[i[0]]['title'])
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# ------------------ Streamlit App UI ------------------ #
st.header('🎬 Movie Recommendation System')

# Load data
movies = pd.DataFrame(load('movie.joblib'))
similarity = load('similarity.joblib')

# Dropdown for movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox('Type to select a movie from dropdown:', movie_list)

# Show recommendations
if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)
    if names and posters:
        columns = st.columns(5)
        for i in range(5):
            with columns[i]:
                st.text(names[i])
                st.image(posters[i])
