# Contributing to SmartSense

First off, thank you for considering contributing to SmartSense! It's people like you that make SmartSense such a great tool. We welcome contributions from everyone, whether it's a bug report, feature suggestion, code improvement, or documentation enhancement.

This document provides guidelines and instructions for contributing to the SmartSense project. Following these guidelines helps maintain code quality and streamlines the contribution process.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [Development Environment Setup](#development-environment-setup)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Security Policy](#security-policy)
- [Community Guidelines](#community-guidelines)

## Code of Conduct

By participating in this project, you are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md). Please report unacceptable behavior to the project maintainers.

## Ways to Contribute

There are many ways to contribute to SmartSense:

### Reporting Bugs

When reporting bugs, please include:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior and what actually happened
- SmartSense version and Python version
- Any relevant logs or error messages

Use the GitHub issue tracker with the "bug" label.

### Suggesting Features

Feature suggestions are always welcome! Please provide:

- A clear description of the feature
- Why this feature would be beneficial
- Any relevant examples or use cases

Use the GitHub issue tracker with the "enhancement" label.

### Code Contributions

We welcome code contributions through pull requests. Before writing code, please:

1. Check existing issues and pull requests to avoid duplicating work
2. For significant changes, open an issue first to discuss your approach
3. Follow the coding standards and testing requirements

### Documentation Improvements

Documentation is crucial for any project. Improvements can include:

- Fixing typos or clarifying existing documentation
- Adding examples or tutorials
- Translating documentation to other languages
- Creating diagrams or visual aids

## Development Environment Setup

Follow these steps to set up your development environment:

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/SmartSense.git
   cd SmartSense
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
5. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Coding Standards

We follow these coding standards to maintain code quality and consistency:

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) standards
- Use [Google's docstring format](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Maximum line length is 88 characters (compatible with Black)
- Use type hints for all function parameters and return values

### Code Formatting

We use the following tools to enforce code style:

- [Black](https://black.readthedocs.io/) for code formatting
- [isort](https://pycqa.github.io/isort/) for import sorting
- [flake8](https://flake8.pycqa.org/) for style guide enforcement
- [mypy](https://mypy.readthedocs.io/) for type checking

You can run all these tools with pre-commit:

```bash
pre-commit run --all-files
```

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests after the first line
- Consider using the following prefixes:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation changes
  - `test:` for test-related changes
  - `refactor:` for refactoring existing code
  - `style:` for formatting changes
  - `chore:` for routine tasks and maintenance

## Testing Requirements

All code contributions must include appropriate tests:

- Write unit tests for all new functionality
- Ensure all tests pass before submitting a pull request
- Aim for at least 90% test coverage for new code
- Run the test suite with:
  ```bash
  pytest
  ```
- For coverage report:
  ```bash
  pytest --cov=src/smartsense --cov-report=term
  ```

## Pull Request Process

1. **Branch naming**: Use a descriptive branch name following this pattern:
   - `feature/short-description` for new features
   - `bugfix/issue-description` for bug fixes
   - `docs/description` for documentation-only changes
   - `refactor/description` for refactoring

2. **Keep changes focused**: Each PR should address a single concern. If you have multiple unrelated changes, submit separate PRs.

3. **Submit your PR**: Fill out the PR template completely, including:
   - A clear description of what the PR does
   - Any related issues it addresses (use "Fixes #123" or "Relates to #123")
   - Changes you made
   - How to test the changes

4. **Code review process**:
   - Maintainers will review your code and may suggest changes
   - Address any review comments and push additional commits to your branch
   - Once approved, a maintainer will merge your PR

5. **After PR approval**:
   - Your changes will be merged into the main branch
   - You can delete your branch if you want

## Security Policy

### Reporting Security Issues

If you discover a security vulnerability, please do **NOT** open a public issue. Instead:

1. Email us at [security@example.com](mailto:security@example.com) with details
2. Include steps to reproduce the vulnerability
3. Allow time for us to address the issue before disclosing it publicly

We take security issues seriously and will work quickly to address any vulnerabilities.

## Community Guidelines

To foster a positive and inclusive community, please:

- **Be respectful**: Treat everyone with respect and kindness, regardless of their background or experience level
- **Be constructive**: Offer constructive feedback and focus on the ideas, not the person presenting them
- **Stay on topic**: Keep discussions relevant to SmartSense development
- **Help others learn**: If you have expertise, share it with others who are learning
- **Give credit**: Acknowledge others' contributions and ideas
- **Follow the code of conduct**: Adhere to our community standards

### Communication Channels

- **GitHub Issues**: For bug reports, feature requests, and specific technical discussions
- **GitHub Discussions**: For general questions, ideas, and community conversation
- **GitHub Wiki**: For collaborative documentation

## Thank You!

Your contributions to SmartSense help make it better for everyone. We appreciate the time and effort you put into improving this project.

---

This contribution guide was last updated on April 29, 2025.

# Contributing to SmartSense

First off, thank you for considering contributing to SmartSense! It's people like you that make SmartSense such a great tool.

## Code of Conduct

By participating in this project, you are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for SmartSense. Following these guidelines helps maintainers understand your report, reproduce the behavior, and find related reports.

* Use the GitHub issue search — check if the issue has already been reported.
* Check if the issue has been fixed — try to reproduce it using the latest `main` branch.
* Isolate the problem — create a reduced test case and a live example.

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for SmartSense, including completely new features and minor improvements to existing functionality.

* Use the GitHub issue search — check if the enhancement has already been suggested.
* Describe the current behavior and explain which behavior you expected to see instead and why.
* Explain why this enhancement would be useful to most SmartSense users.
* List some other projects where this enhancement exists.

### Pull Requests

* Fill in the required template
* Follow the style guide
* Document new code
* End all files with a newline
* Avoid platform-dependent code

## Style Guides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Consider starting the commit message with an applicable emoji:
   * 🎨 `:art:` when improving the format/structure of the code
   * ⚡️ `:zap:` when improving performance
   * 🔥 `:fire:` when removing code or files
   * 🐛 `:bug:` when fixing a bug
   * 🔒 `:lock:` when dealing with security
   * ⬆️ `:arrow_up:` when upgrading dependencies
   * ⬇️ `:arrow_down:` when downgrading dependencies

### Python Style Guide

* Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Use docstrings following [Google's docstring format](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
* Run `black` and `isort` on your code before committing
* Maintain 100% test coverage for new code

## Development Environment Setup

1. Fork and clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   * Windows: `venv\Scripts\activate`
   * Unix/MacOS: `source venv/bin/activate`
4. Install development dependencies: `pip install -e ".[dev]"`
5. Install pre-commit hooks: `pre-commit install`

## Testing

* Write tests for all new features and bug fixes
* Run the test suite before submitting a PR: `pytest`
* Ensure all tests pass and maintain or improve code coverage

## Documentation

* Update documentation for all new features and changes to existing functionality
* Follow the documentation style guide in `docs/style_guide.md`

## Project Structure

```
SmartSense/
├── docs/               # Documentation
├── src/                # Python source code
│   └── smartsense/     # Main package
├── hardware/           # Hardware designs and schematics
├── tests/              # Test suite
├── .github/            # GitHub specific files
└── ...
```

## Thank You!

Your contributions to open source, large or small, make projects like this possible. Thank you for taking the time to contribute.

