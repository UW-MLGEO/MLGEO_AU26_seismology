# MLGEO_AU26_seismology
This repository provides an end-to-end pipeline to acquire, clean, document, and partition a 3-component ground motion seismic dataset from the Pacific Northwest Seismic Network (PNSN). The dataset is formatted to satisfy rigorous benchmark specifications for machine learning workflows in geophysics and earth observation.

---

## Data Sources & Citations

- **Source Catalog:** Pacific Northwest Seismic Network (PNSN) / University of Washington Seismology Lab.
- **Data Access:** PNSN / IRIS Web Services & PNWML HDF5 event catalog.
- **License:** Creative Commons Attribution 4.0 International (CC-BY-4.0).
- **Citation:** Code and documentation preserved in `data/ai_ready/description.yml`.
- **Retrieval Date** 10/20/2026 from SeisBench

---

## Installing the Repository

This code will install and prepare the code to be run. 

Clone and prepare the repository:

```bash
git clone [https://github.com/UW-MLGEO/MLGEO_AU26_seismology.git](https://github.com/UW-MLGEO/MLGEO_AU26_seismology.git)
cd MLGEO_AU26_seismology
git pull
```

## Setting up the Environment

This project uses Pixi for environment and dependency management. 

```
# Install environment dependencies via Pixi and register Jupyter kernel
pixi install
pixi run python -m ipykernel install --user --name MLGEO_AU26_seismology --display-name "Python (Pixi MLGEO)"
```
Legacy setup via Conda can also be initialized using:

```
conda env create --file environment.yml
```

## Running the Code

To run the pipeline notebooks:
1. Open the desired notebook in VS Code or Jupyter
2. Select the Python (Pixi MLGEO) kernel
3. Run cells sequentially across the core workflow notebooks:
    - notebooks/Download_Data.ipynb
    - notebooks/data_cleaning.ipynb
    - notebooks/prepare_ai_ready_data.ipynb
    - notebooks/EDA.ipynb
    - notebooks/dimensionality_reduction.ipynb
4. Smoke Test
    - /scripts/smoke_test.py

## Favorite Earth Science Topics:

- Volcanology
- Seismology

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
EOF

## AI Agent Critique & AI-Use Disclosure
### AI Tools & Usage Disclosure
- Tools Used: Large Language Model Assistant (GitHub Copilot)
- Tasks Automated: Routine syntax refactoring, Parquet export, Markdown table formatting, and PCA visualization code.
- Verification Performed: All generated code was executed in the local Pixi environment; file outputs (description.yml and partitions.parqut) were manually inspected and validated against terminal ls and git status checks.

### Critique of Agent Evaluation Report
The full agent evaluation report is saved in AI_logs/agent_eval.md.

Upon auditing the agent's evaluation, the agent awared a score of 2 for criteria B3 (Noise) based on windowed SNR calculations in notebooks/prepare_ai_ready_data.ipynb , but this score is unsupported by the evidence. While the code calucates windowed signal-to-noise ratios, it does not separate or model instrumental sensor noise from background noise. According to the rubric, a score of 2 requires documented instrumental noise. Therefore, B3 strictly scores a 1. I identified this error by directly reading the SNR implementation in the notebook and verifying the absence of instrument response files.

## Reflections and Future Directions

1. What did you learn from this exercise?
I learned how earth science domain constraints dictate machine learning pipeline design. In notebooks/prepare_ai_ready_data.ipynb , partitioning data by station ID rather than random row splitting prevents models from memorizing specific site responses and subsurface path features, ensuring true evaluation on unseen geographic location.

2. What did you learn from interacting with agents or chatbots?
I asked the assistant to generate EDA scripts, PCA dimensionality reduction routines, and rubric score tables. The tool excelled at syntax generation and data formatting, however, it struggled with directory nesting. Duplicate data/ai_ready/data/ai_ready/ paths were created and a score of 2 on criteria B3 was given without verifying wheteher instrumental noise models actually existed  in the repository. I discovered this by inspecting the filesystem and reading the code line by line.

3. What would you suggest to improve this assignment so it meets its learning goals?
I recommend providing explicit guidelines early on regarding how raw HDF5 binary data interacts with tabular Parquet metadata would reduce initial pathing and datatype confusion.

## Licensing

We chose to use the MIT license due to how it allows others to replicate, edit, and duplicate our work with few restrictions. 

