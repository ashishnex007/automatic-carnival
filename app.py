import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')

def fetch_poster(movie_id):
    res = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id, api_key))
    data = res.json()
    return 'https://image.tmdb.org/t/p/w500' + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_idx = movies.iloc[i[0]].id
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_idx))
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies, recommended_movies_posters

movie_dict = pickle.load(open('movie-dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie = st.selectbox("Select the Movie", movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0], caption=names[0])
    with col2:
        st.image(posters[1], caption=names[1])
    with col3:
        st.image(posters[2], caption=names[2])
    with col4:
        st.image(posters[3], caption=names[3])
    with col5:
        st.image(posters[4], caption=names[4])