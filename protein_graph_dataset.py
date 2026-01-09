import torch
from torch_geometric.data import Data, Dataset
import numpy as np
from geometry_engine import GeometryEngine

class ProteinGraphDataset(Dataset):
    """
    Task 2.1: Data Loader.
    Converts processed PDBs and Frenet frames into Graph objects for PyTorch.
    """
    def __init__(self, pdb_paths):
        super().__init__()
        self.pdb_paths = pdb_paths
        self.geo_engine = GeometryEngine()

    def len(self):
        return len(self.pdb_paths)

    def get(self, idx):
        path = self.pdb_paths[idx]
        frames = self.geo_engine.extract_backbone_frames(path)
        
        # Node Features (x): For now, use the rotation matrix flattened (9 dims) 
        # + placeholder for amino acid identity (ESM-2 embeddings would go here)
        node_features = []
        pos = []
        
        for f in frames:
            # Flatten 3x3 rotation matrix to 9D vector
            rot_flat = f['rotation_matrix'].flatten()
            node_features.append(rot_flat)
            pos.append(f['origin'])
            
        x = torch.tensor(np.array(node_features), dtype=torch.float)
        pos = torch.tensor(np.array(pos), dtype=torch.float)
        
        # Edges: KNN Graph (Connect each residue to its 10 nearest neighbors)
        # In a real model, we'd also include covalent peptide bond edges
        edge_index = self._build_knn_graph(pos, k=10)
        
        return Data(x=x, pos=pos, edge_index=edge_index)

    def _build_knn_graph(self, pos, k=10):
        # Simple distance-based edge construction
        dist = torch.cdist(pos, pos)
        _, indices = dist.topk(k + 1, largest=False)
        
        # Create edge list (excluding self-loops)
        edge_index = []
        for i in range(indices.size(0)):
            for j in indices[i][1:]:
                edge_index.append([i, j])
                
        return torch.tensor(edge_index, dtype=torch.long).t().contiguous()

if __name__ == "__main__":
    # Run on a sample file (assuming 1l2y_clean.pdb exists in clean folder)
    paths = ["data/clean_pdb/1l2y_clean.pdb"]
    dataset = ProteinGraphDataset(paths)
    sample_graph = dataset[0]
    print(f"Graph created with {sample_graph.num_nodes} nodes and {sample_graph.num_edges} edges.")