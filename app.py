from optparse import Option
import streamlit as st
import pickle
import pandas as pd 
#to hit the API u need this library
import requests


def get_poster(movie_id):
    response_api = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    #converting that response to json 
    response_data = response_api.json()
    return "https://image.tmdb.org/t/p/w500/" + response_data['poster_path']


def recommend(movie):
    movie_idx = movies_df[movies_df['title'] == movie].index[0]
    distances = vectors_similarity[movie_idx]
    movies_lst = sorted(list((enumerate(distances))),reverse=True, key = lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_lst:
        movie_ids = movies_df.iloc[i[0]].movie_id
        #fetching poster from API
        recommended_movies.append(movies_df.iloc[i[0]].title)
        recommended_movies_posters.append(get_poster(movie_ids))
    return recommended_movies,recommended_movies_posters

st.title('Movie Recommender')

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies_df = pd.DataFrame(movies_dict)

vectors_similarity = pickle.load(open('vectors_similarity.pkl','rb'))
 
# st.markdown(
#     """
# <style>
# .reportview-container .markdown-text-container {
#     font-family: monospace;
# }
# .sidebar .sidebar-content {
#     background-image: linear-gradient(#2e7bcf,#2e7bcf);
#     color: white;
# }
# .Widget>label {
#     color: white;
#     font-family: monospace;
# }
# [class^="st-b"]  {
#     color: white;
#     font-family: monospace;
# }
# .st-bb {
#     background-color: transparent;
# }
# .st-at {
#     background-color: #0c0080;
# }
# footer {
#     font-family: monospace;
# }
# .reportview-container .main footer, .reportview-container .main footer a {
#     color: #0c0080;
# }
# header .decoration {
#     background-image: none;
# }

# </style>
# """,
#     unsafe_allow_html=True,
# )
selected_movie = st.selectbox('Enter movie name' , movies_df['title'].values)

#This lets me display movie which is selected  
if st.button('Recommend'):
    name,posters =  recommend(selected_movie)
    
    #to display 5 of the posters
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(posters[0])

    with col2:
        st.text(name[1])
        st.image(posters[1])
        
    with col3:
        st.text(name[2])
        st.image(posters[2])

    with col4:
        st.text(name[3])
        st.image(posters[3])

    with col5:
        st.text(name[4])
        st.image(posters[4])

