import argparse
from pubMed_fetcher.fetcher import PubMedFetcher
from pubMed_fetcher.processor import save_as_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed")
    parser.add_argument('query', type=str, help="Search query")
    parser.add_argument('max_results', type=int, nargs='?', default=None, help="Number of Results (Optional)")
    parser.add_argument('-f', '--file', type=str, help="Output file name")
    parser.add_argument('-d', '--debug', action='store_true', help="Enable debug mode")
    # parser.add_argument('-h', '--help', action='store_true', help="Show detailed help information and exit.")
    
    args = parser.parse_args()

    try:
        # Create the fetcher instance
        fetcher = PubMedFetcher(email="your-email@example.com", debug=args.debug)
        
        # Check if max_results is provided
        if args.max_results:
            papers = fetcher.fetch_papers(args.query, args.max_results)
        else:
            papers = fetcher.fetch_papers(args.query)

        if args.file:
            save_as_csv(papers, args.file)
            print(f"Results saved to {args.file}")
        else:
            # print(papers)
            for index, paper in enumerate(papers, start=1):
                print("\n-----------------")
                print(f"Paper {index}:")
                print("-----------------")
                print(f"PubmedID: {paper['PubmedID']}")
                print(f"Title: {paper['Title']}")
                print(f"Publication Date: {paper['PublicationDate']}")
                print(f"Non-academic Authors: {', '.join(paper.get('NonAcademicAuthors', [])) or 'None'}")
                print(f"Company Affiliations: {', '.join(paper.get('CompanyAffiliations', [])) or 'None'}")
                print(f"Corresponding Author Email: {paper.get('CorrespondingAuthorEmail', 'N/A')}")
                print("-"*100+"\n")
    except Exception as e:
        print(f"Error during execution: {e}")


if __name__ == "__main__":
    main()
