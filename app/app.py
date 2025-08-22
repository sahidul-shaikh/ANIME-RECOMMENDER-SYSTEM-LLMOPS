import streamlit as st
from pipeline.pipeline import AnimeRecommendationPipeline
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Anime Recommender", page_icon=":sparkles:", layout="wide")
st.title("Anime Recommender System")

@st.cache_resource
def init_pipeline():
    return AnimeRecommendationPipeline()

pipeline = init_pipeline()

query  = st.text_input("Enter your query:", placeholder="Light hearted anime with comedy and romance")
if st.button("Get Recommendations"):
    if query:
        with st.spinner("Generating recommendations..."):
            try:
                recommendations = pipeline.recommend(query)
                st.success("Recommendations generated successfully!")
                st.write(recommendations)
            except Exception as e:
                st.error(f"Error during recommendation: {str(e)}")
    else:
        st.warning("Please enter a query to get recommendations.")