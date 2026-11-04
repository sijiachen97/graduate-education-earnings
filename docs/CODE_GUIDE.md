# Graduate education: code guide

All executable research code is under `code/`. `code/data_process/` constructs inputs; `code/analysis/` estimates models and produces tables/figures. Run commands from the repository root. The original research folders are unchanged.

The code is selected against the supplied final paper/slides and their production dependencies, rather than copied as an archive of every experiment. [Source manifest](SOURCE_MANIFEST.json) records original filenames, selected notebook cells, hashes and adaptations. [Source review](SOURCE_REVIEW.json) lists the reviewed source inventory and inclusion/exclusion decisions. No microdata, model caches or saved notebook outputs are shared.

## Final paper and corrected source selection

Reference: the March 2025 final paper, `Sijia_Chen_Graduate_Education.pdf` / `final-paper/Sijia_Chen_3Y_Paper_Revision.pdf`.

The main source is **`look into-regressions-UR-version.ipynb`**, not `regressions.ipynb`. Its final grouped specification reproduces Table 3: **169,092 observations**, early-career bachelor's coefficient **−0.0190876725**, and master's interaction **+0.0243328957**. The consolidated main notebook was executed against the existing local analysis input and reproduces these values.

## Run order and paper correspondence

Open the notebooks in order. Their first cell sets the working directory to the repository root.

| Step | Included notebook | Input → output / paper result |
| --- | --- | --- |
| 1 | `code/data_process/01_import_harmonize_nscg.ipynb` | SAS waves → `data-all-waves/update_merged_nscg_2010_to_2021.csv` |
| 2 | `code/data_process/02_link_respondents.ipynb` | Harmonized waves → `data-all-waves/matched_df.csv`, including reconstructed `assigned_id` |
| 3 | `code/data_process/03_build_analysis_data.ipynb` | Original cells 0–16 of `regressions-for-non-repeated-respondents.ipynb`: matched data → `data-all-waves/df_final.csv` |
| 4 | `code/analysis/01_main_earnings.ipynb` | Original production cells 0, 1, 3, 5, 8, 9, 19 of the final UR-version notebook: Table 3 / Figure 3 |
| 5 | `code/analysis/02_selection_composition.ipynb` | Attainment probit, cohort/composition plots and gender subgroup check: Table 2, Figures 1–2, Appendix A2 |
| 6 | `code/analysis/03_descriptive_tables.ipynb` | Cohort counts and respondent frequency: Table 1 / Appendix A1 |
| 7 | `code/analysis/04_field_transitions.ipynb` | Field-transition pooled regressions and residual plots |
| 8 | `code/analysis/05_field_heterogeneity.ipynb` | Field-specific models and plots: Table 4, Figure 4 and Appendix Figure A1 |

Place the NSCG SAS files and unemployment CSVs in `data-all-waves/`. The preparation notebook expects `epcg{year}.sas7bdat`; follow its exact filename dictionary. The two output handoffs above are now explicitly written to the directory read by the following notebook. No replacement cleaning rules or estimator have been introduced.

The preparation block preserves the original degree-specific `gradur` fields for compatibility. The **final main regression merges and uses the bachelor's-graduation `UR` for both education groups**. It uses survey-year and experience-bin fixed effects and individual-clustered standard errors.

## Replication notes

- Main-regression validation started from the existing `df_final.csv`; the complete raw-wave matching pipeline has not been rerun. Source preparation, linkage and export stages are now present rather than left as an unexplained file handoff.
- The original grouped-plot function approximates the master's confidence band without the covariance between the two coefficients. It is retained to preserve the published Figure 3 source; it should not be used to claim a correctly computed confidence interval for the sum. Table 3 estimation itself is unchanged.
- The original gender-subgroup block reversed the male/female variable labels. The shared copy corrects the labels; Appendix A2 labels/results require reconciliation. The pooled Table 2 model is unchanged.
- Notebook outputs are cleared. The code may print diagnostics when run locally; do not commit respondent previews or generated data.

## Source data: where to download

- [NCSES public-use microdata](https://ncses.nsf.gov/explore-data/microdata): select National Survey of College Graduates, waves 2010, 2013, 2015, 2017, 2019 and 2021; download SAS files and codebooks.
- [FRED CGBD16O](https://fred.stlouisfed.org/series/CGBD16O): BLS unemployment rate for college graduates with a bachelor's degree, age 16 and over. This is the exact series named in paper footnote 2 and the final notebook. Save the downloaded CSV as `ur_ba_16y.csv`; code averages the observations by calendar year.
- [FRED CGMD16O](https://fred.stlouisfed.org/series/CGMD16O): master's-degree series read by the original intermediate-data builder, saved as `ur_ma_16y.csv`. It is not the final main regression's shock variable.

Preserve the original unemployment CSV vintage when reproducing published estimates; a fresh download may contain revisions.

## Software

Install Python packages with `pip install -r requirements.txt`. Jupyter is needed for the preparation/analysis notebooks.

Dependencies are not a fully pinned environment. See [Validation](VALIDATION.md) for what was and was not executed.
