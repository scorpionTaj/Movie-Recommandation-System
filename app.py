import streamlit as st
import pickle
import requests
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

if "theme" not in st.session_state:
    st.session_state.theme = "light"


def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"


def load_css():
    if st.session_state.theme == "dark":
        bg_color = "#121212"
        text_color = "#FFFFFF"
        card_bg = "#1E1E1E"
        accent_color = "#BB86FC"
        secondary_accent = "#03DAC5"
        section_bg = "#2D2D2D"
    else:
        bg_color = "#FFFFFF"
        text_color = "#333333"
        card_bg = "#F9F9F9"
        accent_color = "#6200EE"
        secondary_accent = "#03DAC6"
        section_bg = "#EAEAEA"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        .title {{
            text-align: center;
            margin-bottom: 20px;
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(45deg, {accent_color}, {secondary_accent});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            padding: 10px 0;
        }}
        .subtitle {{
            text-align: center;
            margin-bottom: 30px;
            font-style: italic;
            color: {'rgba(255,255,255,0.7)' if st.session_state.theme == 'dark' else 'rgba(0,0,0,0.6)'};
        }}
        .movie-card {{
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 8px 20px {'rgba(0,0,0,0.5)' if st.session_state.theme == 'dark' else 'rgba(0,0,0,0.2)'};
            margin-bottom: 20px;
            position: relative;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            background: {card_bg};
        }}
        .movie-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 15px 30px {'rgba(0,0,0,0.8)' if st.session_state.theme == 'dark' else 'rgba(0,0,0,0.3)'};
        }}
        .movie-info {{
            padding: 12px;
            background: {'rgba(30,30,30,0.9)' if st.session_state.theme == 'dark' else 'rgba(249,249,249,0.9)'};
            color: {text_color};
            position: absolute;
            bottom: 0;
            width: 100%;
            backdrop-filter: blur(8px);
            border-top: 1px solid {'rgba(255,255,255,0.1)' if st.session_state.theme == 'dark' else 'rgba(0,0,0,0.1)'};
        }}
        .rating-badge {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: {'rgba(187,134,252,0.9)' if st.session_state.theme == 'dark' else 'rgba(98,0,238,0.9)'};
            color: {'#121212' if st.session_state.theme == 'dark' else 'white'};
            border-radius: 50%;
            width: 45px;
            height: 45px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            box-shadow: 0 2px 8px {'rgba(0,0,0,0.5)' if st.session_state.theme == 'dark' else 'rgba(0,0,0,0.3)'};
            font-size: 0.9rem;
        }}
        .similarity-badge {{
            position: absolute;
            top: 10px;
            left: 10px;
            background: {'rgba(3,218,197,0.9)' if st.session_state.theme == 'dark' else 'rgba(3,218,198,0.9)'};
            color: {'#121212' if st.session_state.theme == 'dark' else 'white'};
            border-radius: 20px;
            padding: 5px 12px;
            font-size: 0.8rem;
            font-weight: bold;
            box-shadow: 0 2px 8px {'rgba(0,0,0,0.5)' if st.session_state.theme == 'dark' else 'rgba(0,0,0,0.2)'};
        }}
        .genre-tag {{
            display: inline-block;
            background: {'rgba(187,134,252,0.2)' if st.session_state.theme == 'dark' else 'rgba(98,0,238,0.1)'};
            color: {'rgba(187,134,252,1)' if st.session_state.theme == 'dark' else 'rgba(98,0,238,1)'};
            border-radius: 20px;
            padding: 4px 12px;
            margin-right: 6px;
            margin-bottom: 6px;
            font-size: 0.8rem;
            border: 1px solid {'rgba(187,134,252,0.3)' if st.session_state.theme == 'dark' else 'rgba(98,0,238,0.2)'};
            transition: all 0.2s ease;
        }}
        .genre-tag:hover {{
            background: {'rgba(187,134,252,0.3)' if st.session_state.theme == 'dark' else 'rgba(98,0,238,0.2)'};
        }}
        .section-header {{
            padding: 12px 20px;
            border-radius: 12px;
            margin: 30px 0 20px 0;
            background: {section_bg};
            border-left: 5px solid {accent_color};
        }}
        .custom-button {{
            background: {accent_color};
            color: {'#121212' if st.session_state.theme == 'dark' else 'white'};
            padding: 12px 20px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            text-align: center;
            margin: 12px auto;
            display: block;
            transition: all 0.3s ease;
            font-weight: bold;
            box-shadow: 0 4px 6px {'rgba(0,0,0,0.5)' if st.session_state.theme == 'dark' else 'rgba(0,0,0,0.2)'};
        }}
        .custom-button:hover {{
            opacity: 0.9;
            transform: scale(1.03);
            box-shadow: 0 6px 10px {'rgba(0,0,0,0.7)' if st.session_state.theme == 'dark' else 'rgba(0,0,0,0.3)'};
        }}
        .detail-container {{
            border-radius: 16px;
            padding: 25px;
            box-shadow: 0 6px 18px {'rgba(0,0,0,0.4)' if st.session_state.theme == 'dark' else 'rgba(0,0,0,0.15)'};
            background: {card_bg};
            margin-bottom: 25px;
            border: 1px solid {'rgba(255,255,255,0.1)' if st.session_state.theme == 'dark' else 'rgba(0,0,0,0.05)'};
        }}
        .favorite-btn {{
            background-color: {'rgba(255,215,0,0.1)' if st.session_state.theme == 'dark' else 'rgba(255,215,0,0.1)'};
            color: #FFD700;
            border: 2px solid #FFD700;
            border-radius: 30px;
            padding: 8px 18px;
            font-weight: bold;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
            margin: 10px 0;
        }}
        .favorite-btn:hover {{
            background-color: rgba(255,215,0,0.2);
            transform: translateY(-2px);
        }}
        .history-item {{
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            border: 1px solid {'rgba(255,255,255,0.1)' if st.session_state.theme == 'dark' else 'rgba(0,0,0,0.05)'};
            background: {'rgba(30,30,30,0.4)' if st.session_state.theme == 'dark' else 'rgba(249,249,249,0.7)'};
        }}
        .history-item:hover {{
            background: {'rgba(187,134,252,0.2)' if st.session_state.theme == 'dark' else 'rgba(98,0,238,0.1)'};
            transform: translateX(5px);
        }}
        /* Loading animation */
        .loader {{
            width: 50px;
            height: 50px;
            border: 5px solid {'rgba(255,255,255,0.2)' if st.session_state.theme == 'dark' else 'rgba(0,0,0,0.1)'};
            border-radius: 50%;
            border-top-color: {accent_color};
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }}
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
        /* Improved button styles */
        .stButton>button {{
            background: {accent_color};
            color: {'#121212' if st.session_state.theme == 'dark' else 'white'};
            border-radius: 8px;
            border: none;
            padding: 10px 15px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px {'rgba(0,0,0,0.5)' if st.session_state.theme == 'dark' else 'rgba(0,0,0,0.2)'};
        }}
        .stButton>button:hover {{
            opacity: 0.9;
            transform: translateY(-2px);
            box-shadow: 0 6px 10px {'rgba(0,0,0,0.7)' if st.session_state.theme == 'dark' else 'rgba(0,0,0,0.3)'};
        }}
        /* Improved select box */
        .stSelectbox>div>div {{
            background: {card_bg};
            border-radius: 8px;
            border: 1px solid {'rgba(255,255,255,0.2)' if st.session_state.theme == 'dark' else 'rgba(0,0,0,0.1)'};
        }}
        /* Scrollbar styling */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: {'rgba(30,30,30,0.4)' if st.session_state.theme == 'dark' else 'rgba(249,249,249,0.7)'};
        }}
        ::-webkit-scrollbar-thumb {{
            background: {accent_color};
            border-radius: 10px;
        }}
        /* Improved text input */
        .stTextInput>div>div>input {{
            background: {card_bg};
            border: 1px solid {'rgba(255,255,255,0.2)' if st.session_state.theme == 'dark' else 'rgba(0,0,0,0.1)'};
            border-radius: 8px;
            padding: 10px 15px;
            color: {text_color};
        }}
        /* Star rating visualization */
        .star-rating {{
            color: #FFD700;
            font-size: 1.2rem;
            letter-spacing: 2px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


load_css()


@st.cache_data(ttl=3600)
def fetch_movie_details(movie_id):
    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        return {"error": "API key not found"}

    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-us"

    try:
        response = requests.get(movie_url)
        response.raise_for_status()
        data = response.json()

        genres = [genre["name"] for genre in data.get("genres", [])]

        videos_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}&language=en-us"
        videos_response = requests.get(videos_url)
        videos_response.raise_for_status()
        videos_data = videos_response.json()

        trailer_key = None
        for video in videos_data.get("results", []):
            if video.get("type") == "Trailer" and video.get("site") == "YouTube":
                trailer_key = video.get("key")
                break

        credits_url = (
            f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"
        )
        credits_response = requests.get(credits_url)
        credits_response.raise_for_status()
        credits_data = credits_response.json()

        cast = [
            {"name": member.get("name"), "character": member.get("character")}
            for member in credits_data.get("cast", [])[:5]
        ]

        director = next(
            (
                person.get("name")
                for person in credits_data.get("crew", [])
                if person.get("job") == "Director"
            ),
            "Unknown",
        )

        return {
            "title": data.get("title"),
            "overview": data.get("overview", "Description not available"),
            "poster_path": (
                f"https://image.tmdb.org/t/p/w500/{data.get('poster_path')}"
                if data.get("poster_path")
                else None
            ),
            "backdrop_path": (
                f"https://image.tmdb.org/t/p/w1280/{data.get('backdrop_path')}"
                if data.get("backdrop_path")
                else None
            ),
            "rating": data.get("vote_average", "N/A"),
            "release_date": data.get("release_date", "N/A"),
            "runtime": data.get("runtime", "N/A"),
            "genres": genres,
            "trailer_key": trailer_key,
            "cast": cast,
            "director": director,
            "popularity": data.get("popularity", 0),
        }
    except requests.exceptions.RequestException:
        return None


@st.cache_data
def load_data():
    movies = pickle.load(open("movies.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
    return movies, similarity


@st.cache_data
def recommend(movie, num_movies=5, start_index=0):
    try:
        index = movies[movies["title"] == movie].index[0]
        distances = sorted(
            list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1]
        )
        recommended_movie_ids = [
            movies.iloc[i[0]].id
            for i in distances[start_index + 1 : start_index + 1 + num_movies]
        ]
        recommended_movie_titles = [
            movies.iloc[i[0]].title
            for i in distances[start_index + 1 : start_index + 1 + num_movies]
        ]
        similarity_scores = [
            round(distances[i + 1 + start_index][1] * 100) for i in range(num_movies)
        ]
        return recommended_movie_ids, recommended_movie_titles, similarity_scores
    except IndexError:
        st.error("Movie not found in the dataset.")
        return [], [], []


def display_movie_details(movie_id):
    details = fetch_movie_details(movie_id)
    if details:
        if details.get("error"):
            st.error(details["error"])
            return

        with st.spinner("Loading movie details..."):
            if details.get("backdrop_path"):
                st.image(details["backdrop_path"], use_container_width=True)

            with st.container():
                st.markdown(f'<div class="detail-container">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 2])

                with col1:
                    if details["poster_path"]:
                        st.image(details["poster_path"], use_container_width=True)
                    else:
                        st.image(
                            "https://via.placeholder.com/300x450?text=No+Poster",
                            use_container_width=True,
                        )

                    if "favorites" not in st.session_state:
                        st.session_state.favorites = []

                    is_favorite = movie_id in st.session_state.favorites

                    favorite_text = (
                        "★ Remove from Favorites"
                        if is_favorite
                        else "☆ Add to Favorites"
                    )

                    if st.button(
                        favorite_text,
                        key=f"fav_{movie_id}",
                    ):
                        if is_favorite:
                            st.session_state.favorites.remove(movie_id)
                        else:
                            st.session_state.favorites.append(movie_id)
                        st.rerun()

                with col2:
                    st.header(details["title"])

                    if "history" not in st.session_state:
                        st.session_state.history = []

                    if movie_id not in st.session_state.history:
                        st.session_state.history.insert(0, movie_id)
                        st.session_state.history = st.session_state.history[:10]

                    rating = details["rating"]
                    if rating != "N/A":
                        try:
                            rating = float(rating)
                            full_stars = int(rating // 2)
                            half_star = rating % 2 >= 1
                            empty_stars = 5 - full_stars - (1 if half_star else 0)

                            star_display = "★" * full_stars
                            if half_star:
                                star_display += "½"
                            star_display += "☆" * empty_stars
                            st.markdown(
                                f"**Rating:** {rating}/10 <span class='star-rating'>{star_display}</span>",
                                unsafe_allow_html=True,
                            )
                        except:
                            st.markdown(f"**Rating:** {rating}/10")
                    else:
                        st.markdown("**Rating:** Not available")

                    st.markdown(f"**Director:** {details['director']}")
                    st.markdown(f"**Release Date:** {details['release_date']}")
                    st.markdown(f"**Runtime:** {details['runtime']} minutes")

                    st.markdown("**Genres:**")
                    genre_html = " ".join(
                        [
                            f'<span class="genre-tag">{genre}</span>'
                            for genre in details.get("genres", [])
                        ]
                    )
                    st.markdown(genre_html, unsafe_allow_html=True)

                    if details.get("cast"):
                        st.markdown("**Cast:**")
                        for actor in details["cast"]:
                            st.markdown(f"• {actor['name']} as *{actor['character']}*")

                    st.markdown("### Overview")
                    st.write(details["overview"])

                    if details.get("trailer_key"):
                        st.markdown("### Trailer")
                        video_url = (
                            f"https://www.youtube.com/watch?v={details['trailer_key']}"
                        )
                        st.video(video_url)

                st.markdown("</div>", unsafe_allow_html=True)


def display_recommendations(
    movie_ids, movie_titles, similarity_scores=None, is_additional=False
):
    num_columns = min(len(movie_ids), 3)
    if num_columns > 0:
        for i in range(0, len(movie_ids), num_columns):
            cols = st.columns(num_columns)

            for j in range(num_columns):
                if i + j < len(movie_ids):
                    movie_id = movie_ids[i + j]
                    movie_title = movie_titles[i + j]
                    similarity = similarity_scores[i + j] if similarity_scores else None

                    with cols[j]:
                        details = fetch_movie_details(movie_id)
                        if details and details.get("poster_path"):
                            similarity_badge = ""
                            if similarity is not None:
                                similarity_badge = f'<div class="similarity-badge">{similarity}% match</div>'

                            genres_html = ""
                            if details.get("genres"):
                                genres = details.get("genres")[:2]
                                genres_text = ", ".join(genres)
                                genres_html = f"<div style='font-size: 0.7rem; opacity: 0.8;'>{genres_text}</div>"

                            html_content = f"""
                            <div class="movie-card">
                                <div style="position:relative;">
                                    <img src="{details["poster_path"]}" style="width:100%;">
                                    <div class="rating-badge">{details["rating"] if details["rating"] != "N/A" else "-"}</div>
                                    {similarity_badge}
                                    <div class="movie-info">
                                        <strong>{movie_title}</strong><br>
                                        {details["release_date"][:4] if details["release_date"] and details["release_date"] != "N/A" else ""}
                                        {genres_html}
                                    </div>
                                </div>
                            </div>
                            """
                            st.markdown(html_content, unsafe_allow_html=True)

                            if st.button(
                                f"View Details", key=f"{movie_id}_{is_additional}"
                            ):
                                st.session_state.selected_movie_id = movie_id
                                st.rerun()
                        else:
                            st.text(movie_title)
                            st.warning("Poster not available.")


def display_favorites():
    if "favorites" not in st.session_state or not st.session_state.favorites:
        st.info("You haven't added any favorites yet.")
        return

    st.markdown(
        '<div class="section-header"><h2>My Favorite Movies</h2></div>',
        unsafe_allow_html=True,
    )

    favorite_ids = st.session_state.favorites
    favorite_titles = []

    for movie_id in favorite_ids:
        details = fetch_movie_details(movie_id)
        if details:
            favorite_titles.append(details["title"])
        else:
            favorite_titles.append(f"Movie {movie_id}")

    display_recommendations(favorite_ids, favorite_titles, is_additional=True)


def display_history():
    if "history" not in st.session_state or not st.session_state.history:
        return

    with st.expander("Recently Viewed Movies"):
        history_ids = st.session_state.history
        for movie_id in history_ids:
            details = fetch_movie_details(movie_id)
            if details:
                col1, col2 = st.columns([1, 4])
                with col1:
                    if details.get("poster_path"):
                        st.image(details["poster_path"], width=80)
                    else:
                        st.write("🎬")
                with col2:
                    if st.button(details["title"], key=f"history_{movie_id}"):
                        st.session_state.selected_movie_id = movie_id
                        st.rerun()
                    release_year = (
                        details["release_date"][:4]
                        if details["release_date"] and details["release_date"] != "N/A"
                        else ""
                    )
                    st.caption(
                        f"{release_year} | {', '.join(details.get('genres', [])[:2])}"
                    )


def display_settings():
    st.markdown(
        '<div class="section-header"><h2>Settings</h2></div>', unsafe_allow_html=True
    )

    tabs = st.tabs(["Appearance", "Recommendations", "Data Management"])

    with tabs[0]:
        st.markdown("### Appearance Settings")

        st.subheader("Theme")
        col1, col2 = st.columns([1, 3])
        with col1:
            theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
            st.write(f"{theme_icon} Current Theme:")
        with col2:
            st.write(st.session_state.theme.capitalize())

        if st.button("Toggle Dark/Light Mode"):
            toggle_theme()
            st.rerun()

        st.subheader("UI Customization")

        if "font_size" not in st.session_state:
            st.session_state.font_size = "Medium"

        font_size = st.select_slider(
            "Font Size",
            options=["Small", "Medium", "Large"],
            value=st.session_state.font_size,
        )

        if font_size != st.session_state.font_size:
            st.session_state.font_size = font_size
            st.success(
                f"Font size set to {font_size}. This will be implemented in a future update."
            )

    with tabs[1]:
        st.markdown("### Recommendation Settings")

        if "default_num_recommendations" not in st.session_state:
            st.session_state.default_num_recommendations = 6

        default_num = st.slider(
            "Number of recommendations to show initially",
            min_value=3,
            max_value=12,
            value=st.session_state.default_num_recommendations,
            step=3,
        )

        if default_num != st.session_state.default_num_recommendations:
            st.session_state.default_num_recommendations = default_num
            st.session_state.num_shown = default_num
            st.success(f"Default recommendations count set to {default_num}")

        st.subheader("Genre Preferences")

        if "preferred_genres" not in st.session_state:
            st.session_state.preferred_genres = []

        all_genres = [
            "Action",
            "Adventure",
            "Animation",
            "Comedy",
            "Crime",
            "Documentary",
            "Drama",
            "Family",
            "Fantasy",
            "History",
            "Horror",
            "Music",
            "Mystery",
            "Romance",
            "Science Fiction",
            "Thriller",
            "War",
            "Western",
        ]

        preferred_genres = st.multiselect(
            "Select your preferred genres (Will prioritize these in future updates)",
            all_genres,
            default=st.session_state.preferred_genres,
        )

        if preferred_genres != st.session_state.preferred_genres:
            st.session_state.preferred_genres = preferred_genres
            st.success(
                f"Genre preferences updated: {', '.join(preferred_genres) if preferred_genres else 'No preferences'}"
            )

        if "min_rating" not in st.session_state:
            st.session_state.min_rating = 0.0

        min_rating = st.slider(
            "Minimum movie rating to include (0-10)",
            min_value=0.0,
            max_value=9.0,
            value=st.session_state.min_rating,
            step=0.5,
        )

        if min_rating != st.session_state.min_rating:
            st.session_state.min_rating = min_rating
            st.success(
                f"Minimum rating set to {min_rating}. This will be implemented in a future update."
            )

    with tabs[2]:
        st.markdown("### Data Management")

        st.subheader("Watch History")
        history_count = (
            len(st.session_state.history) if "history" in st.session_state else 0
        )
        st.write(f"You have {history_count} movies in your watch history.")

        if st.button("Clear Watch History"):
            if "history" in st.session_state:
                st.session_state.history = []
                st.success("Watch history cleared!")
            else:
                st.info("No watch history to clear.")

        st.subheader("Favorites")
        favorites_count = (
            len(st.session_state.favorites) if "favorites" in st.session_state else 0
        )
        st.write(f"You have {favorites_count} movies in your favorites.")

        if st.button("Clear Favorites"):
            if "favorites" in st.session_state:
                st.session_state.favorites = []
                st.success("Favorites cleared!")
            else:
                st.info("No favorites to clear.")

        st.subheader("Reset All Settings")
        st.warning("This will reset all your preferences and data.")

        if st.button("Reset Everything", type="primary"):
            for key in list(st.session_state.keys()):
                if key != "theme":
                    del st.session_state[key]
            st.success("All settings and data have been reset!")
            st.rerun()

    st.markdown("---")
    st.markdown("### About")
    st.write("Movie Recommendation System v1.1")
    st.write("Built with Streamlit and TMDB API")
    st.write("© 2025 ")


def main():
    with st.sidebar:
        st.markdown("## 🎬 Movie Explorer")

        page = st.radio("Navigation", ["Home", "Favorites", "Settings"])

        theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
        if st.button(f"{theme_icon} Toggle Theme"):
            toggle_theme()
            st.rerun()

        st.markdown("---")

        display_history()
    load_css()

    if page == "Favorites":
        display_favorites()
        return
    elif page == "Settings":
        display_settings()
        return

    st.markdown(
        "<h1 class='title'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True
    )
    st.markdown(
        "<p class='subtitle'>Find your next favorite movie with AI-powered recommendations</p>",
        unsafe_allow_html=True,
    )

    global movies, similarity
    movies, similarity = load_data()

    col1, col2 = st.columns([2, 1])

    with col1:
        search_query = st.text_input("🔍 Search for a movie", "")

    movies_list = movies["title"].values
    if search_query:
        movies_list = [m for m in movies_list if search_query.lower() in m.lower()]
        if not movies_list:
            st.warning("No movies found matching your search.")
            movies_list = movies["title"].values

    selected_movie = st.selectbox("Select a movie to get recommendations:", movies_list)

    if "selected_movie_id" not in st.session_state:
        st.session_state.selected_movie_id = None
    if "num_shown" not in st.session_state:
        st.session_state.num_shown = 6
    if "show_recommendations" not in st.session_state:
        st.session_state.show_recommendations = False
    if "recommendations_ids" not in st.session_state:
        st.session_state.recommendations_ids = []
    if "recommendations_titles" not in st.session_state:
        st.session_state.recommendations_titles = []
    if "similarity_scores" not in st.session_state:
        st.session_state.similarity_scores = []

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("🎯 Get Recommendations", use_container_width=True):
            st.session_state.num_shown = 6
            st.session_state.show_recommendations = True
            (
                st.session_state.recommendations_ids,
                st.session_state.recommendations_titles,
                st.session_state.similarity_scores,
            ) = recommend(selected_movie, num_movies=12)

    with col2:
        if st.button("🔄 Clear Selection", use_container_width=True):
            st.session_state.selected_movie_id = None

    if st.session_state.selected_movie_id:
        st.markdown(
            '<div class="section-header"><h2>Selected Movie</h2></div>',
            unsafe_allow_html=True,
        )
        with st.container():
            display_movie_details(st.session_state.selected_movie_id)

    if st.session_state.show_recommendations and st.session_state.recommendations_ids:
        st.markdown(
            '<div class="section-header"><h2>Recommended Movies</h2></div>',
            unsafe_allow_html=True,
        )

        sort_options = ["Similarity", "Rating", "Release Date", "Popularity"]
        sort_by = st.selectbox("Sort by:", sort_options)

        rec_details = []
        for i, movie_id in enumerate(st.session_state.recommendations_ids):
            details = fetch_movie_details(movie_id)
            if details:
                rec_details.append(
                    {
                        "id": movie_id,
                        "title": st.session_state.recommendations_titles[i],
                        "similarity": (
                            st.session_state.similarity_scores[i]
                            if i < len(st.session_state.similarity_scores)
                            else 0
                        ),
                        "rating": (
                            float(details["rating"])
                            if details["rating"] != "N/A"
                            else 0
                        ),
                        "release_date": (
                            details["release_date"]
                            if details["release_date"] != "N/A"
                            else "1900-01-01"
                        ),
                        "popularity": details["popularity"],
                    }
                )

        if sort_by == "Rating":
            rec_details = sorted(rec_details, key=lambda x: x["rating"], reverse=True)
        elif sort_by == "Release Date":
            rec_details = sorted(
                rec_details, key=lambda x: x["release_date"], reverse=True
            )
        elif sort_by == "Popularity":
            rec_details = sorted(
                rec_details, key=lambda x: x["popularity"], reverse=True
            )

        sorted_ids = [item["id"] for item in rec_details[: st.session_state.num_shown]]
        sorted_titles = [
            item["title"] for item in rec_details[: st.session_state.num_shown]
        ]
        sorted_scores = [
            item["similarity"] for item in rec_details[: st.session_state.num_shown]
        ]

        display_recommendations(sorted_ids, sorted_titles, sorted_scores)

        if st.session_state.num_shown < len(st.session_state.recommendations_ids):
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("Load More Recommendations", key="load_more"):
                    st.session_state.num_shown += 6

        elif st.session_state.num_shown >= len(st.session_state.recommendations_ids):
            st.info("No more recommendations available.")

    elif (
        st.session_state.show_recommendations
        and not st.session_state.recommendations_ids
    ):
        st.error("No recommendations found.")


if __name__ == "__main__":
    main()
