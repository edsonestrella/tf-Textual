# Contributing to tf-textual

We love your input! We want to making contributing to tf-textual as easy and transparent as possible.

## Development Setup

1. Fork the repo
2. Clone your fork:
```bash
git clone https://github.com/edsonestrella/tf-Textual
cd tf-textual
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Set up pre-commit hooks:
```bash
pre-commit install
```
## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Ensure tests pass: `pytest`
4. Run code quality checks: `black src/ && ruff check src/ && mypy src/`
5. Update documentation if needed
6. Submit a pull request

## Code Style

- Use Black for formatting (88 character line length)
- Use Ruff for linting
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Add tests for new features
- Keep functions focused and single-purpose

## Testing

- Write tests for new functionality
- Ensure all tests pass: `pytest`
- Include both unit tests and integration tests where appropriate
- Test with different Terraform versions if possible

## Documentation

- Update README.md for user-facing changes
- Add docstrings for all new functions and classes
- Include examples for new features
- Update type hints if function signatures change

## Reporting Bugs

Use the GitHub issue tracker with this information:

- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Terraform version and platform details
- Python version
- Relevant error messages or logs

## Feature Requests

We welcome feature ideas! Please include:

- The problem you're trying to solve
- Your proposed solution
- Any alternative approaches considered
- Use cases or examples

## Project Structure

```
tf-textual/
├── src/tf_textual/
│   ├── app.py          # Main application
│   ├── __init__.py     # Package metadata
│   └── __main__.py     # CLI entry point
├── tests/              # Test files
├── examples/           # Usage examples
└── docs/               # Documentation
```

## Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

## Release Process

1. Update version in `src/tf_textual/__init__.py`
2. Update CHANGELOG.md
3. Create a release tag
4. Build and publish to PyPI

## Getting Help

- Join our discussions in GitHub Issues
- Check existing documentation
- Look at similar issues or pull requests

## Code Review Guidelines

- All submissions require review
- Reviewers should check for:
  - Code quality and style
  - Functionality and edge cases
  - Test coverage
  - Documentation updates
- Be constructive and respectful in reviews

## Credits

### Core Contributors
- **[Your Name]** - Project lead and main developer
- **Claude from Anthropic** - AI assistant and co-architect

### Special Thanks
- The Textual team for the amazing TUI framework
- The Terraform community for inspiration
- All our users and contributors

Thank you for helping make tf-textual better! 🚀

---

*This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).*