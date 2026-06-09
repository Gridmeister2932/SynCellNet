import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


# ==== File paths (edit if needed) ====
file_real_High = 'mono_Class_genomap_tanh.csv'
file_synthetic_High = 'synthetic_mono.csv'
file_real_Low = 'b_Class_genomap_tanh.csv'
file_synthetic_Low = 'synthetic_b.csv'

# ==== Load CSVs and flatten numeric data ====
def load_flatten_numeric(csv_path):
    df = pd.read_csv(csv_path)
    # keep only numeric columns; flatten to 1D; drop NaNs
    arr = df.select_dtypes(include=[np.number]).to_numpy().ravel()
    return arr[np.isfinite(arr)]

data_real_High       = load_flatten_numeric(file_real_High)
data_synthetic_High  = load_flatten_numeric(file_synthetic_High)
data_real_Low        = load_flatten_numeric(file_real_Low)
data_synthetic_Low   = load_flatten_numeric(file_synthetic_Low)

# ==== Plot settings ====
plt.rcParams.update({'font.size': 18})

# Global range & bins for consistency
data_min = np.min([data_real_High.min(), data_synthetic_High.min(),
                   data_real_Low.min(),  data_synthetic_Low.min()])
data_max = np.max([data_real_High.max(), data_synthetic_High.max(),
                   data_real_Low.max(),  data_synthetic_Low.max()])
bins = 30
hist_range = (data_min, data_max)

# ==== Combined PDF (all four) ====
plt.figure(figsize=(8, 6))
# step-style histograms avoid heavy overlap; density=True gives PDF
plt.hist(data_real_High,      bins=bins, range=hist_range, density=True,
         histtype='step', linewidth=2, label='Real Mono')
plt.hist(data_synthetic_High, bins=bins, range=hist_range, density=True,
         histtype='step', linewidth=2, label='Synthetic Mono')
plt.hist(data_real_Low,       bins=bins, range=hist_range, density=True,
         histtype='step', linewidth=2, label='Real B')
plt.hist(data_synthetic_Low,  bins=bins, range=hist_range, density=True,
         histtype='step', linewidth=2, label='Synthetic B')

plt.yscale('log')
plt.ylim(bottom=1e-6)  # avoid zero on log scale
plt.xticks(np.linspace(data_min, data_max, 5))
plt.yticks([1e-6, 1e-4, 1e-2, 1e0])
plt.xlabel('Normalized Genomap Values Scaled to [-1,1]')
plt.ylabel('Density')
plt.grid(axis='y')

# --- FIX: custom line legend handles instead of box patches ---
legend_lines = [
    Line2D([0], [0], color='C0', linewidth=2, label='Real Mono'),
    Line2D([0], [0], color='C1', linewidth=2, label='Synthetic Mono'),
    Line2D([0], [0], color='C2', linewidth=2, label='Real B'),
    Line2D([0], [0], color='C3', linewidth=2, label='Synthetic B'),
]
plt.legend(handles=legend_lines, frameon=False)

plt.tight_layout()
plt.savefig('combined_pdf.png', dpi=300)
plt.show()
# ==== Combined CDF (all four) ====
def ecdf(x):
    x_sorted = np.sort(x)
    y = np.arange(1, len(x_sorted) + 1) / len(x_sorted)
    return x_sorted, y

x_rh, y_rh = ecdf(data_real_High)
x_sh, y_sh = ecdf(data_synthetic_High)
x_rl, y_rl = ecdf(data_real_Low)
x_sl, y_sl = ecdf(data_synthetic_Low)

'''
plt.figure(figsize=(8, 6))
plt.step(x_rh, y_rh, where='mid', linewidth=3, label='Real Stem-like', linestyle='dotted')
plt.step(x_sh, y_sh, where='mid', linewidth=3, label='Synthetic Stem-like', linestyle='--')
plt.step(x_rl, y_rl, where='mid', linewidth=3, label='Real Differentiating', linestyle='-.')
plt.step(x_sl, y_sl, where='mid', linewidth=3, label='Synthetic Differentiating', linestyle='-')
'''

plt.step(x_rh, y_rh, where='mid', linewidth=3, label='Real Mono',
         linestyle='-', color='C0')
plt.step(x_sh, y_sh, where='mid', linewidth=3, label='Synthetic Mono',
         linestyle='--', color='C1')
plt.step(x_rl, y_rl, where='mid', linewidth=3, label='Real B',
         linestyle='-.', color='C2')
plt.step(x_sl, y_sl, where='mid', linewidth=3, label='Synthetic B',
         linestyle=':', color='C3')

plt.xticks(np.linspace(data_min, data_max, 5))
plt.yticks(np.linspace(0, 1, 5))
plt.xlabel('Normalized Genomap Values Scaled to [-1,1]')
plt.ylabel('Cumulative Probability')
plt.legend()
plt.grid(axis='y')
plt.tight_layout()
#plt.savefig('combined_cdf.png', dpi=300)
plt.show()
