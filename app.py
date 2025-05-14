import streamlit as st
import os
from dotenv import load_dotenv
from agents import ResearchAgents
from data_loader import DataLoader

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="Virtual Research Assistant", page_icon="📚", layout="wide")

# Custom CSS - updated to blue gradient and modified input/button styles
st.markdown(
    """
    <style>
    html, body, .stApp {
        height: 100%;
        margin: 0;
        padding: 0;
        background: linear-gradient(to bottom right, #cce5ff, #99ccff, #66b3ff);
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
        color: black !important;
    }

    h1, h2, h3, h4, h5, h6, p, span, div {
        color: black !important;
    }

    @media only screen and (max-width: 768px) {
        html, body, .stApp {
            font-size: 14px;
        }
    }

    h1 {
        font-size: 2.2rem !important;
        text-align: center;
        margin-top: 1rem;
    }

    p {
        font-size: 1.1rem;
        text-align: center;
    }

    /* Custom styles for search input and button */
    .stTextInput > div > div > input {
        background-color: white !important;
        color: black !important;
        font-size: 1rem;
        padding: 10px;
    }

    .stButton > button {
        background-color: white !important;
        color: black !important;
        font-size: 1rem;
        padding: 10px;
        border: 1px solid black !important;
    }

    .stButton > button:hover {
        background-color: #f0f0f0 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Title and intro
st.markdown("<h1>📚 Virtual Research Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p>Find, summarize, and analyze top research papers on any topic!</p>", unsafe_allow_html=True)
st.markdown("---")

# Retrieve API Key
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("❌ GROQ_API_KEY is missing. Please set it in your environment variables.")
    st.stop()

# Initialize agents and data loader
agents = ResearchAgents(groq_api_key)
data_loader = DataLoader()

# Input and automatic trigger
st.markdown("### 🔍 Enter Your Research Topic Below")

search_trigger = st.session_state.get("search_trigger", False)

def trigger_search():
    st.session_state.search_trigger = True

query = st.text_input("Topic", placeholder="e.g., Large Language Models in Healthcare", on_change=trigger_search, key="query_input")

# Search button (manually resets trigger to True)
if st.button("🔎 Search"):
    st.session_state.search_trigger = True

# Only process if triggered and query is present
if st.session_state.get("search_trigger") and st.session_state.get("query_input"):
    query = st.session_state.query_input
    with st.spinner("Fetching and analyzing research papers..."):
        arxiv_papers = data_loader.fetch_arxiv_papers(query)
        scholar_papers = data_loader.fetch_google_scholar_papers(query)

        if not arxiv_papers and not scholar_papers:
            st.error("❌ Failed to fetch papers. Try a different topic.")
        else:
            # ArXiv Section
            if arxiv_papers:
                st.markdown("## 📄 Research Papers from ArXiv")
                for i, paper in enumerate(arxiv_papers, 1):
                    summary = agents.summarize_paper(paper['summary'])
                    adv_dis = agents.analyze_advantages_disadvantages(summary)
                    with st.expander(f"{i}. {paper['title']}", expanded=False):
                        st.markdown(f"🔗 [**Read Full Paper**]({paper['link']})", unsafe_allow_html=True)
                        st.markdown("#### 📝 Summary")
                        st.write(summary)
                        st.markdown("#### ✅ Advantages & ❌ Disadvantages")
                        st.markdown(adv_dis)
                        st.markdown("---")
            else:
                st.warning("No ArXiv papers found.")

            # Google Scholar Section
            if scholar_papers:
                st.markdown("## 📄 Research Papers from Google Scholar")
                for i, paper in enumerate(scholar_papers, 1):
                    summary = agents.summarize_paper(paper['summary'])
                    adv_dis = agents.analyze_advantages_disadvantages(summary)
                    with st.expander(f"{i}. {paper['title']}", expanded=False):
                        st.markdown(f"🔗 [**Read Full Paper**]({paper['link']})", unsafe_allow_html=True)
                        st.markdown("#### 📝 Summary")
                        st.write(summary)
                        st.markdown("#### ✅ Advantages & ❌ Disadvantages")
                        st.markdown(adv_dis)
                        st.markdown("---")
            else:
                st.warning("No Google Scholar papers found.")

    # Reset the trigger so it doesn't rerun automatically
    st.session_state.search_trigger = False
