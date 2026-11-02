# AI Agent Dataset Evaluation Report

## Evaluation Matrix

| Criterion | Score | Evidence Quoted | Notes / Missing Elements |
| :--- | :---: | :--- | :--- |
| **A1 Provenance** | 2 | `data/ai_ready/description.yml` (lines 3-5) | PNSN/UW Seismology Lab attribution, CC-BY-4.0 license, and catalog citation present. |
| **A2 Homogenization** | 2 | `data/ai_ready/description.yml` (lines 7-10) | Uniform 100 Hz sampling rate, 15s duration (1500 samples), 3-component counts, UTC time base. |
| **A3 Quality and gaps** | 2 | `data/clean/DATASET_SUMMARY.md` | Dead channels, NaNs, and sentinel values rejected during cleaning phase. |
| **A4 Structure and metadata** | 2 | `data/ai_ready/description.yml` (lines 12-25) | Machine-readable YAML manifest detailing array shapes `[3, 1500]` and variable schema. |
| **B1 Diversity** | 2 | `data/ai_ready/description.yml` (lines 31-34) | Covers 281 independent stations, 8,055 unique events, and 6 regional networks. |
| **B2 Distribution** | 2 | `notebooks/EDA.ipynb` | Magnitude range 0.0–4.8 ($M \ge 3.0$ rare tail isolated at 329 records / 1.77%). |
| **B3 Noise** | 2 | `notebooks/Prepare_AI_Ready_Data.ipynb` | Windowed SNR calculations on pre-P noise vs. signal windows. |
| **B4 Augmentation** | 2 | `README.md` | Defined physical validity constraints (phase shifting vs. cross-channel shuffling). |
| **B5 Labels** | 2 | `data/ai_ready/description.yml` (line 36) | Analyst-reviewed PNSN catalog picks and magnitude determinations. |
| **B6 Dimensionality** | 2 | `notebooks/Dimensionality_Reduction.ipynb` | $N=18640, D=4500$. PCA shows 2 components capture >97% of overall variance. |
| **B7 Partitioning** | 2 | `data/ai_ready/partitions.parquet` | Geographic station-holdout splits (85% train / 10% test / 5% val) by independent unit. |

## Lowest Scores / Author Recommendations
1. **B3 Noise:** Provide explicit sensor transfer function response curves alongside windowed SNR.
2. **B5 Labels:** Include formal analyst pick variance/uncertainty estimates in seconds.
3. **A2 Homogenization:** Add explicit metadata flags tracking historical instrument updates across station operational lifespans.
