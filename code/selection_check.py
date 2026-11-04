"""Pooled graduate-attainment selection diagnostic; see README for provenance."""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

REQUIRED = ['assigned_id', 'REFYR', 'BAYR', 'DGRDG', 'UR', 'GENDER', 'AGE', 'RACEM', 'EDMOM', 'EDDAD']
FORMULA = 'with_masters ~ UR + cohort_trend + cohort_trend_sq + C(GENDER) + AGE + C(RACEM) + C(EDMOM) + C(EDDAD)'


def prepare_data(df):
    missing = set(REQUIRED) - set(df.columns)
    if missing:
        raise ValueError(f'Missing input columns: {sorted(missing)}')
    df = df.dropna(subset=['assigned_id', 'REFYR']).sort_values('REFYR', kind='stable')
    df = df.drop_duplicates('assigned_id', keep='last').copy()
    # Complete-case filtering before fitting keeps cohort clusters aligned.
    df = df.dropna(subset=REQUIRED)
    df = df.loc[df.BAYR < 2020].copy()
    if df.empty or df.BAYR.nunique() < 2:
        raise ValueError('Need nonempty data with at least two graduation cohorts.')
    df['with_masters'] = (df.DGRDG == 2).astype(int)
    df['cohort_trend'] = df.BAYR - df.BAYR.min()
    df['cohort_trend_sq'] = df.cohort_trend ** 2
    if df.with_masters.nunique() != 2:
        raise ValueError('Both degree outcome categories must be present.')
    return df


def synthetic_data(seed=97, n=3000):
    """Artificial data for execution checks only; no real respondents."""
    rng = np.random.default_rng(seed)
    cohorts = np.arange(2000, 2019)
    cohort_ur = dict(zip(cohorts, rng.uniform(3, 10, len(cohorts))))
    ba = rng.choice(cohorts, n)
    return pd.DataFrame({
        'assigned_id': np.arange(n), 'REFYR': 2021, 'BAYR': ba,
        'DGRDG': rng.choice([1, 2], n, p=[.65, .35]),
        'UR': [cohort_ur[x] for x in ba], 'GENDER': rng.choice(['F', 'M'], n),
        'AGE': rng.integers(25, 60, n), 'RACEM': rng.choice(['A', 'B', 'C'], n),
        'EDMOM': rng.choice([1, 2, 3], n), 'EDDAD': rng.choice([1, 2, 3], n)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--input', type=Path)
    source.add_argument('--demo', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    df = prepare_data(synthetic_data() if args.demo else pd.read_csv(args.input))
    result = smf.probit(FORMULA, data=df, missing='raise').fit(
        disp=False, cov_type='cluster', cov_kwds={'groups': df.BAYR})
    if not result.mle_retvals['converged']:
        raise RuntimeError('Model did not converge; inspect the specification and data.')
    args.output.mkdir(parents=True, exist_ok=True)
    label = 'SYNTHETIC DEMO — NOT RESEARCH RESULTS\n' if args.demo else ''
    (args.output/'summary.txt').write_text(label + result.summary().as_text())
    print(label + f'Observations: {len(df)}; cohorts: {df.BAYR.nunique()}')
    print(f'UR probit coefficient: {result.params["UR"]:.4f}; SE: {result.bse["UR"]:.4f}; p: {result.pvalues["UR"]:.4f}')
    print(f'Saved summary to {args.output / "summary.txt"}')


if __name__ == '__main__':
    main()
