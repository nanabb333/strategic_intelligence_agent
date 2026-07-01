# Golden Output Philosophy

Golden outputs are stable reference artifacts used to detect regressions. They are not proof that an output is correct.

## Why Golden Outputs Matter

For this repository, golden outputs would help verify:

- API response shape remains stable.
- Run artifacts keep the same filenames and top-level fields.
- Brief sections remain present and ordered.
- Evidence and limitations remain visible.
- Official product terminology and English output structure do not silently drift.

## What Golden Outputs Should Avoid

Golden outputs should not assert every sentence in a long generated brief. That would make tests brittle and discourage useful copy improvements.

They should avoid:

- Exact full-document text matching.
- Claims that the output is scientifically correct.
- Treating one historical analogy as the only acceptable answer.
- Freezing known weaknesses into permanent requirements.

## Recommended Golden Output Strategy

Use small fixtures that check:

- Required top-level API fields.
- Required artifact files.
- Required decision-support sections.
- Required evidence and limitation sections.
- Absence of forbidden advice language.
- Stable JSON structure for a small set of representative cases.

## Current Repository Status

The current test suite includes API shape and artifact smoke tests, but it does not yet include formal golden output fixtures.

## Related Docs

- [Testing](Testing.md)
- [Evaluation Methodology](EvaluationMethodology.md)
- [Future Engineering Recommendations](FutureEngineeringRecommendations.md)
