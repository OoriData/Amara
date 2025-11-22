Amara Contributor Guide

# Quick Reference

## Why We Use `uv pip install -U .`

This project uses a source layout where `pylib/` becomes `amara/` during package building. This remapping only happens during wheel building, not in development environments.

**Why not use hatch environments?**
- Hatch's path remapping (`tool.hatch.build.sources`) only applies during wheel building
- Hatch's dev-mode uses editable installs which can't apply the source remapping
- Setting `dev-mode=false` means no install happens at all

**Solution:** We use proper package installation (`uv pip install -U .`) instead of editable/dev-mode installs. This ensures the source remapping is applied correctly and your development environment matches the built package.

See also the note in `pyproject.toml` at `[tool.hatch.build.targets.wheel]` for more details on this limitation.

## Daily Development

```bash
# Install in current virtualenv
uv pip install -U .

# Run tests
pytest test/ -v

# Run specific test file
pytest test/iri/test_iri.py -v
pytest test/uxml/test_parser.py -v

# Run linting
ruff check .

# Auto-fix linting issues
ruff check --fix .

# Run tests with coverage
pytest test/ --cov=amara --cov-report=html
```

## Making Changes

```bash
# After editing any Python files in pylib/
uv pip install -U .

# After editing resources/
uv pip install -U .

# After editing tests only (no reinstall needed)
pytest test/ -v
```

## Useful Commands

```bash
# See package structure after install
python -c "import amara, os; print(os.path.dirname(amara.__file__))"
ls -la $(python -c "import amara, os; print(os.path.dirname(amara.__file__))")

# Check what files are in the installed package
pip show -f amara

# Check installed version
python -c "import amara; print(amara.__version__)"

# Compare source version
cat pylib/__about__.py

# Uninstall completely
pip uninstall amara -y

# Clean build artifacts
rm -rf build/ dist/ *.egg-info
rm -rf .pytest_cache .ruff_cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
```

## Testing Package Build Locally

```bash
# Build locally
python -m build
python -m build -w  # For some reason needs to need both, in this order. Probably an issue in how we're using hatch

# Test the built wheel (replace X.Y.Z with actual version)
pip install dist/Amara-X.Y.Z-py3-none-any.whl --force-reinstall

# Check package contents (replace X.Y.Z with actual version)
unzip -l dist/Amara-X.Y.Z-py3-none-any.whl
```

# Project Structure

```
Amara/
├── pylib/              # Source code (becomes 'amara' package when installed)
│   ├── __init__.py
│   ├── __about__.py    # Version info
│   ├── iri/            # IRI processing modules
│   │   ├── __init__.py
│   │   ├── iri.py      # Core IRI class and functions
│   │   ├── irihelper.py
│   │   ├── inputsource.py
│   │   └── asynctools.py
│   ├── uxml/           # MicroXML/XML processing modules
│   │   ├── __init__.py
│   │   ├── parser.py   # XML/MicroXML parser
│   │   ├── tree.py     # Tree data model
│   │   ├── html5.py    # HTML5 parsing
│   │   ├── writer.py   # XML writer
│   │   └── cli/        # Command-line tools
│   │       └── microx.py
│   └── uxpath/         # MicroXPath query module
│       ├── __init__.py
│       ├── xast.py
│       └── grammar.lark
├── test/               # Tests
│   ├── conftest.py
│   ├── test_readme.py
│   ├── iri/            # IRI tests
│   │   ├── test_iri.py
│   │   ├── test_iri_attrs.py
│   │   └── test_inputsource.py
│   ├── uxml/           # XML/UXML tests
│   │   ├── test_parser.py
│   │   ├── test_tree.py
│   │   ├── test_html5.py
│   │   ├── test_writer.py
│   │   └── test_uxpath.py
│   └── resource/       # Test resources
│       ├── chansonbalisage.xml
│       └── quoteattr.xml
├── pyproject.toml      # Project config
├── README.md
└── CHANGELOG.md
```

When installed, becomes:

```
site-packages/
└── amara/
    ├── __init__.py
    ├── __about__.py
    ├── iri/
    │   ├── __init__.py
    │   ├── iri.py
    │   ├── irihelper.py
    │   ├── inputsource.py
    │   └── asynctools.py
    ├── uxml/
    │   ├── __init__.py
    │   ├── parser.py
    │   ├── tree.py
    │   ├── html5.py
    │   ├── writer.py
    │   └── cli/
    │       └── microx.py
    └── uxpath/
        ├── __init__.py
        ├── xast.py
        └── grammar.lark
```

## Key Files

- `pylib/__about__.py` - Version number (update for releases)
- `pyproject.toml` - Dependencies, metadata, build config
- `pylib/iri/iri.py` - Core IRI implementation
- `pylib/uxml/parser.py` - XML/MicroXML parser
- `pylib/uxml/tree.py` - Tree data model
- `pylib/uxml/cli/microx.py` - Command-line tool implementation
- `pylib/uxpath/` - MicroXPath query implementation
- `test/resource/` - Test data files (XML, etc.)
- `README.md` - Main documentation
- `CHANGELOG.md` - Release notes

# Publishing a Release

Before creating a release:

- [ ] Update version in `pylib/__about__.py`
- [ ] Update CHANGELOG.md
- [ ] Run tests locally: `pytest test/ -v`
- [ ] Run linting: `ruff check .`
- [ ] Commit and push all changes
<!-- 
- [ ] Create git tag: `git tag v0.X.Y`
- [ ] Push tag: `git push origin v0.X.Y`
 -->
- [ ] [Create GitHub release](https://github.com/OoriData/Amara/releases/new) (triggers publish workflow)
- [ ] Verify package update on PyPI: https://pypi.org/project/Amara/

## Testing the Package

After publishing, test the installation:

```bash
# Create a fresh virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from PyPI
pip install amara

# Test import
python -c "import amara; print(amara.__version__)"

# Test basic functionality
python -c "
from amara.iri import I
from amara.uxml import parse

# Test IRI processing
url = I('http://example.org/path/to/resource')
print(f'IRI scheme: {url.scheme}')
print(f'IRI host: {url.host}')

# Test XML parsing
xml_text = '<root><item id=\"1\">Hello</item></root>'
doc = parse(xml_text)
print(f'Root element: {doc.xml_name}')
print(f'First child: {doc.xml_children[1].xml_name}')
"
```

# Initial Project Setup

Historical, and to inform maintenance. GitHub Actions & PyPI publishing.

## GitHub Actions Setup

The repository includes two workflows:

### 1. CI Workflow (`.github/workflows/main.yml`)

Runs automatically on every push and pull request. It:
- Tests on Python 3.12 and 3.13
- Runs ruff linting and black formatting checks
- Runs pytest test suite

### 2. Publish Workflow (`.github/workflows/publish.yml`)

Runs when you create a new GitHub release. It builds and publishes to PyPI.

## PyPI Trusted Publishing Setup

###  PyPI Setup

- Login your [PyPI](https://pypi.org) account
- For new package:
    - Go to: https://pypi.org/manage/account/publishing/
    - Click "Add a new pending publisher"
    - Fill in:
    - **PyPI Project Name**: `Amara` (must match `name` in `pyproject.toml`, with case)
    - **Owner**: `OoriData`
    - **Repository name**: `Amara`
    - **Workflow name**: `publish.yml`
    - **Environment name**: `pypi` (PyPI's recommended name)
- If the package already exists on PyPI:
    - Go to the project page: https://pypi.org/manage/project/Amara/settings/publishing/
    - Add the publisher configuration as above

### GitHub Setup
- Go to: https://github.com/OoriData/Amara/settings/environments
- Click "New environment"
- Name: `pypi`
- Click "Configure environment"
- (Optional) Add protection rules:
    - Required reviewers: Add yourself to require manual approval before publishing
    - Wait timer: Add a delay (e.g., 5 minutes) before publishing
- Click "Save protection rules"

### Note on using the environment name

Using an environment name (`pypi`) adds an extra layer of protection, with rules such as required reviewers (manual approval before publishing), wait timers (delay before publishing) and branch restrictions. Without an environment stipulation the workflow runs automatically when a release is created.

## First Time Publishing

Option on the very first release to PyPI: may want to do a manual publish to ensure everything is set up correctly:

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# For some reason, the wheel only seems to work if you build first without then with `-w`
python -m build -w

# Basic build check
twine check dist/*

# Extra checking (replace VERSION with actual version)
VERSION=4.0.3 pip install --force-reinstall -U dist/Amara-$VERSION-py3-none-any.whl
python -c "from amara.iri import I; from amara.uxml import parse; print('Import successful')"

# Upload to Test PyPI first (optional but recommended)
twine upload --repository testpypi dist/*
# Username: __token__
# Password: your-test-pypi-token

# If test looks good, upload to real PyPI
twine upload dist/*
# Username: __token__
# Password: your-pypi-token
```

After the first manual upload, you can use trusted publishing for all future releases.

## Troubleshooting

### "Project name 'Amara' is not valid"
- Check that the name in `pyproject.toml` matches exactly (currently `Amara`)
- Names are case-insensitive but must match what you registered on PyPI

### "Invalid or non-existent authentication information"
- For trusted publishing: Double-check the repository name, owner, and workflow name
- For token auth: Make sure the token is saved as `PYPI_API_TOKEN` in GitHub secrets

### Workflow fails with "Resource not accessible by integration"
- Make sure the workflow has `id-token: write` permission
- Check that the repository settings allow GitHub Actions

### Package version already exists
- You can't overwrite versions on PyPI
- Increment the version in `pylib/__about__.py` and create a new release

## Additional Resources

- [PyPI Trusted Publishing Guide](https://docs.pypi.org/trusted-publishers/)
- [GitHub Actions for Python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)
- [Python Packaging Guide](https://packaging.python.org/en/latest/)
