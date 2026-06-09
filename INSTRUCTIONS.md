# SynCellNet — Run Instructions

All notebooks were developed on **Google Colab** (GPU runtime recommended). They can also be run locally in Jupyter with a GPU. Each section below lists the notebook, its inputs, and its outputs.

---

## Environment Setup

### Option A: Google Colab (Recommended)
1. Upload the repo to your Google Drive.
2. Open any `.ipynb` notebook in Colab.
3. Update the Drive path at the top of each notebook to match your Drive folder location (look for `drive.mount` and path variables).
4. Set runtime to **GPU**: Runtime → Change runtime type → T4 GPU.

### Option B: Local (Jupyter)
```bash
# Python 3.9+ required
pip install -r requirements.txt
jupyter notebook
```
Remove or comment out the `from google.colab import drive` and `drive.mount(...)` lines at the top of each notebook, and update all file paths to local absolute paths.

---

## Step-by-Step Workflow

### PBMC Case (B-cells and Monocytes)

#### Step 1 — Train the SynCellNet cWGAN
**Notebook**: `SynCellNet Approach/For PBMC case/cWGAN_main_PBMC.ipynb`

**Inputs**:
- `Real PBMC dataset/b_Class_dataset.csv`
- `Real PBMC dataset/mono_Class_dataset.csv`

**What it does**: Trains a conditional WGAN-GP on genomap image representations of PBMC gene expression.

**Outputs** (saved to your Drive):
- `generator_Epoch-XXXX.h5` — Generator model checkpoints
- `discriminator_Epoch-XXXX.h5` — Discriminator model checkpoints
- Training loss curves

**Pre-trained model available at**: `PBMC generator model for synthetic generation/generator.h5`

---

#### Step 2 — Generate Synthetic .npy Files
**Notebook**: `SynCellNet Approach/For PBMC case/Synthetic_npy_file_creation_for_reverse.ipynb`

**Inputs**:
- `PBMC generator model for synthetic generation/generator.h5`
- `Reverse GeneExpression Required Docs/transformation_matrix_T_b_class.npy`
- `Reverse GeneExpression Required Docs/transformation_matrix_T_mono_class.npy`
- `Reverse GeneExpression Required Docs/original_means_*.npy`
- `Reverse GeneExpression Required Docs/original_stds_*.npy`

**What it does**: Loads the trained generator, generates synthetic genomap images, then reverses the PCA + normalization transforms to produce gene expression profiles.

**Outputs**:
- `recovered_gene_expression_b_class.csv`
- `recovered_gene_expression_mono_class.csv`

Pre-generated outputs are already in `Synthetic PBMC dataset/`.

---

#### Step 3 — Train the Classifier
**Notebook**: `SynCellNet Approach/For PBMC case/Classifier for PBMC.ipynb`

**Inputs**: Real and synthetic gene expression CSVs

**What it does**: Trains a neural network classifier to evaluate how well synthetic cells preserve cell-type identity.

---

#### Step 4 — Compute SSIM / PSNR
**Notebook**: `SynCellNet Approach/For PBMC case/SSIM_PSNR_calculation.ipynb`

**Inputs**: Real and synthetic genomap `.npy` arrays

**What it does**: Computes Structural Similarity Index (SSIM) and Peak Signal-to-Noise Ratio (PSNR) between real and synthetic genomap images.

---

#### Step 5 — Plot CDF / PDF Distributions
**Script**: `Evaluation Codes & Materials/CDF & PDF/GeneExpression/4 plots_new.py`
or `Evaluation Codes & Materials/CDF & PDF/Genomap tanh/4 plots_new.py`

**Inputs**: Real and synthetic CSVs or `.npy` files in the same folder

**Run**:
```bash
python "4 plots_new.py"
```

---

### PDO Case (Patient-Derived Organoids)

The PDO workflow mirrors the PBMC workflow. Use the corresponding PDO notebooks:

| Step | Notebook |
|------|----------|
| Train cWGAN | `For PDO case/cWGAN_main_PDO.ipynb` |
| Reverse gene expression | `For PDO case/Copy_of_Cancer_Reverse_Gene_Expression_.ipynb` |
| Classifier | `For PDO case/Classifier for PDO.ipynb` |
| CDF/PDF plots | `For PDO case/Evaluation Codes & Materials/CDF & PDF/` |

**Data**:
- Real: `Real PDO/3. Stem_High_Raw_Finalized.csv` and `3. Differential_Low_Raw_Finalized.csv`
- Pre-trained generator: `PDO generator model for synthetic generation/generator_Epoch-2725.h5`
- Reverse transform files: `Reverse Calculation Related doc/*.npy`

---

### Benchmark: scGAN

**Source code**: `The Benchmark Study on scGAN & scVI/scGAN/scGAN-master/`

#### Train scGAN on PBMC
**Notebook**: `3.2_scGAN_newtrain_PBMC_B_MONO.ipynb`

```bash
# Alternatively run from command line using the original scGAN CLI:
cd "The Benchmark Study on scGAN & scVI/scGAN/scGAN-master"
pip install -r requirements.txt
python main.py parameters.json
```

**Parameters**: Edit `parameters.json` to set dataset path, number of steps, batch size.

**Pre-trained weights**: `Experiments/PBMC/PBMC_B_MONO_experiments/experiments/pbmc_cscgan_v2/weights/`

#### Train scGAN on PDO
**Notebook**: `3.1_scGAN_PDO_Stem_Diff_Batch_32.ipynb`

**Pre-trained weights**: `Experiments/PDO/PDO_Stem_Diff_experiments/experiments/PDO_cscgan_v1/weights/`

#### Generate scGAN synthetic files
**Notebook**: `scGAN_Synthetic_file_generation.ipynb`

**Outputs** (already generated):
- `Synthetic PBMC dataset/scGAN/PBMC/scgan_synthetic_b_expression.csv`
- `Synthetic PBMC dataset/scGAN/PBMC/scgan_synthetic_mono_expression.csv`
- `Synthetic PDO dataset/scGAN/PDO/scgan_synthetic_stem_high_expression.csv`
- `Synthetic PDO dataset/scGAN/PDO/scgan_synthetic_diff_low_expression.csv`

---

### Benchmark: scVI

#### Train scVI on PBMC
**Notebook**: `The Benchmark Study on scGAN & scVI/scVI/scVI_PBMC_B_Mono.ipynb`

**Pre-trained checkpoints**: `scVI/PBMC/checkpoints/`

#### Train scVI on PDO
**Notebook**: `scVI_PDO_Stem_Diff.ipynb`

**Pre-trained checkpoints**: `scVI/PDO/checkpoints/`

#### Generate scVI synthetic files
**Notebook**: `scVI_Synthetic_file_generation.ipynb`

**Outputs** (already generated):
- `Synthetic PBMC dataset/scVI/PBMC/scvi_synthetic_b_expression.csv`
- `Synthetic PDO dataset/scVI/PDO/scvi_synthetic_stem_high_expression.csv`

---

### Final Evaluation (All Methods)

**Notebook**: `Metrics_Analysis_v3.ipynb` ← **Start here if you only want to reproduce results**

**Inputs**: All synthetic CSV files from `Synthetic PBMC dataset/` and `Synthetic PDO dataset/`

**What it computes**:
- KS statistic and Wasserstein distance per gene
- PCA, t-SNE, UMAP visualizations
- Random Forest AUC (discriminability)
- Spearman correlation
- Mann–Whitney U with FDR correction

**Outputs**: Figures and metric tables comparing SynCellNet vs. scGAN vs. scVI vs. Copula.

---

## File Path Update Guide

All notebooks were originally run on Google Colab with Drive paths like:
```
/content/drive/MyDrive/Ahsan/8. 2025 cGAN Hamid with Dr. Darren Dataset/
```

When running locally or from this repo, replace these paths with the relative path from the repo root. For example:

| Original Colab Path | Repo-relative Path |
|---|---|
| `/content/drive/MyDrive/Ahsan/.../b_Class_dataset.csv` | `SynCellNet Approach/For PBMC case/Real PBMC dataset/b_Class_dataset.csv` |
| `/content/drive/MyDrive/Ahsan/.../generator.h5` | `SynCellNet Approach/For PBMC case/PBMC generator model for synthetic generation/generator.h5` |
| `/content/drive/MyDrive/Ahsan/.../generator_Epoch-2725.h5` | `SynCellNet Approach/For PDO case/PDO generator model for synthetic generation/generator_Epoch-2725.h5` |
| `/content/drive/MyDrive/Ahsan/.../transformation_matrix_T_b_class.npy` | `SynCellNet Approach/For PBMC case/Reverse GeneExpression Required Docs/transformation_matrix_T_b_class.npy` |

---

## Hardware Requirements

| Task | Minimum | Recommended |
|------|---------|-------------|
| Inference / evaluation only | CPU | CPU |
| Training cWGAN | GPU (8 GB VRAM) | GPU (16 GB VRAM) |
| Training scGAN | GPU (8 GB VRAM) | GPU (16 GB VRAM) |
| Training scVI | GPU (8 GB VRAM) | GPU (16 GB VRAM) |

Google Colab free tier (T4 GPU) is sufficient for training and inference.
