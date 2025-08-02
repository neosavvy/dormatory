# Contributing to DORMATORY

Thank you for your interest in contributing to DORMATORY! This document provides guidelines for contributing to the project.

## Getting Started

### Forking the Repository

1. **Fork the repository** on GitHub by clicking the "Fork" button at the top right of the [DORMATORY repository page](https://github.com/your-username/dormatory).

2. **Clone your fork** to your local machine:
   ```bash
   git clone https://github.com/your-username/dormatory.git
   cd dormatory
   ```

3. **Add the original repository as upstream**:
   ```bash
   git remote add upstream https://github.com/original-owner/dormatory.git
   ```

4. **Create a new branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   # or for bug fixes:
   git checkout -b fix/your-bug-description
   ```

## Development Setup

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install project dependencies**:
   ```bash
   uv sync
   ```

3. **Activate the virtual environment**:
   ```bash
   uv shell
   ```

4. **Run tests** (when implemented):
   ```bash
   uv run pytest
   ```

## Making Changes

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code style
- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add hierarchical data storage functionality
fix: resolve issue with parent-child relationship queries
docs: update README with installation instructions
test: add unit tests for data validation
```

### Pull Request Process

1. **Ensure your code works**:
   - Run the test suite: `uv run pytest`
   - Check for linting issues: `uv run ruff check .`
   - Verify the project builds: `uv run python -m build`

2. **Update documentation** if your changes affect:
   - User-facing APIs
   - Installation or setup procedures
   - Configuration options

3. **Create a pull request**:
   - Use a descriptive title
   - Include a detailed description of your changes
   - Reference any related issues
   - Add screenshots or examples if applicable

4. **Keep your fork updated**:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

## Issue Reporting

When reporting issues, please include:

- **Description**: Clear description of the problem
- **Steps to reproduce**: Detailed steps to reproduce the issue
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Environment**: OS, Python version, uv version
- **Additional context**: Any other relevant information

## Feature Requests

When requesting features:

- **Describe the use case**: Why is this feature needed?
- **Propose a solution**: How should it work?
- **Consider alternatives**: Are there existing ways to achieve this?
- **Provide examples**: Show how the feature would be used

## Code of Conduct

- Be respectful and inclusive
- Focus on the code and technical discussions
- Help others learn and grow
- Report any inappropriate behavior to maintainers

## Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check the README and inline code comments

## License

By contributing to DORMATORY, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to DORMATORY! 🏠 