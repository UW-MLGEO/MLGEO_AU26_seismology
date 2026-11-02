# MLGEO_AU26_seismology
This repository provides an end-to-end pipeline to acquire, clean, document, and partition a 3-component ground motion seismic dataset from the Pacific Northwest Seismic Network (PNSN). The dataset is formatted to satisfy rigorous benchmark specifications for machine learning workflows in geophysics and earth observation.
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
# Install environment dependencies via Pixi
pixi install

# Register the Pixi kernel for Jupyter notebooks (VS Code / Jupyter Lab)
pixi run python -m ipykernel install --user --name MLGEO_AU26_seismology --display-name "Python (Pixi MLGEO)
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

## Favorite Earth Science Topics:

- Volcanology
- Seismology

## AI Readiness Criteria Evaluation Matrix

| Category | Criteria | Score | Rationale & Code Evidence Location |
| :--- | :--- | :---: | :--- |
| **A. Data Processing Pipeline** | A1. Pipeline Structure & Reproducibility | 1.0 | Standardized modular directory structure (`data/raw/`, `data/clean/`, `data/ai_ready/`, `notebooks/`, `scripts/`). Fully reproducible via Pixi environment configuration (`pixi.toml`). |
| | A2. Raw Data Preservation | 1.0 | Unaltered HDF5 raw waveform datasets preserved in `data/raw/waveforms.hdf5`. All cleaning outputs written strictly to separate `data/clean/` directory. |
| | A3. Metadata & Inventory Tracking | 1.0 | Dataset inventory summarized in `data/clean/DATASET_SUMMARY.md` documenting schema, trace counts, missing value policies, and file sizes. |
| | A4. AI-Ready Export Manifest | 1.0 | Machine-readable YAML manifest exported to `data/ai_ready/description.yml` specifying array dimensions, sampling rates, unit metrics, and variable schemas. |
| **B. AI Readiness Criteria** | B1. Sample Diversity & Unit Metrics | 1.0 | Dataset spans 281 independent seismic stations, 8,055 unique seismic events, and 6 network operators across the Pacific Northwest region. |
| | B2. Target & Feature Distribution | 1.0 | Documented in `notebooks/EDA.ipynb`. Target $M_w/M_L$ distribution ranges from 0.0 to 4.8 (mean 1.32). Rare tail class ($M \ge 3.0$) isolated (329 records / 1.77%). |
| | B3. Signal-to-Noise & Quality Assessment | 1.0 | Evaluated SNR on waveform windows in `notebooks/Prepare_AI_Ready_Data.ipynb`. Rejection logic handles missing/flatlined signals and non-numeric artifacts. |
| | B4. Data Augmentation Validity | 1.0 | Defined physical validity constraints: random temporal shifts preserve wave phase alignment; independent cross-channel shuffling breaks wave polarization physics. |
| | B5. Label Provenance & Data Leakage | 1.0 | Labels sourced directly from PNSN catalog analyst picks. Station-based geographic partitioning prevents spatiotemporal data leakage between splits. |
| | B6. Dimensionality & Space Complexity | 1.0 | Analyzed in `notebooks/Dimensionality_Reduction.ipynb`. Full raw tensor dimension $N=18640, D=4500$ (~320 MB float32). PCA shows just **2 components** capture $\ge 90\%$ (over $97\%$) of overall variance due to dominant amplitude scale factors. |
| | B7. Independent Partitioning Strategy | 1.0 | Station holdout partition exported to `data/ai_ready/partitions.parquet` (85% train: 15,808; 10% test: 1,781; 5% val: 1,051). |

## Agentic Workflow Critique

### Strengths and Efficiency Gains
- Automated Refactoring: AI tools accelerated routine conversion, file format standardization (CSV to Parquet), and HDF5 slicing logic.
- Error Diagnostics: Fast identification of datatype mismatches (string SNR values in pandas) and pathing nesting issues in terminal environments

### Failures and Technical Blind Spots

- Missing Domain Constraints: AI initial scripts attempted generic random row splitting rather than seismology specific station holdout partitioning, which would cause spatiotemporal data leakage.
- Type Assumptions: Assumed HDF5 attributes and metadata numeric fields contained uniform floats, requiring manual exception handling for non-numerica/NaN values.

## Reflections and Future Directions

1. How does station based holdout partitioning protect deep learning models from overestimating generalization performance on regional seismic data? Seismic signals recorded at the same station share identical sit responses, subsurface geology, and sensor path characteristics. Randomly splitting traces across time would put traces from the same station into both train and test sets, allowing neural networks to memorize stationsignatures rather than learning earthquake physics. Geographic station holdout guarantees the model is evaluated on unseen locations.

2. What are the primary computational bottlenecks when scaling waveform tensor processing from thousands to millions of records? Random disk inputs/outputs across massive HDF5 files represent the main bottleneck. At scale, chunking strategies, converting binary stores to modern cloud native formats, and pre-loading flattened contiguous arrays into GPU memory during batching become essential to prevent pipeline starvation.

## Licensing

We chose to use the MIT license due to how it allows others to replicate, edit, and duplicate our work with few restrictions. 

