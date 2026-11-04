# Graduate education and initial labor market conditions

This project examines how the association between labor market conditions at bachelor's graduation and later earnings differs by subsequent master's attainment. The broader research uses repeated NSCG survey waves and earnings regressions.

## Featured code: selection diagnostic

`selection_check.py` is a refactored extract of the original exploratory notebook's pooled probit specification. It asks whether unemployment at bachelor's graduation predicts later master's attainment, controlling for demographic characteristics and a quadratic graduation-cohort trend. Standard errors are clustered by bachelor's graduation cohort.

This is a selection diagnostic, not an instrument or a causal estimate of the return to a master's degree. It does not eliminate selection on unobserved characteristics.

```sh
python code/selection_check.py --demo --output /tmp/education-demo
python code/selection_check.py --input /path/to/prepared.csv --output /path/to/results
```

The demo generates artificial observations to exercise the workflow; its estimates are not research findings. Real input must already be cleaned and coded using the project's conventions.

| Column | Meaning |
| --- | --- |
| `assigned_id` | Respondent identifier used to keep the latest observation |
| `REFYR` | Survey reference year |
| `BAYR` | Bachelor's graduation year |
| `DGRDG` | Degree category; 2 identifies master's attainment in this sample |
| `UR` | Unemployment rate at bachelor's graduation, in percentage points |
| `GENDER`, `RACEM` | Gender and race categories |
| `AGE` | Age |
| `EDMOM`, `EDDAD` | Parental education categories |

The script reports the probit coefficient, standard error and p-value for `UR`; the coefficient is not a probability marginal effect. It excludes cohorts from 2020 onward, consistent with the selected notebook specification. The full paper's sample construction is upstream and is not reproduced here.
