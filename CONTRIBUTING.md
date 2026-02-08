# Contributing to MeroShare IPO Application Bot

Thank you for your interest in contributing! This guide will help you get started.

## How to Contribute

### Reporting Bugs

1. Check [existing issues](https://github.com/YashwanKafle/meroshare-ipo-apply-bot/issues) to avoid duplicates.
2. Open a new issue using the **Bug Report** template.
3. Include steps to reproduce, expected behavior, and actual behavior.

### Suggesting Features

1. Open a new issue using the **Feature Request** template.
2. Describe the feature and why it would be useful.

### Submitting Changes

1. **Fork** the repository and clone your fork.
2. Create a new branch from `master`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes.
4. Ensure your code follows the project's style (formatted with `black`, imports sorted with `isort`).
5. Commit your changes with a clear message:
   ```bash
   git commit -m "feat: add your feature description"
   ```
6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. Open a **Pull Request** against the `master` branch.

## Development Setup

```bash
git clone https://github.com/<your-username>/meroshare-ipo-apply-bot.git
cd meroshare-ipo-apply-bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Code Style

- **Formatter:** [Black](https://github.com/psf/black) with a line length of 79.
- **Import sorting:** [isort](https://pycqa.github.io/isort/) with the `black` profile.
- **Type checking:** [Pyright](https://github.com/microsoft/pyright) in strict mode.

## Commit Message Convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — new feature
- `fix:` — bug fix
- `docs:` — documentation changes
- `refactor:` — code restructuring without behavior change
- `chore:` — maintenance tasks

## Pull Request Guidelines

- Keep PRs focused on a single change.
- Reference related issues (e.g., `Closes #12`).
- Provide a clear description of what was changed and why.
- Ensure there are no linting or type-checking errors.

## Code of Conduct

By participating, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).
