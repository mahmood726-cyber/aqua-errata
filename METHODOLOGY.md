# Methodology and disclosure

Reuses the two completed AQuA audit evidence packages and their verifiers. New work is a public register, integration checks, documentation, and portable optional upstream retrieval. Packaging adds no new findings.

Portfolio reconnaissance found no matches for `AQuA dataset errata`; the searched manifest reported generatedAt `2026-04-27T00:00:00Z` and contained a limited seven-project sample. This is not evidence that related work is absent elsewhere.

| Kind | Disclosure |
|---|---|
| Static | Reviewed case selection, mathematical templates and custom cases, unit aliases, pinned commit and hashes, regression expectations, exclusion decisions, and numerical tolerances |
| Dynamic | Source identities and hashes, calculations, option equivalence, category totals, overlap checks, and optional full-source comparisons |

Initial batch: 354 records / 304 distinct exact question texts. Scoring batch: 624 records / 588 distinct exact question texts. Distinct-question counts are per batch and must not be added as estimates of independent problems. Integration uses file and one-based line, rejecting overlap. Source record fields, including awkward wording and formatting, are preserved.

See `evidence/*/review_exclusions.json`. Already reported upstream issue #1 (test line 153) is excluded. Rationale arithmetic checks establish only the cited local inequality. Wrong-key checks use explicit reviewed templates and tolerances; they are not a general proof system. Key-content collisions establish repeated option content, not universal correctness of that content. Paired-output records need contextual question/choice repair review.

The archived scoring manifest retains cumulative 1,027 totals from the combined reporting campaign, which included 49 BIG-bench records. Those campaign totals are not this repository's AQuA count. `summary.json` gives the AQuA-only total, 978. In the original manifest, `accepted_records` means accepted into the auditor's reviewed set, not author acceptance.

Private email bodies, delivery records, mailbox identifiers, and private contacts are excluded. Public author-contact metadata in original manifests is retained as provenance. This is a public research artifact, not portfolio certification or a complete dataset cleaning claim.
## Publication review

Fresh upstream retrieval passed SHA-256 and Git blob identity for all three pinned splits and exact field comparison for all 978 selected records. Both batch verifiers and integrated register checks passed on 28 October 2026.

Sentinel pre-publication scan: zero blocking findings, seven warnings. Two claim-grounding warnings refer to percentages inside quoted original math questions, which have pinned row citations. Five encoding warnings concern preserved upstream text or template keys matching that text. They were reviewed against hashed source records; changing them in the evidence would corrupt provenance. Original text is retained. Git attributes disable newline conversion to preserve evidence hashes across Windows and Unix checkouts.
