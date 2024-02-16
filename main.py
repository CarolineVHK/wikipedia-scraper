from .scr.scraper import WikipediaScraper

def main():
    scraper = WikipediaScraper()
    if __name__ == "__main__":
        wiki_scraper = WikipediaScraper()  # Create an instance of the WikipediaScraper class
        wiki_scraper.write_to_file()  # Call the write_to_file method to save leaders data to JSON file
        wiki_scraper.read_file()  # Call the read_file method to read and print leaders data from JSON file

main()