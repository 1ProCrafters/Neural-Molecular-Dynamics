import os
from Bio.PDB import PDBParser, PDBIO, Select
from Bio.PDB.Polypeptide import is_aa

class ProteinOnlySelect(Select):
    """
    Filter class for PDBIO.
    - Removes HOH (Water)
    - Removes ligands/ions (HETATM)
    - Keeps only standard amino acid residues
    """
    def accept_residue(self, residue):
        # ' ' indicates a standard residue. 'W' is water, 'H_' is hetero.
        is_standard = residue.id[0] == ' '
        return is_aa(residue) and is_standard

class StructureCleaner:
    """
    Task 1.2: Sanitization Engine.
    Prepares the protein for Graph Neural Network input.
    """
    def __init__(self, output_dir="data/clean_pdb"):
        self.output_dir = output_dir
        self.parser = PDBParser(QUIET=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def clean(self, input_path):
        pdb_id = os.path.basename(input_path).split('.')[0]
        structure = self.parser.get_structure(pdb_id, input_path)
        
        io = PDBIO()
        io.set_structure(structure)
        
        clean_name = f"{pdb_id}_clean.pdb"
        save_path = os.path.join(self.output_dir, clean_name)
        
        io.save(save_path, ProteinOnlySelect())
        print(f"Cleaned: {save_path}")
        return save_path

if __name__ == "__main__":
    cleaner = StructureCleaner()
    # Run on a sample file (assuming 1l2y.pdb exists in raw folder)
    try:
        cleaner.clean("data/raw_pdb/1l2y.pdb")
    except FileNotFoundError:
        print("Run Task 1.1 first to download data.")