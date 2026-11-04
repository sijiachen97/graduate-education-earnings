# Research workflow: graduate education and earnings

## Working with the research source

`research/` contains the original research code, including data construction and estimation. `code/` retains the smaller, separately documented portfolio utilities. Run research scripts with **`research/` as the working directory**. Original project-root paths have been changed to `.` in these copies; configure any remaining legacy/external input paths before execution. Do not point the copies at the original research folder if you want to keep its outputs unchanged.

Notebook outputs, execution counts and cell metadata have been cleared. Notebook cell order and analysis specifications are retained; the notebooks contain successive specifications and are not advertised as a clean, unattended pipeline. No respondent-level data or model caches are included. `docs/SOURCE_MANIFEST.json` records original relative filenames, source hashes and adaptations.

## Data construction and main analysis

| Notebook under `research/` | Role |
| --- | --- |
| `prepare-data-for-matching.ipynb` | Import and harmonize NSCG SAS waves; write `data-all-waves/update_merged_nscg_2010_to_2021.csv` for respondent matching |
| `merge-save-data.ipynb` | Wave-import variant writing `data-all-waves/merged_nscg_2010_to_2021.csv`, the filename read by the earnings notebook |
| `matching.ipynb` | Construct respondent links and write `matched_df.csv` |
| `regressions.ipynb` | Clean the earnings sample, merge graduation-year unemployment, build experience/degree interactions, estimate earnings specifications and plot coefficients |
| `endogeneity.ipynb` | Master's-attainment selection and composition checks |
| `balance-table.ipynb` | Descriptive balance comparisons |
| `field-transition analysis.ipynb`, `by-degree-type-field-transition.ipynb`, `field-transition-regressions.ipynb` | Field transitions and associated regression analyses |
| `regressions-for-non-repeated-respondents.ipynb`, `regressions-alter-ur.ipynb` | Alternative sample and unemployment specifications |

Start Jupyter with `research/` as the working directory and place downloaded wave files in `data-all-waves/` using the filenames expected by the import notebooks. Follow the data-construction notebooks before selecting and executing the earnings specifications. Review successive cells before running: the notebooks preserve research iterations and are not a single finalized linear batch script.

## Unresolved handoffs and corrections

- `matching.ipynb` exports `matched_df.csv`, whereas `regressions.ipynb` reads `merged_nscg_2010_to_2021.csv`. The exact handoff incorporating reconstructed IDs needs reconciliation; do not assume that renaming the matched output reproduces the published sample.
- `endogeneity.ipynb` reads `data-all-waves/df_final.csv`; the earnings notebook constructs `df_final` in memory, but the saved-file handoff is not established by the included export statements. Verify the intended columns/sample before saving that intermediate file.
- The unemployment merge reads `ur_ba_16y.csv`, identifies column `CGBD16O`, and averages observations by calendar year. This identifies the series label used in the code, but its source vintage and full definition still need verification against the original downloaded file. No substitute series has been introduced.
- Reversed male/female subgroup labels in `endogeneity.ipynb` have been corrected in this copy. Saved outputs were removed, and the corrected subgroup models have not been re-estimated.
- The notebooks contain multiple earnings specifications. Their presence does not certify which cell reproduces each published table; final table-to-cell reconciliation and a full real-data run remain necessary.

The smaller `code/selection_check.py` remains available as a standalone refactored selection diagnostic with synthetic data; it is not a replacement for these earnings and construction notebooks. See [CODE_GUIDE.md](CODE_GUIDE.md) for NSCG download links and the diagnostic's input schema.

## Software referenced by the source

Python imports (including standard-library modules): `collections`, `matplotlib`, `numpy`, `os`, `pandas`, `scipy`, `seaborn`, `statsmodels`.

These are detected imports, not a pinned or tested environment lockfile. The requirements for the smaller `code/` utilities do not necessarily cover the complete research notebooks.
