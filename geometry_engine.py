import numpy as np
from Bio.PDB import PDBParser

class GeometryEngine:
    """
    Task 1.3: Geometric Feature Extraction.
    Converts 3D coordinates into SE(3)-Equivariant local frames.
    Physics-based modeling.
    """
    def __init__(self):
        self.parser = PDBParser(QUIET=True)

    def extract_backbone_frames(self, pdb_path):
        """
        Calculates local T, N, B vectors for every Alpha-Carbon.
        T (Tangent): Direction along the backbone.
        N (Normal): Principal curvature direction.
        B (Binormal): Orthogonal torsion vector.
        """
        structure = self.parser.get_structure('protein', pdb_path)
        ca_coords = []

        # 1. Extract C-Alpha (CA) points
        for model in structure:
            for chain in model:
                for residue in chain:
                    if residue.has_id('CA'):
                        ca_coords.append(residue['CA'].get_vector().get_array())
        
        points = np.array(ca_coords)
        if len(points) < 3: return []

        # 2. Tangent (T) = r[i+1] - r[i]
        T = np.diff(points, axis=0)
        T /= np.linalg.norm(T, axis=1, keepdims=True)

        # 3. Normal (N) = T[i] - T[i-1]
        N = np.diff(T, axis=0)
        N /= np.linalg.norm(N, axis=1, keepdims=True)

        # 4. Binormal (B) = T x N
        # Align arrays: T must be sliced to match N's length
        T_aligned = T[:-1]
        B = np.cross(T_aligned, N)

        # 5. Pack into frames
        frames = []
        for i in range(len(B)):
            frames.append({
                'origin': points[i+1],
                'rotation_matrix': np.stack([T_aligned[i], N[i], B[i]], axis=1)
            })
        
        return frames

if __name__ == "__main__":
    engine = GeometryEngine()
    # Run on a sample file (assuming 1l2y_clean.pdb exists in clean folder)
    try:
        frames = engine.extract_backbone_frames("data/clean_pdb/1l2y_clean.pdb")
        print(f"Extracted {len(frames)} local coordinate frames.")
        print(f"Sample Frame Matrix:\n{frames[0]['rotation_matrix']}")
    except Exception as e:
        print(f"Error: {e}. Ensure Phase 1.1 & 1.2 are completed.")