import streamlit as st
import pickle

import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import pandas as pd
import webbrowser

# dictionary of movies files
genre_pkl_mapping = {
    'Fantasy': 'movies_title_fantasy.pkl',
    'Musical': 'movies_title_musical.pkl',
    'Adult': 'movies_title_adult.pkl',
    'Adventure': 'movies_title_adventure.pkl',
    'Animation': 'movies_title_animation.pkl',
    'Biography': 'movies_title_biography.pkl',
    'Crime': 'movies_title_crime.pkl',
    'Film-Noir': 'movies_title_film-noir.pkl',
    'Game-Show': 'movies_title_game-show.pkl',
    'History': 'movies_title_history.pkl',
    'Horror': 'movies_title_horror.pkl',
    'Music': 'movies_title_music.pkl',
    'Western': 'movies_title_western.pkl',
    'War': 'movies_title_war.pkl',
    'Thriller': 'movies_title_thriller.pkl',
    'Sport': 'movies_title_sport.pkl',
    'Sci-Fi': 'movies_title_sci-fi.pkl',
    'Reality-TV': 'movies_title_reality-tv.pkl',
    'Mystery': 'movies_title_mystery.pkl'
}


st.markdown(
    """
    <style>

        .title-text {
            background-color: #FFC0CB; 
            padding: 10px; 
            border-radius: 10px; 
        }

      
        .title-text h1 {
            font-family: 'Arial', sans-serif; 
            font-size: 36px; 
            font-weight: bold; 
            color: #000000;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='title-text'>PlayReview-Analysis</h1>", unsafe_allow_html=True)

url = 'https://adarshkaintura.github.io/PlayCool-Music-Player/'

if st.button('PlayCool Music'):
    webbrowser.open_new_tab(url)


# Load the dictionary of movie titles from the selected pickle file
genre = st.selectbox("Select Genre:", list(genre_pkl_mapping.keys()))

#
#
def print_picture(positive_count, negative_count, neutral_count, total_reviews):
    if total_reviews == 0:
        st.image("bored__.webp", caption="Neutral Sentiment")
    elif positive_count / total_reviews >= 0.6:
        st.image("good_movie.webp", caption="Positive Sentiment")
    elif (negative_count+neutral_count) / total_reviews >= 0.6:
        st.image("adfsf.webp", caption="Negative Sentiment")
    elif (positive_count+neutral_count /total_reviews) >=0.8:
        st.image("bored__.webp", caption="Worth considering")
    else:
        st.image("confused.webp", caption="Mixed Sentiment")





def get_movie_id(movie_name):
    try:
        movies_dict = pickle.load(open('movies_title.pkl', 'rb'))
        df_combined = pd.DataFrame(movies_dict)
        # we are converting the movies name  into lower case
        movie_name_lower = movie_name.lower()
        # checking if foudn the movie;
        if movie_name_lower in df_combined['name'].str.lower().values:
            # getting the id of the movie;
            movie_id = df_combined.loc[df_combined['name'].str.lower() == movie_name_lower, 'id'].iloc[0]
            return movie_id
        else:
            print("Movie not found in the dataset.")
            return None
    except Exception as e:
        print("Error:", e)
        return None



def scrape_reviews(movie_id):
    url = f"https://www.imdb.com/title/{movie_id}/reviews"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    reviews = []
    for review in soup.find_all('div', class_='text show-more__control'):
        reviews.append(review.text.strip())
    return reviews


def analyze_sentiment(reviews):
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    for review in reviews:
        analysis = TextBlob(review)
        if analysis.sentiment.polarity > 0.135:
            positive_count += 1
        elif analysis.sentiment.polarity < -0.1:
            negative_count += 1
        else:
            neutral_count += 1
    total_reviews = len(reviews)
    return (positive_count, negative_count, neutral_count, total_reviews)


def is_worth_watching(positive_count, negative_count, neutral_count, total_reviews):
    if total_reviews == 0:
        return "No reviews available."
    elif positive_count / total_reviews >= 0.6:
        return "Worth watching!"
    elif (negative_count + neutral_count) / total_reviews >= 0.6:
        return "Not worth watching!"
    elif (positive_count+neutral_count) / total_reviews > 0.8 :
        return "Worth considering, but not necessarily worth watching."
    else:
        return "Mixed reviews, watch at your own discretion."



def sentiment_on_movie(movie_name):
    closest_movie_id = get_movie_id(movie_name)
    reviews = scrape_reviews(closest_movie_id)#c tt10857164
    positive_count, negative_count, neutral_count, total_reviews = analyze_sentiment(reviews)
    verdict = is_worth_watching(positive_count, negative_count, neutral_count, total_reviews)
    return positive_count, negative_count, neutral_count, total_reviews, verdict, reviews

def print_reviews(reviews):
    st.subheader("Reviews")
    for i, review in enumerate(reviews[:5], start=1):
        st.write(f"Review {i}: {review}")
def analyse_movie_sentiments(movie_name):
    positive_count, negative_count, neutral_count, total_reviews, verdict,reviews = sentiment_on_movie(movie_name)
    st.write("Sentiment Analysis Result:")
    st.write(f"Positive Reviews: {positive_count}")
    st.write(f"Negative Reviews: {negative_count}")
    st.write(f"Neutral Reviews: {neutral_count}")
    st.write(f"Total Reviews: {total_reviews}")
    st.write(f"Verdict: {verdict}")

    print_picture(positive_count, negative_count, neutral_count,total_reviews)

   #these are additional details
    if total_reviews > 0:
        st.write(f"Percentage of Positive Reviews: {(positive_count / total_reviews) * 100:.2f}%")
        st.write(f"Percentage of Negative Reviews: {(negative_count / total_reviews) * 100:.2f}%")
        st.write(f'Selected Movie: {movie_name}')
        print_reviews(reviews)




movies_list = pickle.load(open(genre_pkl_mapping[genre], 'rb'))
# to choose the genre
movie_name = st.selectbox("Enter The Title Of The Movie", list(movies_list['name'].values()))


if st.button('Analyse'):
    analyse_movie_sentiments(movie_name)


