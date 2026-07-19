# Pre-commit Hooks Setup

This project uses `pre-commit` hooks to maintain code quality and run tests automatically before commits.

## Installation

1. **Install pre-commit (one-time setup):**
```bash
pip3 install pre-commit --break-system-packages
```

2. **Install the pre-commit hooks in your repository:**
```bash
pre-commit install
```

This command creates a `.git/hooks/pre-commit` file that runs on every commit.

## Configuration Files

- **`.pre-commit-config.yaml`** - Main configuration for pre-commit hooks
- **`.flake8`** - Configuration for flake8 (Python linter)
- **`.pylintrc`** - Configuration for pylint (Python code analyzer)
- **`.bandit`** - Configuration for bandit (security scanner)

## Hooks Enabled

### 1. **flake8** (Linting)
- Enforces PEP 8 style guide
- Checks for common Python errors
- Configured to allow:
  - Lines up to 100 characters
  - Specific style relaxations (E203, W503, W504)
- Skips: `__pycache__`, venv, build artifacts, circular import files

### 2. **pytest** (Testing)
- Runs all tests in the `tests/` directory
- Exits with failure if any test fails
- Prevents commits with failing tests

## Usage

### Commit with hooks enabled (default)
```bash
git commit -m "Your commit message"
```

If hooks fail:
- flake8 will report style issues
- pytest will show test failures
- Fix the issues and re-run `git commit`

### Skip hooks (not recommended)
```bash
git commit --no-verify -m "Your commit message"
```

### Run hooks manually on all files
```bash
pre-commit run --all-files
```

### Run hooks manually on changed files only
```bash
pre-commit run
```

## Troubleshooting

### "pre-commit: command not found"
Install pre-commit:
```bash
pip3 install pre-commit --break-system-packages
```

### Hooks not running
Re-install hooks:
```bash
pre-commit install
```

### Want to skip hooks temporarily
```bash
git commit --no-verify -m "WIP: temporary commit"
```

### Clear pre-commit cache
```bash
pre-commit clean
```

## Continuous Integration

The same checks run in CI/CD pipelines:
- GitHub Actions will run `pytest tests/` to verify all changes
- Code quality checks can be integrated into branch protection rules

## Contributing

When contributing to this project:
1. Ensure all tests pass locally: `pytest tests/`
2. Let pre-commit hooks run before committing
3. Address any flake8 warnings before pushing
4. All 110+ tests must pass

## Notes

- Test files in `tests/` are excluded from some linting rules (docstring requirements)
- Circular import protection excludes `defect3d/__init__.py` and `defect3d/clock_mechanisms/__init__.py` from strict import checks
- The project targets 100-character line lengths
