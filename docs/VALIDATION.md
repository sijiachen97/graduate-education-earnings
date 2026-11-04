# Validation and remaining issues

Consolidation checks, November 4, 2026: 0 R files, 0 Python files, 8 notebooks (127 code cells), and 0 shell entrypoints passed syntax checks. Notebook outputs and execution counts were cleared. Source hashes and adapted-file hashes are in SOURCE_MANIFEST.json.

The consolidated `code/analysis/01_main_earnings.ipynb` was executed against the existing local `df_final.csv` and original unemployment CSV. Results match final paper Table 3 after rounding:

- Observations: 169,092.
- Bachelor's early-career coefficient: -0.0190876725.
- Master's early-career interaction: 0.0243328957.

The full NSCG import/linkage pipeline and other regressions were not rerun. Original Figure 3 plotting code omits covariance in the approximate confidence band for the summed master’s effect; preserved for traceability, not endorsed as correct inference. Reversed gender-subgroup labels in the original endogeneity notebook were corrected in the copy; Appendix A2 needs reconciliation.
