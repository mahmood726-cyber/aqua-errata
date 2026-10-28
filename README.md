# AQuA public errata register

Reproducible, source-linked audit findings for **978 affected AQuA source records** at commit [`26b64ed1f22208c6742f47df547dfd65088ec30d`](https://github.com/google-deepmind/AQuA/tree/26b64ed1f22208c6742f47df547dfd65088ec30d). Audit date: 28 October 2026. Maintainer: Mahmood Ahmad.

These are affected-record counts, including repeated questions and shared causes. They are not 978 independent defects, wrong final answers, or author-approved corrections. The 49 BIG-bench findings from a separate audit are outside this repository.

## Browse the evidence

- [Itemized register](errata.jsonl) and [computed category totals](summary.json).
- [Initial 354-record evidence](evidence/initial/findings.json) and [readable HTML report](initial.html).
- [Additional 624-record evidence](evidence/scoring/findings.json) and [readable HTML report](scoring.html).
- Entries link to exact upstream files and one-based lines. Evidence includes original questions, choices, rationales, keys, record hashes, and checked discrepancies.

| Category | Records | What is established |
|---|---:|---|
| False numeric equalities in rationales | 223 | The cited equality is false; this alone does not establish a wrong final key |
| Question/key discrepancies | 121 | Reviewed formula-based discrepancies, with assumptions and tolerances in the verifier |
| Checked key/conclusion conflicts | 10 | Calculated result and rationale/key disagreement |
| Missing numerical choices | 60 | Numerical answers absent; choices contain units only |
| Identical content under keyed and other labels | 427 | Duplicate keyed content conflicts with a unique-option design; mathematical correctness is not established for every keyed value |
| Numerically equivalent keyed choices | 57 | Exact value-equivalent choices under multiple labels |
| Requested pair absent from choices | 63 | Question asks for two distinct outputs but choices are scalar |
| Additional solved wrong-key/missing-option cases | 17 | Calculated result disagrees with the published key or available values |

## Reproduce

Python 3.10 or later; default checks use only the standard library:

```sh
python verify.py
```

Runs both batch verifiers, validates evidence hashes, joins the register to original evidence, rejects source-record overlap, and recomputes totals. Original verifiers use assertions; do not run with Python optimization (`-O`). The wrapper rejects optimized execution.

Optional full source comparison:

```sh
python verify.py --upstream
```

Downloads the three pinned original splits (about 48 MB) into ignored `source-cache/`, verifies SHA-256 and Git blob hashes, then compares all selected records. Requires internet access. Default checks verify bundled evidence, not fresh upstream retrieval. Archived second-pass summaries document checks performed during the audit; they are historical evidence, not fresh reruns of independent implementations.

## Interpretation and limitations

This is an **errata register**, with proposed labels where available. Original splits are preserved; there is no automatically relabeled or purportedly fully cleaned dataset. Proposed labels need contextual review, especially where wording, formatting, rounding, or missing choices require repairs beyond changing a letter. See [methodology](METHODOLOGY.md).

No model benchmarks were rerun. Duplicate labels can affect single-letter grading, but actual score or ranking changes are not quantified. Selection was targeted, not representative; no dataset-wide error prevalence is inferred. The [upstream README](https://github.com/google-deepmind/AQuA/blob/26b64ed1f22208c6742f47df547dfd65088ec30d/README.md) states that the original paper used a different earlier dataset; these findings do not establish an error in its published results.

The audit was shared with dataset authors. One author welcomed public errata publication and explained that the archived legacy repository has no active update process. This acknowledgement is not item-by-item validation or endorsement. Private correspondence is not included.

## Review and contributions

Open an issue with the case ID, pinned source link, proposed disposition, and worked derivation. Preserve original evidence and log reasons for status changes. Before producing cleaned splits, adjudicate each change, preserve split membership and original IDs, publish a change log, and rerun source and mathematical checks. Structural ambiguity may require exclusion or rewriting rather than relabeling.

## Source and license

Original dataset: [Wang Ling, Dani Yogatama, Chris Dyer, and Phil Blunsom (2017), Program Induction by Rationale Generation](https://aclanthology.org/P17-1015/). Source: [google-deepmind/AQuA](https://github.com/google-deepmind/AQuA). Copyright 2017 Google Inc.; source notices retained. This register and audit code are Apache-2.0; see [LICENSE](LICENSE) and [NOTICE](NOTICE). Independent community audit; no Google affiliation or official endorsement is claimed.
