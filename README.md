# VerifyAI

## Project Overview

This Proof of Concept (PoC) leverages PydanticAI to systematically validate insurance insights by comparing provided statements against supporting evidence. The system evaluates whether claims made about insurance performance metrics are factually accurate based on available data visualizations and tabular information. While this implementation focuses specifically on insurance analytics validation, the approach can be readily extended to other domains requiring factual verification against evidence sources, such as **financial reporting, medical research claims, legal document verification**, or any field where assertions need to be cross-checked against supporting data.

### Architecture

- **PydanticAI**: Type safety, model provider agnosticism, and automatic output coercion to Pydantic models
- **Logfire**: Real-time monitoring of token usage and model interactions
- **Modular validation**: Separate Pydantic models for grammar, premises, and overall assessment, enabling type-safe validation at each stage

### Validation Methodology

We split insights into two key components:
1. The core conclusion
2. Supporting evidence or premises

This approach prevents circular validation where the conclusion validates itself. Each compound statement is atomized into discrete premises, ensuring granular assessment against all available evidence.

### Validation Pipeline

1. Extract and isolate the main conclusion using LLM reasoning
2. Parse remaining text into discrete, testable premises
3. Validate each premise against relevant data sources (LRS data, charts)
4. Perform grammar verification as a parallel process
5. Consolidate all validation results into a comprehensive assessment

When rephrasing premises, we take care to preserve the meaning, ensuring the validation remains true to the original source material.

### Technical Notes

- Architecture natively supports async operations for concurrent validations
- Token usage must be actively managed to control costs
- Ability to change models without refactoring codebase
- Real-time telemetry via Logfire to monitor agent activity and LLM interactions

***

<img width="1278" alt="Screenshot 2025-03-12 at 1 45 50 PM" src="https://github.com/user-attachments/assets/4ba35e2f-a65e-40d7-8e5d-494862621474" />

***


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

## License

No Public License / Internal Use
