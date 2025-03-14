import os
from unittest.mock import patch
import pytest
import requests
from requests_mock import Mocker
from pubMed_fetcher.fetcher import PubMedFetcher  # Adjust the import path

# Mock environment variables
@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(os.environ, {"BASE_URL": "https://example.com/search", "FETCH_URL": "https://example.com/fetch"}):
        yield

# Mock the PubMed API responses
@pytest.fixture
def mock_pubmed_responses():
    with Mocker() as m:
        # Mock the search response
        m.get("https://example.com/search", json={
            "esearchresult": {
                "idlist": ["12345", "67890"]
            }
        })
        # Mock the fetch response
        m.get("https://example.com/fetch", json={
            "result": {
                "12345": {
                    "title": "Test Paper 1",
                    "pubdate": "2023-01-01",
                    "authors": [
                        {"name": "Author A", "affiliation": "Company X"},
                        {"name": "Author B", "affiliation": "University Y"}
                    ],
                    "elocationid": "authorA@example.com"
                },
                "67890": {
                    "title": "Test Paper 2",
                    "pubdate": "2023-02-01",
                    "authors": [
                        {"name": "Author C", "affiliation": "Company Z"},
                        {"name": "Author D", "affiliation": "University W"}
                    ],
                    "elocationid": "authorC@example.com"
                }
            }
        })
        yield m

# Test the PubMedFetcher class
def test_fetch_papers(mock_pubmed_responses):
    fetcher = PubMedFetcher(email="test@example.com", debug=True)
    papers = fetcher.fetch_papers(query="cancer", max_results=2)

    # Assertions
    assert len(papers) == 2

    # Check the first paper
    assert papers[0]["PubmedID"] == "12345"
    assert papers[0]["Title"] == "Test Paper 1"
    assert papers[0]["PublicationDate"] == "2023-01-01"
    assert papers[0]["NonAcademicAuthors"] == ["Author A", "Author B"]
    assert papers[0]["CompanyAffiliations"] == ["company x", "university y"]
    assert papers[0]["CorrespondingAuthorEmail"] == "authorA@example.com"

    # Check the second paper
    assert papers[1]["PubmedID"] == "67890"
    assert papers[1]["Title"] == "Test Paper 2"
    assert papers[1]["PublicationDate"] == "2023-02-01"
    assert papers[1]["NonAcademicAuthors"] == ["Author C", "Author D"]
    assert papers[1]["CompanyAffiliations"] == ["company z", "university w"]
    assert papers[1]["CorrespondingAuthorEmail"] == "authorC@example.com"

# Test error handling
def test_fetch_papers_error_handling():
    fetcher = PubMedFetcher(email="test@example.com", debug=True)

    with patch('requests.get', side_effect=requests.RequestException("API Error")):
        papers = fetcher.fetch_papers(query="cancer", max_results=2)
        assert papers == []

# Test no paper IDs found
def test_fetch_papers_no_ids(mock_pubmed_responses):
    # Override the search response to return no IDs
    mock_pubmed_responses.get("https://example.com/search", json={
        "esearchresult": {
            "idlist": []
        }
    })

    fetcher = PubMedFetcher(email="test@example.com", debug=True)
    papers = fetcher.fetch_papers(query="cancer", max_results=2)

    assert papers == []