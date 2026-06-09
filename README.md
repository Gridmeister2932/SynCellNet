# SynCellNet: Conditional GAN-Based Synthetic Single-Cell RNA-seq Generation

SynCellNet is a conditional Wasserstein GAN (cWGAN) framework for generating high-fidelity synthetic single-cell RNA sequencing (scRNA-seq) data. It operates on **genomap** image representations of gene expression and includes a full reverse-transformation pipeline to recover biologically interpretable gene expression profiles.

This repository contains all code, datasets, and trained models used in the paper.

---

## Repository Structure

```
SynCellNet Codes/Github Repository/
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
│   │   ├── Synthetic_npy_file_creation_for_reverse.ipynb  ← Generate synthetic .npy files
│   │   ├── SSIM_PSNR_calculation.ipynb        ← Image quality metrics
│   │   ├── Real PBMC dataset/                 ← Real scRNA-seq data (B-cell, Monocyte)
│   │   ├── Synthetic PBMC dataset/            ← All synthetic outputs
│   │   │   ├── syncellnet_b_expression.csv
│   │   │   ├── syncellnet_mono_expression.csv
│   │   │   ├── scGAN/PBMC/
│   │   │   ├── scVI/PBMC/
│   │   │   └── ...
│   │   ├── PBMC generator model for synthetic generation/
│   │   │   └── generator.h5                   ← Pretrained PBMC generator
│   │   ├── Reverse GeneExpression Required Docs/
│   │   │   ├── transformation_matrix_T_*.npy  ← PCA transform matrices
│   │   │   ├── original_means_*.npy
│   │   │   └── original_stds_*.npy
│   │   └── Evaluation Codes & Materials/
│   │       └── CDF & PDF/                     ← Distribution comparison plots
│   │
│   └── For PDO case/                  ← Patient-Derived Organoids (cancer)
│       ├── cWGAN_main_PDO.ipynb               ← Train SynCellNet on PDO
│       ├── Classifier for PDO.ipynb
│       ├── Copy_of_Cancer_Reverse_Gene_Expression_.ipynb
│       ├── Real PDO/                          ← Real PDO data (Stem/High, Diff/Low)
│       ├── Synthetic PDO dataset/             ← All synthetic outputs
│       │   ├── syncellnet_high_expression.csv
│       │   ├── syncellnet_low_expression.csv
│       │   ├── scGAN/PDO/
│       │   ├── scVI/PDO/
│       │   └── Copula/
│       ├── PDO generator model for synthetic generation/
│       │   └── generator_Epoch-2725.h5        ← Pretrained PDO generator
│       ├── Reverse Calculation Related doc/
│       │   ├── transformation_matrix_T_*.npy
│       │   ├── original_means_*.npy
│       │   └── original_stds_*.npy
│       └── Effect of Copula Study/            ← Ablation: Gaussian copula effect
│
└── The Benchmark Study on scGAN & scVI/  ← Competing methods
    ├── scGAN/
    │   ├── scGAN-master/                  ← Original scGAN source code
    │   ├── Experiments/
    │   │   ├── PBMC/                      ← scGAN PBMC training runs + weights
    │   │   └── PDO/                       ← scGAN PDO training runs + weights
    │   ├── 1.1_Original_scGAN.ipynb
    │   ├── 3.1_scGAN_PDO_Stem_Diff_Batch_32.ipynb
    │   ├── 3.2_scGAN_newtrain_PBMC_B_MONO.ipynb
    │   └── scGAN_Synthetic_file_generation.ipynb
    └── scVI/
        ├── scVI_PBMC_B_Mono.ipynb
        ├── scVI_PDO_Stem_Diff.ipynb
        ├── scVI_Synthetic_file_generation.ipynb
        ├── PBMC/                          ← scVI PBMC checkpoints + results
        └── PDO/                           ← scVI PDO checkpoints + results
```

---

## Datasets

### PBMC (Peripheral Blood Mononuclear Cells)
- **Cell types**: B-cells and Monocytes (2 classes)
- **Real data location**: `SynCellNet Approach/For PBMC case/Real PBMC dataset/`
  - `b_Class_dataset.csv` — B-cell gene expression matrix
  - `mono_Class_dataset.csv` — Monocyte gene expression matrix
- **Format**: CSV, rows = cells, columns = genes

### PDO (Patient-Derived Organoids)
- **Cell types**: Stem-like / High (class 1) and Differentiated / Low (class 0)
- **Real data location**: `SynCellNet Approach/For PDO case/Real PDO/`
  - `3. Stem_High_Raw_Finalized.csv`
  - `3. Differential_Low_Raw_Finalized.csv`
- **Format**: CSV, rows = cells, columns = genes

### Synthetic Outputs (all methods)
Pre-generated synthetic datasets for both PBMC and PDO are included under each case's `Synthetic * dataset/` folder, organized by method (SynCellNet, scGAN, scVI, Copula).

---

## Pretrained Models

| Model | Location | Description |
|-------|----------|-------------|
| SynCellNet PBMC Generator | `For PBMC case/PBMC generator model.../generator.h5` | cWGAN generator trained on PBMC genomaps |
| SynCellNet PDO Generator | `For PDO case/PDO generator model.../generator_Epoch-2725.h5` | cWGAN generator trained on PDO genomaps |
| scGAN PBMC | `The Benchmark Study.../scGAN/Experiments/PBMC/` | Trained scGAN weights for PBMC |
| scGAN PDO | `The Benchmark Study.../scGAN/Experiments/PDO/` | Trained scGAN weights for PDO |
| scVI PBMC | `The Benchmark Study.../scVI/PBMC/checkpoints/` | Trained scVI weights for PBMC |
| scVI PDO | `The Benchmark Study.../scVI/PDO/checkpoints/` | Trained scVI weights for PDO |

---

## Quick Start

See **[INSTRUCTIONS.md](INSTRUCTIONS.md)** for the full step-by-step guide.

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/SynCellNet.git
cd SynCellNet

# 2. Install dependencies
pip install -r requirements.txt

# 3. Open any notebook in Jupyter or upload to Google Colab
jupyter notebook "SynCellNet Approach/For PBMC case/cWGAN_main_PBMC.ipynb"
```

---

## Method Overview

SynCellNet works in three stages:

1. **Genomap encoding** — Gene expression vectors are encoded as 2D genomap images using a position-optimized spatial mapping, preserving gene–gene correlations.
2. **cWGAN training** — A conditional Wasserstein GAN with gradient penalty (WGAN-GP) learns the distribution of genomap images conditioned on cell type label.
3. **Reverse transformation** — Synthetic genomap images are decoded back to gene expression space using stored PCA transformation matrices, means, and standard deviations.

---

## Evaluation Metrics

The following metrics are used to compare SynCellNet against scGAN and scVI (`Metrics_Analysis_v3.ipynb`):

- KS statistic & Wasserstein distance (per-gene distribution similarity)
- SSIM / PSNR (image-level fidelity)
- PCA & t-SNE / UMAP visualizations
- Random Forest classifier AUC (cell type preservation)
- Spearman correlation of gene expression
- Mann–Whitney U test with FDR correction

---

## Citation

> [Paper citation to be added upon publication]

---

## License

This project is for research purposes. Please cite the paper if you use this code or data.
