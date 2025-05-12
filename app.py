import streamlit as st
import os
from dotenv import load_dotenv
from agents import ResearchAgents
from data_loader import DataLoader

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="Virtual Research Assistant", page_icon="📚", layout="wide")

# Custom CSS for blue background, black text, and white button
st.markdown(
    """
    <style>
    html, body, .stApp {
        height: 100%;
        margin: 0;
        padding: 0;
        background: linear-gradient(to bottom right, #d0e8ff, #a0c8ff, #70b0ff);
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
        color: black !important;
    }

    h1, h2, h3, h4, h5, h6, p, span, div {
        color: black !important;
    }

    /* Responsive font size for mobile */
    @media only screen and (max-width: 768px) {
        html, body, .stApp {
            font-size: 14px;
        }

        .stTextInput > div > div > input {
            color: #666 !important;  /* Text color */
            font-size: 1rem;
            font-weight: 400;
            background-color: white !important;  /* Search bar background */
            text-align: center !important;  /* Center the text */
        }

        /* Ensure placeholder text is visible and centered on mobile */
        .stTextInput input::placeholder {
            color: #666 !important;  /* Placeholder color */
            text-align: center !important;  /* Center the placeholder text */
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

    .stTextInput > div > div > input {
        font-size: 1rem;
        color: #666 !important;  /* Text color */
        background-color: white !important;  /* Search bar background */
        text-align: center !important;  /* Center the text */
    }

    /* Style the search button */
    .stButton>button {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ccc !important;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        font-weight: bold;
        border-radius: 6px;
    }

    .stButton>button:hover {
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

# User input
st.markdown("### 🔍 Enter Your Research Topic Below")
query = st.text_input("Topic", placeholder="e.g., Large Language Models in Healthcare")

# Search and process
if st.button("🔎 Search"):
    with st.spinner("Fetching and analyzing research papers..."):
        arxiv_papers = data_loader.fetch_arxiv_papers(query)
        all_papers = arxiv_papers

        if not all_papers:
            st.error("❌ Failed to fetch papers. Try a different topic.")
        else:
            processed_papers = []

            for paper in all_papers:
                summary = agents.summarize_paper(paper['summary'])
                adv_dis = agents.analyze_advantages_disadvantages(summary)

                processed_papers.append({
                    "title": paper["title"],
                    "link": paper["link"],
                    "summary": summary,
                    "advantages_disadvantages": adv_dis,
                })

            # Display results
            st.markdown("## 📄 Top Research Papers")
            for i, paper in enumerate(processed_papers, 1):
                with st.expander(f"{i}. {paper['title']}", expanded=False):
                    st.markdown(f"🔗 [**Read Full Paper**]({paper['link']})", unsafe_allow_html=True)
                    st.markdown("#### 📝 Summary")
                    st.write(paper["summary"])
                    st.markdown("#### ✅ Advantages & ❌ Disadvantages")
                    st.markdown(paper["advantages_disadvantages"])
                    st.markdown("---")
