import requests
from typing import List, Dict, Any
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

class PubMedFetcher:
    def __init__(self, email: str, debug: bool = False):
        self.email = email
        self.debug = debug
        self.base_url = os.getenv("BASE_URL")
        self.fetch_url = os.getenv("FETCH_URL")
        
        if not self.base_url or not self.fetch_url:
            raise ValueError("BASE_URL or FETCH_URL not found in environment variables.")

    def fetch_papers(self, query: str, max_results: int = 100) -> List[Dict[str, Any]]:
        try:
            if self.debug:
                print(f"Fetching papers for query: {query} & for max_result: {max_results}")

            search_params = {
                'db': 'pubmed',
                'term': query,
                'retmax': max_results,
                'retmode': 'json',
                'email': self.email
            }
            response = requests.get(self.base_url, params=search_params)
            response.raise_for_status()
            paper_ids = response.json().get('esearchresult', {}).get('idlist', [])

            if not paper_ids:
                print(f"No paper IDs found for the given query: {query}.")
                return []

            if self.debug:
                print(f"Paper IDs fetched: {paper_ids}")

            fetch_params = {
                'db': 'pubmed',
                'id': ','.join(paper_ids),
                'retmode': 'json'
            }
            fetch_response = requests.get(self.fetch_url, params=fetch_params)
            fetch_response.raise_for_status()
            paper_summaries = fetch_response.json().get('result', {})
            # print(paper_summaries)

            if self.debug:
                print("Paper summaries fetched successfully")

            papers = []
            for paper_id in paper_ids:
                paper_info = paper_summaries.get(paper_id, {})
                authors = paper_info.get('authors', [])

                non_academic_authors = []
                company_affiliations = []

                for author in authors:
                    non_academic_authors.append(author.get('name'))
                    affiliation = author.get('affiliation', '').lower()
                    if affiliation:
                        company_affiliations.append(affiliation)

                papers.append({
                    'PubmedID': paper_id,
                    'Title': paper_info.get('title', 'N/A'),
                    'PublicationDate': paper_info.get('pubdate', 'N/A'),
                    'NonAcademicAuthors': non_academic_authors,
                    'CompanyAffiliations': company_affiliations,
                    'CorrespondingAuthorEmail': paper_info.get('elocationid', 'N/A')
                })

            return papers
        except requests.RequestException as e:
            print(f"Error fetching data from PubMed API: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []
