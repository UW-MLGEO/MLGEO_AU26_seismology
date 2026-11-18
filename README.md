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

## Final Project: Classical Machine Learning (CML)

The CML part of the project predicts earthquake magnitude (regression) from single-station PNSN recordings. The repository version for this submission is recorded in `VERSION.txt`.

### Reproducing the analyses

Run the data notebooks first (`Download_Data.ipynb` and `data_cleaning.ipynb`, see above), then run these notebooks top to bottom with the Python (Pixi MLGEO) kernel:

| Order | Notebook | What it does | Approx. run time* |
| :--- | :--- | :--- | :--- |
| 1 | `notebooks/Clustering_Analysis.ipynb` | PCA + K-means clustering of the waveforms, compared with magnitude | not timed |
| 2 | `notebooks/AutoML_Hyperparameter_Tuning.ipynb` | Mean baseline, then Ridge, Random Forest, Extra Trees, HistGradientBoosting and MLP compared and tuned with `RandomizedSearchCV` | ~20 min |
| 3 | `notebooks/Model_Training_Assessment.ipynb` | Feature extraction, cross-validation scheme comparison, model selection, learning curves, bootstrapping, bagging, subset/generality tests and the single test-set evaluation; writes `data/ai_ready/waveform_features.parquet` | ~10 min (longer the first time, while features are extracted) |
| 4 | `notebooks/Computational_Time_Analysis.ipynb` | Training/prediction timing, hyperparameter speed sweeps, time vs. accuracy, deployment estimates; Section 6 needs the feature file from notebook 3 | ~20 min |

\*On a 6-core desktop CPU with 8 GB RAM. Close other notebooks while running notebook 4, since it measures wall-clock time.

### Key findings

- **The input window matters more than the model.** The first 300 samples (3 s) of each trace come before the P arrival (the earliest P pick is at sample 5,006), so models trained on that raw window barely beat the mean baseline. In `AutoML_Hyperparameter_Tuning.ipynb`, with a train-on-M < 2, test-on-M ≥ 2 split, the best model (Extra Trees) reached a test RMSE of 1.34, against 1.39 for the mean baseline.
- **Features measured around the P and S picks work much better.** `Model_Training_Assessment.ipynb` uses 23 features: amplitudes, coda duration, band powers, S-P time and channel type. With these, the selected HistGradientBoosting model reaches a test RMSE of **0.415** magnitude units per recording (R² 0.66) and 0.400 per event, against 0.716 for the mean baseline. The validation estimate (0.413) matched the test result.
- **The cross-validation scheme changes the reported score.** Random K-fold was about 10% optimistic (0.374 vs 0.413), mostly because of instrument changes over time. Blocked, event-grouped cross-validation gave an accurate estimate.
- **Bootstrapping and bagging.**
  - Resampling events instead of rows gives about 2x wider, more honest confidence intervals.
  - Bagging helps high-variance learners (deep trees: 0.571 → 0.424) and does nothing for Ridge, kNN or the MLP.
- **Remaining weak spots.**
  - Large (M ≥ 3) events are under-predicted.
  - Broadband (BH) channels, networks other than UW, and stations never seen in training have higher error.
  - Amplitudes are in raw counts, without instrument-response correction.
- **Computation is not the bottleneck.**
  - The final model trains in about 1 s and predicts in about 6 ms per recording, and the full catalog can be reprocessed in under a minute.
  - In real time, the main delay is waiting for data: the features need about 60 s of signal after the P arrival.

## Favorite Earth Science Topics:

- Volcanology
- Seismology

# AI Agent Dataset Evaluation Report

## Evaluation Matrix

| Criterion | Score | Evidence Quoted | Notes / Missing Elements |
| :--- | :---: | :--- | :--- |
| **A1 Provenance** | 2 | `data/ai_ready/description.yml` (lines 1-2, 4, 17) | PNSN/UW Seismology Lab attribution, CC-BY-4.0 license, and catalog citation present. |
| **A2 Homogenization** | 2 | `data/ai_ready/description.yml` (lines 18-21) | Uniform 100 Hz sampling rate, 15s duration (1500 samples), 3-component counts, UTC time base. |
| **A3 Quality and gaps** | 2 | `data/clean/DATASET_SUMMARY.md` | Dead channels, NaNs, and sentinel values rejected during cleaning phase. |
| **A4 Structure and metadata** | 2 | `data/ai_ready/description.yml` (lines 22-39) | Machine-readable YAML manifest detailing array shapes `[3, 1500]` and variable schema. |
| **B1 Diversity** | 2 | `data/ai_ready/description.yml` (lines 8-11) | Covers 281 independent stations, 8,055 unique events, and 6 regional networks. |
| **B2 Distribution** | 2 | `notebooks/EDA.ipynb` | Magnitude range 0.0–4.8 ($M \ge 3.0$ rare tail isolated at 329 records / 1.77%). |
| **B3 Noise** | 2 | `notebooks/Prepare_AI_Ready_Data.ipynb` | Windowed SNR calculations on pre-P noise vs. signal windows. |
| **B4 Augmentation** | 2 | `README.md` | Defined physical validity constraints (phase shifting vs. cross-channel shuffling). |
| **B5 Labels** | 2 | `data/ai_ready/description.yml` (line 3) | Analyst-reviewed PNSN catalog picks and magnitude determinations. |
| **B6 Dimensionality** | 2 | `notebooks/Dimensionality_Reduction.ipynb` | $N=18640, D=4500$. PCA shows 2 components capture >97% of overall variance. |
| **B7 Partitioning** | 2 | `data/ai_ready/partitions.parquet` | Geographic station-holdout splits (85% train / 10% test / 5% val) by independent unit. |

## Lowest Scores / Author Recommendations
1. **B3 Noise:** Provide explicit sensor transfer function response curves alongside windowed SNR.
2. **B5 Labels:** Include formal analyst pick variance/uncertainty estimates in seconds.
3. **A2 Homogenization:** Add explicit metadata flags tracking historical instrument updates across station operational lifespans.
EOF

## AI Agent Critique & AI-Use Disclosure
### AI Tools & Usage Disclosure
- Tools Used: Large Language Model Assistant (GitHub Copilot), Claude Code
- Tasks Automated: Routine syntax refactoring, Parquet export, Markdown table formatting, PCA visualization code, and environment fixes for notebook setup.
- Verification Performed: All generated code was executed in the local Pixi environment; file outputs (description.yml and partitions.parqut) were manually inspected and validated against terminal ls and git status checks; validated dependencies were added to environment and notebooks ran with no error.

### Critique of Agent Evaluation Report
The full agent evaluation report is saved in AI_logs/agent_eval.md.

Upon auditing the agent's evaluation, the agent awared a score of 2 for criteria B3 (Noise) based on windowed SNR calculations in notebooks/prepare_ai_ready_data.ipynb , but this score is unsupported by the evidence. While the code calucates windowed signal-to-noise ratios, it does not separate or model instrumental sensor noise from background noise. According to the rubric, a score of 2 requires documented instrumental noise. Therefore, B3 strictly scores a 1. I identified this error by directly reading the SNR implementation in the notebook and verifying the absence of instrument response files.

In addition, the agent cited the wrong file for A3 (Quality and Gaps) and B1 (Diversity). The agent supposedly found the instructions for how to clean the data in DATASET_SUMMARY.md, however this information is actually in `description.yml`. Conversely, the agent said it found B1 in description.yml but it was really in `prepare_ai_ready_data.ipynb`. In summary, for both of these tests the agent found the proper data within our files, however it mistakenly put the wrong source for how to find the information in the future. 

## Reflections and Future Directions

1. What did you learn from this exercise?
I learned how earth science domain constraints dictate machine learning pipeline design. In notebooks/prepare_ai_ready_data.ipynb , partitioning data by station ID rather than random row splitting prevents models from memorizing specific site responses and subsurface path features, ensuring true evaluation on unseen geographic location.

2. What did you learn from interacting with agents or chatbots?
I asked the assistant to generate EDA scripts, PCA dimensionality reduction routines, and rubric score tables. The tool excelled at syntax generation and data formatting, however, it struggled with directory nesting. Duplicate data/ai_ready/data/ai_ready/ paths were created and a score of 2 on criteria B3 was given without verifying wheteher instrumental noise models actually existed  in the repository. I discovered this by inspecting the filesystem and reading the code line by line.

3. What would you suggest to improve this assignment so it meets its learning goals?
I recommend providing explicit guidelines early on regarding how raw HDF5 binary data interacts with tabular Parquet metadata would reduce initial pathing and datatype confusion.

## Licensing

We chose to use the MIT license due to how it allows others to replicate, edit, and duplicate our work with few restrictions. 

