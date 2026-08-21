# Contributing

Contributions are welcome when they make a skill more specific, more useful, or easier to verify.

## Good contributions

- a recurring AI tell with a clear reader-facing cost and a before-and-after example
- a detector pattern with a must-fail case and a must-pass case
- a false positive removed from `slop-detector.json`, with the sentence that exposed it
- a missing edge case, state, or accessibility check in the design skills
- clearer wording that keeps a rule short enough to act on

Avoid rules based only on taste, and avoid declaring a word bad in every context. The severity model exists because most tells are evidence, not proof.

## Before opening a pull request

1. Edit the relevant `SKILL.md`, reference file, or `slop-detector.json`.
2. If you touched the detector, add your cases to `slop-detector/scripts/test-severity.py`.
3. Run `./scripts/validate.sh`.
4. Describe the reader-facing problem the change solves.

## Licensing

`stop-slop`, `slop-detector`, and the repository scaffolding are MIT. The five impeccable-derived skills (`clarify`, `distill`, `quieter`, `polish`, `harden`) are Apache-2.0, and `red-pen` is redistributed from Rich Tabor without a license grant. Contributions to a folder are licensed under that folder's license. See [NOTICE.md](./NOTICE.md).
