import streamlit as st
import os
from dotenv import load_dotenv
from agents import ResearchAgents
from data_loader import DataLoader

# Load environment variables
load_dotenv()
st.set_page_config(page_title="Virtual Research Assistant", page_icon="📚", layout="wide")
# Custom CSS for background
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to bottom right, #e0f7fa, #b3e5fc, #81d4fa);
    }
    .stApp {
        background: linear-gradient(to bottom right, #e0f7fa, #b3e5fc, #81d4fa);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page Configuration


# Title and Intro
st.markdown("<h1 style='text-align: center;'>📚 Virtual Research Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Find, summarize, and analyze top research papers on any topic!</p>", unsafe_allow_html=True)
st.markdown("---")

# Retrieve API Key
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("❌ GROQ_API_KEY is missing. Please set it in your environment variables.")
    st.stop()

# Initialize agents and data loader
agents = ResearchAgents(groq_api_key)
data_loader = DataLoader()

# User Input Section
st.markdown("### 🔍 Enter Your Research Topic Below")
query = st.text_input("Topic", placeholder="e.g., Large Language Models in Healthcare")

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
