import os

from scraper import PDBScraper
from structure_cleaner import StructureCleaner
from geometry_engine import GeometryEngine

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
    
    engine = GeometryEngine()
    for filename in os.listdir(directory + "clean_pdb"):
        if filename.endswith("_clean.pdb"):
            filepath = os.path.join(directory + "clean_pdb", filename)
            if os.path.isfile(filepath):
                frames = engine.extract_backbone_frames(filepath)
                print(f"Extracted {len(frames)} local coordinate frames from {filename}.")
                print(f"Sample Frame Matrix:\n{frames[0]['rotation_matrix']}")

if __name__ == "__main__":
    main()