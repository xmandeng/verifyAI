# Pastel

## Development Environment Setup

This project uses Python 3.11.8 with `pyenv` for Python version management and Poetry for dependency management. Follow these instructions to set up your development environment.

### Prerequisites

- [pyenv](https://github.com/pyenv/pyenv) for Python version management
- [poetry](https://python-poetry.org) for dependency management
- [git](https://git-scm.com) for version control

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone git@github.com:xmandeng/pastel.git
   cd pastel
   ```

2. **Install Python 3.11.8 using pyenv**

   ```bash
   pyenv install 3.11.8
   ```

3. **Set local Python version for the project**

   ```bash
   pyenv local 3.11.8
   ```

4. **Install Poetry and upgrade pip**

   ```bash
   pip install poetry
   pip install --upgrade pip
   ```

5. **Configure Poetry to use the pyenv Python environment and set up virtualenv options**

   ```bash
   poetry env use $(pyenv which python)
   poetry config virtualenvs.create true
   poetry config virtualenvs.in-project true
   ```

6. **Install project dependencies**

   ```bash
   poetry install
   ```

7. **Install `pre-commit`**

   ```bash
   pre-commit install
   ```

### VS Code Integration

To configure VS Code to use this environment:

1. Open VS Code and install the Python extension if you haven't already

2. Open the Command Palette (Ctrl+Shift+P / Cmd+Shift+P)

3. Search for "Python: Select Interpreter"

4. Select the Poetry environment (it should be listed, typically with a path containing `.venv`)

5. VS Code should now use your Poetry-managed virtual environment for IntelliSense, running code, and debugging

### Using the Environment

- Run commands within the Poetry environment:
  ```bash
  poetry run python your_script.py
  ```

- Or run a new shell with the virtual environment activated:
  ```bash
  poetry run bash  # or zsh, etc.
  ```

## Project Overview

[Add information about what your project does here]

## License

[Add license information here]
