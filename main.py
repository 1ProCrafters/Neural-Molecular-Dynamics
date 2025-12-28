import os

from scraper import PDBScraper
from structure_cleaner import StructureCleaner

from utils import clean_dir

directory = "data/"
samples = ["1L2Y", "1A3N"] # Test with Trp-Cage and a small protease

def main():
    clean_dir(directory)
    
    scraper = PDBScraper()
    
    files = scraper.fetch_ids(samples)
    print(f"Downloaded: {files}")
    
    cleaner = StructureCleaner()
    for filename in os.listdir(directory + "raw_pdb"):
        if filename.endswith(".pdb"):
            filepath = os.path.join(directory + "raw_pdb", filename)
            if os.path.isfile(filepath): cleaner.clean(filepath)

if __name__ == "__main__":
    main()