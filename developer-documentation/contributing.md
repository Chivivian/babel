# Contributing to Babel

Thank you for your interest in contributing to Babel! This document outlines the process for contributing code, documentation, and new language support.

---

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/babel.git
   cd babel
   ```
3. **Set up the development environment** by following the [Setup Guide](./setup-guide.md).

---

## Code Style

We follow standard conventions to keep the codebase consistent:

### Python

- **Formatter:** Black (default settings)
- **Linter:** Ruff
- **Typing:** Use type hints for all function signatures.

Run formatting before committing:
```bash
black babel-backend/
ruff check babel-backend/
```

### JavaScript/TypeScript (Frontend)

- **Formatter:** Prettier
- **Linter:** ESLint

Run formatting:
```bash
npm run lint
npm run format
```

---

## Branching Strategy

We use a simple branching model:

| Branch | Purpose |
| :--- | :--- |
| `main` | Production-ready code. All PRs merge here. |
| `feature/*` | New features (e.g., `feature/arabic-support`). |
| `fix/*` | Bug fixes (e.g., `fix/pdf-parsing-error`). |
| `docs/*` | Documentation updates (e.g., `docs/api-examples`). |

### Creating a Branch

```bash
git checkout -b feature/your-feature-name
```

---

## Making Changes

1. **Create a new branch** from `main`.
2. **Make your changes** with clear, atomic commits.
3. **Write or update tests** if applicable.
4. **Run the test suite** to ensure nothing is broken.
5. **Push your branch** and open a Pull Request.

### Commit Messages

Use clear, descriptive commit messages:

- ✅ `Add Arabic language support with custom font handling`
- ✅ `Fix PDF parsing error for scanned documents`
- ❌ `Fix bug`
- ❌ `Update stuff`

---

## Pull Request Process

1. Open a PR against the `main` branch.
2. Fill out the PR template with:
   - **What** the change does.
   - **Why** it was needed.
   - **How** to test it.
3. Request a review from a maintainer.
4. Address any feedback and push updates.
5. Once approved, a maintainer will merge your PR.

---

## Running Tests

We have a test suite located in the `test/` directory.

### Running All Tests

```bash
cd test
python -m pytest
```

### Running a Specific Test

```bash
python -m pytest test_translation.py::test_french_translation
```

---

## Adding a New Language

To add support for a new language:

1. **Add the language code** to the `ALL_LANGUAGES` dictionary in `translate.py`:
   ```python
   ALL_LANGUAGES = {
       ...
       "sw": "Swahili",
   }
   ```

2. **Verify font support** – Ensure the system has fonts for the new language. For most common languages, this is already handled by TeX Live.

3. **Test the language** by running a translation:
   ```bash
   python translate.py test.pdf --lang sw
   ```

4. **Update the documentation** – Add the language to `documentation/supported-languages.md`.

5. **Open a PR** with your changes.

---

## Reporting Issues

If you find a bug or have a feature request:

1. **Search existing issues** to avoid duplicates.
2. **Open a new issue** with a clear title and description.
3. **Include reproduction steps** if reporting a bug.
4. **Label your issue** (e.g., `bug`, `enhancement`, `documentation`).

---

## Code of Conduct

We are committed to fostering an open and welcoming community. Please be respectful and constructive in all interactions.

---

## Questions?

If you have questions about contributing, feel free to:

- Open a GitHub Discussion.
- Reach out to the maintainers at **dev@lunartech.ai**.

---

Thank you for helping make Babel better! 🚀
