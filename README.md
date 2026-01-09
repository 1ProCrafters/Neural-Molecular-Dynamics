# **Neural Molecular Dynamics (NMD-Fold)**

## **🌟 Project Vision**

**Neural Molecular Dynamics (NMD)** is an interdisciplinary framework designed to bridge the gap between static protein structure prediction and real-time physical simulation. While current state-of-the-art models (like AlphaFold 2/3) excel at predicting the final "native state" of a protein, they often ignore the dynamic pathway—the folding trajectory—that a protein follows.

The goal of this project is to build a **Differentiable Physics-Informed Model** that simulates the continuous folding process, providing biochemists with a "movie" of protein formation rather than just a single snapshot.

## **🛠️ Project Roadmap (Core Steps)**

1. **Geometry Engine:** Converting 3D coordinates into SE(3)-equivariant local frames.  
2. **Neural ODE Trunk:** Modeling folding as a continuous-time vector field.  
3. **Differentiable Physics:** Integrating energy potentials (Van der Waals, Electrostatics) into the neural loss function.  
4. **Training Curriculum:** Learning from simple peptides to complex globular domains.  
5. **Sim-Sandbox:** Exporting physics-validated trajectories for researchers.

## **🧬 Phase 1: Data & Geometry Engine**

**Status: Complete**

Phase 1 establishes the mathematical and data-processing foundation. To achieve "better-than-SOTA" results, we move away from global Cartesian coordinates and adopt a **Residue-Local Coordinate System**.

### **📂 File Architecture**

- `pdb_scraper.py`: High-throughput acquisition of structural data from the RCSB PDB.
- `structure_cleaner.py`: Biological sanitization: removing water, ions, and non-standard ligands.
- `geometry_engine.py`: Geometric encoding of the backbone into Frenet-Serret frames.

### **📐 Mathematical Foundation: Frenet-Serret Frames**

To ensure **SE(3)-Equivariance** (invariance to rotation and translation), the model must view the protein from the "perspective" of the amino acid chain itself. We calculate an orthonormal basis $(T, N, B)$ for every $C\alpha$ atom.

#### **1\. Tangent Vector ($\vec{T}$)**

Represents the local direction of the backbone.

$\vec{T}_i = \frac{\vec{r}_{i+1} - \vec{r}_i}{||\vec{r}_{i+1} - \vec{r}_i||}$

Where $\vec{r}_i$ is the position of the $i$-th Alpha-Carbon.

#### **2. Normal Vector ($\vec{N}$)**

Represents the principal curvature (the "bend"). Derived from the change in the tangent:

$\Delta \vec{T}_i = \vec{T}_i - \vec{T}_{i-1}$

$\vec{N}_i = \frac{\Delta \vec{T}_i}{||\Delta \vec{T}_i||}$

#### **3. Binormal Vector ($\vec{B}$)**

Completes the right-handed basis, capturing the "twist" or torsion:

$\vec{B}_i = \vec{T}_i \times \vec{N}_i$

#### **4. The Rotation Matrix ($R$)**

The resulting frame is encoded as a rotation matrix $R \in SO(3)$:

$R_i =
\begin{pmatrix}
    T_x & N_x & B_x \\
    T_y & N_y & B_y \\
    T_z & N_z & B_z \\
\end{pmatrix}
$

## **🚀 Execution Workflow**

### **1. Installation**

Install the dependencies using this command:

`pip install -r requirements.txt`

### **2. Run Main Script**

Run the main script using this command:

`python main.py`

## **🧪 Future Work: Phase 2 (Modeling)**

The next phase will involve feeding these local frames into an **Equivariant Graph Neural Network** (EGNN) to begin training the prediction engine.
