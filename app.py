import streamlit as st
import pickle
import pandas as pd

movie_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

similaritymatrix = pickle.load(open('similaritymatrix.pkl', 'rb'))


st.title('Movie Recommendations')

def recomend(movie,number=5):
    movie_index = movies[movies['original_title'] == movie].index[0]
    distancesarray = similaritymatrix[movie_index]
    movies_list = sorted(list(enumerate(distancesarray)), reverse=True, key=lambda x: x[1])[
                  1:number + 1]  # Exclude the movie itself

    recommended_movies=[]


    for j in movies_list:
        movie_id=j[0]
        #Fetch poster from API
        recommended_movies.append(movies.iloc[j[0]].original_title)

    return recommended_movies

option = st.selectbox(
    'Select Movie Recommendation',
    movies['original_title'].values,
    placeholder="Select or start typing",
    index=None
) #Option receives the selected option in the dropdown

left, right = st.columns([3.19,1])
with left:
    number_of_recc = st.number_input(
        'How many recommendations? (1-100)',
        placeholder='Enter a number between 1-100',
        value=5,
        min_value=1,max_value=100,
        icon="🔢"
    )
optionempty = True
btnpressed = False
with right:
    st.markdown(
        """
        <div style="
            font-size: 0.875rem;
            color: rgb(250, 250, 250);
            display: flex;
            visibility: visible;
            margin-bottom: 0.25rem;
            height: auto;
            min-height: 1.5rem;
            vertical-align: middle;
            flex-direction: row;
            -webkit-box-align: center;
            align-items: center;
        "
            <p></p>
        </div>
        """, unsafe_allow_html=True
    )
    if st.button(label='Recommend Movies'):
        btnpressed = True
        if option is not None:
            optionempty = False
            recommendations = recomend(option, number_of_recc)
        else:
            optionempty = True

if btnpressed:
    if optionempty:
        st.warning("No Movie Selected")
    else:
        st.subheader(f"Here's {number_of_recc} Movie Recommendations:")
        for i in recommendations:
            st.write(i)


#https://developer.themoviedb.org/reference/movie-details FOR API PURPOSES