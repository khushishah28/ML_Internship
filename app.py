import streamlit as st
import pickle
import requests

# Function to fetch movie poster from The Movie Database (TMDb)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
                return full_path
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error fetching poster for movie ID {movie_id}: {str(e)}")
        return None

# Load movie data and similarity matrix
movies = pickle.load(open('movies_list.pkl', 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['original_title'].values

st.header("Movie Recommender System")

# Selectbox to choose a movie
selected_movie = st.selectbox("Select a movie:", movies_list)

# Function to recommend movies based on similarity
def recommend(selected_movie):
    index = movies[movies['original_title'] == selected_movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommend_movie = []
    recommend_poster = []
    
    for i in distance[1:6]:  # Start from 1 to exclude the selected movie itself
        movie_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].original_title)
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommend_poster.append(poster_url)
        else:
            recommend_poster.append("https://via.placeholder.com/150")  # Placeholder if poster not found
    
    return recommend_movie, recommend_poster

# Show recommendations when button is clicked
if st.button("Show Recommendations"):
    movie_name, movie_poster = recommend(selected_movie)

    # Display recommended movies and posters in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
