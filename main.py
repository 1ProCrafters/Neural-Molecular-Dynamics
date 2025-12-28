from scraper import PDBScraper

def main():
    scraper = PDBScraper()
    
    # Test with Trp-Cage and a small protease
    samples = ["1L2Y", "1A3N"]
    files = scraper.fetch_ids(samples)
    print(f"Downloaded: {files}")

if __name__ == "__main__":
    main()