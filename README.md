# SynCellNet: Generative AI Framework for Single-Cell RNA Sequencing Data Generation and Validation

SynCellNet is a conditional Wasserstein GAN (cWGAN) framework for generating high-fidelity synthetic single-cell RNA sequencing (scRNA-seq) data. It operates on **genomap** image representations of gene expression and includes a full reverse-transformation pipeline to recover biologically interpretable gene expression profiles.

This repository contains all code, datasets, and trained models used in the paper.

---

## Repository Structure

```
SynCellNet/
│
├── README.md                          ← This file
├── INSTRUCTIONS.md                    ← Step-by-step run guide
├── requirements.txt                   ← Python dependencies
├── .gitignore
│
├── Metrics_Analysis_v3.ipynb          ← Final evaluation: all methods compared
│
├── SynCellNet Approach/               ← Core SynCellNet method
│   ├── For PBMC case/                 ← Peripheral Blood Mononuclear Cells
│   │   ├── cWGAN_main_PBMC.ipynb              ← Train SynCellNet on PBMC
│   │   ├── Classifier for PBMC.ipynb          ← Train discriminative classifier
│   │   ├── Synthetic_npy_file_creation_for_reverse.ipynb
│   │   ├── SSIM_PSNR_calculation.ipynb        ← Image quality metrics
│   │   ├── Real PBMC dataset/                 ← Real scRNA-seq data (B-cell, Monocyte)
│   │   ├── Synthetic PBMC dataset/            ← All synthetic outputs
│   │   │   ├── syncellnet_b_expression.csv
│   │   │   ├── syncellnet_mono_expression.csv
│   │   │   ├── scGAN/PBMC/
│   │   │   └── scVI/PBMC/
│   │   ├── PBMC generator model for synthetic generation/
│   │   │   └── generator.h5                   ← Pretrained PBMC generator (see note below)
│   │   └── Reverse GeneExpression Required Docs/
│   │       ├── transformation_matrix_T_*.npy
│   │       ├── original_means_*.npy
│   │       └── original_stds_*.npy
│   │
│   └── For PDO case/                  ← Patient-Derived Organoids (cancer)
│       ├── cWGAN_main_PDO.ipynb
│       ├── Classifier for PDO.ipynb
│       ├── Real PDO/                          ← Real PDO data (Stem/High, Diff/Low)
│       ├── Synthetic PDO dataset/             ← All synthetic outputs
│       │   ├── syncellnet_high_expression.csv
│       │   ├── syncellnet_low_expression.csv
│       │   ├── scGAN/PDO/
│       │   ├── scVI/PDO/
│       │   └── Copula/
│       ├── PDO generator model for synthetic generation/
│       │   └── generator_Epoch-2725.h5        ← Pretrained PDO generator (see note below)
│       └── Reverse Calculation Related doc/
│
└── The Benchmark Study on scGAN & scVI/
    ├── scGAN/
    │   ├── scGAN-master/                  ← Original scGAN source code
    │   ├── Experiments/PBMC/              ← scGAN PBMC training runs
    │   ├── Experiments/PDO/               ← scGAN PDO training runs
    │   └── scGAN_Synthetic_file_generation.ipynb
    └── scVI/
        ├── scVI_PBMC_B_Mono.ipynb
        ├── scVI_PDO_Stem_Diff.ipynb
        ├── PBMC/                          ← scVI PBMC results
        └── PDO/                           ← scVI PDO results
```

---

## Datasets

### PBMC (Peripheral Blood Mononuclear Cells)
- **Cell types**: B-cells and Monocytes
- **Real data**: `SynCellNet Approach/For PBMC case/Real PBMC dataset/`
  - `b_Class_dataset.csv` — B-cell gene expression matrix
  - `mono_Class_dataset.csv` — Monocyte gene expression matrix
- **Format**: CSV, rows = cells, columns = genes

### PDO (Patient-Derived Organoids)
- **Cell types**: Stem-like/High and Differentiated/Low
- **Real data**: `SynCellNet Approach/For PDO case/Real PDO/`
  - `3. Stem_High_Raw_Finalized.csv`
  - `3. Differential_Low_Raw_Finalized.csv`
- **Format**: CSV, rows = cells, columns = genes

---

## Pretrained Models

> **Note:** Large model files (.h5, .h5ad, checkpoints) are excluded from this repo due to GitHub's file size limits. To have access please contact the 1st author at aqueeb.eee@gmail.com

| Model | Description |
|-------|-------------|
| SynCellNet PBMC Generator | cWGAN generator trained on PBMC genomaps |
| SynCellNet PDO Generator | cWGAN generator trained on PDO genomaps (epoch 2725) |
| scGAN PBMC | Trained scGAN weights for PBMC |
| scGAN PDO | Trained scGAN weights for PDO |
| scVI PBMC | Trained scVI weights for PBMC |
| scVI PDO | Trained scVI weights for PDO |

---

## Quick Start

See **[INSTRUCTIONS.md](INSTRUCTIONS.md)** for the full step-by-step guide.

```bash
# 1. Clone the repo
git clone https://github.com/Gridmeister2932/SynCellNet.git
cd SynCellNet

# 2. Install dependencies
pip install -r requirements.txt

# 3. Open any notebook in Jupyter or upload to Google Colab
jupyter notebook "SynCellNet Approach/For PBMC case/cWGAN_main_PBMC.ipynb"
```

---

## Method Overview

SynCellNet works in three stages:

1. **Genomap encoding** — Gene expression vectors are encoded as 2D genomap images using a position-optimized spatial mapping that preserves gene–gene correlations.
2. **cWGAN training** — A conditional Wasserstein GAN with gradient penalty (WGAN-GP) learns the distribution of genomap images conditioned on cell type label.
3. **Reverse transformation** — Synthetic genomap images are decoded back to gene expression space using stored PCA transformation matrices, means, and standard deviations.

---

## Evaluation Metrics
For evlauting SynCellNet generated genomap we had classifier (confusion metrix, precsion recall f1, accuracy,), 
All metrics are computed in Metrics_Analysis_v3.ipynb across both PBMC and PDO datasets, comparing SynCellNet, SynCellNet+Copula, scGAN, and scVI against real data.
Group 1 — Gene-level Distribution

Mean expression correlation (Pearson)
Variance correlation (Pearson)
Coefficient of variation (CV) correlation
Detection rate correlation
Fraction-zero gene correlation
Average KS statistic across all genes

Group 2 — Cell-level Distribution

Library size KS statistic
Fraction-zero per cell KS statistic
Cell detection rate KS statistic
Cell distance KS — KS stat between mean kNN distance distributions in PCA space
kNN occurrence KS — KS stat between kNN occurrence-count distributions
Local Density Factor (LDF) KS — based on Lütge et al. (CellMixS, 2021)

Group 3 — Bivariate Relationships

Mean–variance correlation difference
Mean–fraction-zero correlation difference
Library size–fraction-zero correlation difference

Group 4 — Correlation Structure

Gene–gene correlation (Pearson on top 300 HVG correlation matrices)
Marker gene correlation (top 30 DE genes by fold change)
Cell–cell correlation

Group 5 — Distributional Similarity

Average KS statistic
Average Wasserstein distance
Average KDE overlap (top 200 HVGs)

Group 6 — Global Structural

Maximum Mean Discrepancy (MMD) with RBF kernel in PCA space
Random Forest AUC — 5-fold cross-validated classifier distinguishing real vs. synthetic
PVE difference — |% variance explained by class label in real vs. synthetic|
Silhouette width difference — |silhouette score in real vs. synthetic| (PCA space)

Group 7 — Biological Signal Preservation

Number of differentially expressed (DE) genes (Mann–Whitney U, FDR-BH corrected)
DE gene overlap, precision, recall, and F1 score
Log fold change (LFC) correlation: Pearson on all genes, Pearson and Spearman restricted to real DE genes

Group 8 — Visualization

PCA, t-SNE, and UMAP embeddings of real and synthetic cells across all methods

---

## Benchmark Methods
SynCellNet is evaluated against two state-of-the-art single-cell generative models and one statistical baseline:

| Method | Type | Reference |
|--------|------|-----------|
| **scGAN** | Conditional GAN | Marouf et al., 2020 |
| **scVI** | Variational Autoencoder | Lopez et al., 2018 |
| **Gaussian Copula** | Statistical baseline | — |

### scGAN
scGAN is a conditional GAN designed for scRNA-seq data generation, conditioned on cell type labels.
- **Training notebooks**: `3.2_scGAN_newtrain_PBMC_B_MONO.ipynb` (PBMC) · `3.1_scGAN_PDO_Stem_Diff_Batch_32.ipynb` (PDO)
- **Synthetic generation**: `scGAN_Synthetic_file_generation.ipynb`
- **Synthetic outputs**: `Synthetic PBMC dataset/scGAN/` · `Synthetic PDO dataset/scGAN/`

### scVI
scVI is a VAE-based deep generative model that models the negative binomial distribution of scRNA-seq counts.
- **Training notebooks**: `scVI_PBMC_B_Mono.ipynb` (PBMC) · `scVI_PDO_Stem_Diff.ipynb` (PDO)
- **Synthetic generation**: `scVI_Synthetic_file_generation.ipynb`
- **Synthetic outputs**: `Synthetic PBMC dataset/scVI/` · `Synthetic PDO dataset/scVI/`

### Gaussian Copula
A statistical baseline using Gaussian copula to model gene–gene dependencies and generate synthetic expression profiles.
- **Synthetic outputs**: `Synthetic PBMC dataset/` · `Synthetic PDO dataset/Copula/`
---

## Citation

> [Paper citation to be added upon publication]

---

## License

This project is for research purposes. Please cite the paper if you use this code or data.
