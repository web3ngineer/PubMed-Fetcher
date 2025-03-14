import csv
from typing import List, Dict, Any

def save_as_csv(papers: List[Dict[str, Any]], filename: str) -> None:
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['PubmedID', 'Title', 'PublicationDate', 'Non-academic Authors', 'Company Affiliations', 'Corresponding Author Email'])

            for paper in papers:
                writer.writerow([
                    paper['PubmedID'],
                    paper['Title'],
                    paper['PublicationDate'],
                    ', '.join(paper.get('NonAcademicAuthors', [])),
                    ', '.join(paper.get('CompanyAffiliations', [])),
                    paper.get('CorrespondingAuthorEmail', 'N/A')
                ])
    except Exception as e:
        print(f"Error saving CSV file: {e}")