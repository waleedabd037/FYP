import requests
import xml.etree.ElementTree as ET
from scholarly import scholarly

class DataLoader:
    def __init__(self):
        print("DataLoader Init")

    def fetch_arxiv_papers(self, query):
        """
        Fetches up to 5 research papers from ArXiv based on the user query.
        
        Returns:
            list: A list of dictionaries containing paper details (title, summary, link).
        """

        def search_arxiv(query):
            """Helper function to query ArXiv API."""
            url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5"
            response = requests.get(url)
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                return [
                    {
                        "title": entry.find("{http://www.w3.org/2005/Atom}title").text,
                        "summary": entry.find("{http://www.w3.org/2005/Atom}summary").text,
                        "link": entry.find("{http://www.w3.org/2005/Atom}id").text
                    }
                    for entry in root.findall("{http://www.w3.org/2005/Atom}entry")
                ]
            return []

        papers = search_arxiv(query)

        if not papers:
            print("No ArXiv papers found for this query.")
        elif len(papers) < 5:
            print(f"Only {len(papers)} ArXiv papers found.")

        return papers[:5]  # Ensure max 5 results

    def fetch_google_scholar_papers(self, query):
        """
        Fetches up to 5 research papers from Google Scholar based on the user query.
        
        Returns:
            list: A list of dictionaries containing paper details (title, summary, link).
        """
        papers = []
        try:
            search_results = scholarly.search_pubs(query)

            for i, paper in enumerate(search_results):
                if i >= 5:
                    break
                papers.append({
                    "title": paper["bib"]["title"],
                    "summary": paper["bib"].get("abstract", "No summary available"),
                    "link": paper.get("pub_url", "No link available")
                })
        except Exception as e:
            print(f"Google Scholar error: {e}")

        if not papers:
            print("No Google Scholar papers found for this query.")
        elif len(papers) < 5:
            print(f"Only {len(papers)} Google Scholar papers found.")

        return papers[:5]  # Ensure max 5 results
