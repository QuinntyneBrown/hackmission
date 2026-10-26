# Contributing to HackMission

Thank you for your interest in contributing. By participating, you agree to follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Ways to contribute

- Report a bug or suggest a feature through the repository issue templates.
- Improve documentation, mocks, or the design system.
- Contribute a focused code change for an agreed issue.

For security issues, use the private process in [SECURITY.md](SECURITY.md), not a public issue.

## Before you start

1. Search existing issues to avoid duplicates.
2. For work larger than a small fix, open an issue first and agree on the approach with a maintainer.
3. Read [AGENTS.md](AGENTS.md). It is the source of truth for the mandatory structure, architecture, and coding conventions.

## How changes are made

Production behavior changes follow this order: requirement, detailed design, mock, failing Given-When-Then acceptance test, then small implementation slices. Documentation-only, mock-only, design-system-only, and test-only work skips the steps that do not apply.

Keep each pull request focused. Run the applicable format, lint, build, and test checks before opening it.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/) and keep each commit focused:

```text
feat(events): add registration confirmation state
fix(marketing): preserve email after a subscription error
docs(mocks): add the event list empty state
```

## Pull requests

1. Create a branch from `main` (`feature/<short-name>` or `fix/<short-name>`).
2. Make the change according to [AGENTS.md](AGENTS.md).
3. Open a pull request, link the issue it resolves, and complete the template.
4. Address review feedback with follow-up commits.

By submitting a contribution, you confirm that you have the right to submit it and license it under the [MIT License](LICENSE).
