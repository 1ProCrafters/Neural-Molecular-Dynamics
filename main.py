import os

from pdb_scraper import PDBScraper
from structure_cleaner import StructureCleaner
from geometry_engine import GeometryEngine

from protein_graph_dataset import ProteinGraphDataset

from utils import clean_dir

directory = "data/"
samples = ["1L2Y", "1A3N"] # Test with Trp-Cage and a small protease

def main():
    clean_dir(directory)
    
    # Scrape the data into PDB files.
    scraper = PDBScraper()
    
    files = scraper.fetch_ids(samples)
    print(f"Downloaded: {files}")
    
    # Clean the structures for modeling.
    cleaner = StructureCleaner()
    for filename in os.listdir(directory + "raw_pdb"):
        if filename.endswith(".pdb"):
            filepath = os.path.join(directory + "raw_pdb", filename)
            if os.path.isfile(filepath): cleaner.clean(filepath)
    
    # Extract geometric features using GeometryEngine.
    engine = GeometryEngine()
    for filename in os.listdir(directory + "clean_pdb"):
        if filename.endswith("_clean.pdb"):
            filepath = os.path.join(directory + "clean_pdb", filename)
            if os.path.isfile(filepath):
                frames = engine.extract_backbone_frames(filepath)
                print(f"Extracted {len(frames)} local coordinate frames from {filename}.")
                print(f"Sample Frame Matrix:\n{frames[0]['rotation_matrix']}")
    
    # Create Protein Graph Dataset.
    paths = []
    for filename in os.listdir(directory + "clean_pdb"):
        if filename.endswith("_clean.pdb"):
            filepath = os.path.join(directory + "clean_pdb", filename)
            if os.path.isfile(filepath):
                paths.append(filepath)
    
    dataset = ProteinGraphDataset(paths)
    print(f"Created dataset with {len(dataset)} graphs.")
    print(f"Sample Graph created with {dataset[0].num_nodes} nodes and {dataset[0].num_edges} edges.")

if __name__ == "__main__":
    main()