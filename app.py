import streamlit as st
import os
from dotenv import load_dotenv
from agents import ResearchAgents
from data_loader import DataLoader

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="Virtual Research Assistant", page_icon="📚", layout="wide")

# Custom CSS for green background and responsive font
st.markdown(
    """
    <style>
    html, body, .stApp {
        height: 100%;
        margin: 0;
        padding: 0;
        background: linear-gradient(to bottom right, #d0f0c0, #a8e6a2, #8bcf88);
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
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

    .stTextInput > div > div > input {
        font-size: 1rem;
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
