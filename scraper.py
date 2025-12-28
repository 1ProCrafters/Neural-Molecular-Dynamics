import os
from Bio.PDB import PDBList

class PDBScraper:
    """
    Task 1.1: High-throughput PDB acquisition.
    Handles downloading and organizing raw structural files.
    """
    def __init__(self, storage_path="data/raw_pdb"):
        self.storage_path = storage_path
        self.pdbl = PDBList()
        os.makedirs(self.storage_path, exist_ok=True)

    def fetch_ids(self, pdb_ids):
        """
        Downloads a list of PDB IDs.
        Args:
            pdb_ids (list): 4-character codes (e.g., ['1L2Y', '7UPJ'])
        """
        downloaded_files = []
        for pid in pdb_ids:
            print(f"--- Fetching {pid} ---")
            # retrieve_pdb_file downloads in .ent or .pdb format
            file_path = self.pdbl.retrieve_pdb_file(
                pid, 
                pdir=self.storage_path, 
                file_format='pdb',
                overwrite=False
            )
            
            # Standardize filename
            standard_name = os.path.join(self.storage_path, f"{pid.lower()}.pdb")
            if os.path.exists(file_path):
                os.rename(file_path, standard_name)
                downloaded_files.append(standard_name)
                
        return downloaded_files