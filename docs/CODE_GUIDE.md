# Graduate education and initial labor market conditions

## Source data: where to download

Links checked November 4, 2026.

| Source | Download instructions | Preparation still required |
| --- | --- | --- |
| National Survey of College Graduates | [NCSES public-use microdata](https://ncses.nsf.gov/explore-data/microdata), select NSCG. Download the 2010, 2013, 2015, 2017, 2019, and 2021 survey files and their codebooks. The [NSCG survey page](https://ncses.nsf.gov/surveys/national-survey-college-graduates) provides survey documentation and access to earlier cycles. | Harmonize variables and missing-value codes across waves, construct degree/sample variables, and reproduce the project's respondent linkage. |
| Unemployment at bachelor's graduation | [BLS CPS labor-force statistics](https://www.bls.gov/cps/) is the source portal to consult when documenting the original series. | The exact series ID, population/age definition, seasonal adjustment, annual aggregation, and mapping into `UR` still require verification against the original preparation code. No replacement series is prescribed here. |

The current CLI expects an already prepared CSV, **not** a raw NSCG download. `assigned_id` is a project-generated identifier rather than a promised raw public-use field. Merely renaming a survey file will not make it a valid input. Record the official data citations, original filenames, and download dates when reconstructing the inputs.

## Included research code

The repository now includes data-construction and main-analysis source in `research/`, in addition to the focused utilities described below. See [Research workflow](RESEARCH_WORKFLOW.md) for the file-by-file roles, execution order, and unresolved input handoffs. The earlier selection-only completeness inventory has been superseded by that workflow; full numerical replication has not been certified.

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
