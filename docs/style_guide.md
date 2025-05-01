# Documentation Style Guide

This guide provides standards for creating and maintaining documentation in the SmartSense project. Following these guidelines ensures consistency across our documentation and makes it easier for contributors to create and update documentation.

## Version: 1.0.0 (May 2025)

## Table of Contents

- [General Principles](#general-principles)
- [File Organization](#file-organization)
- [Formatting Standards](#formatting-standards)
- [Code Examples](#code-examples)
- [Images and Diagrams](#images-and-diagrams)
- [Versioning](#versioning)

## General Principles

### Voice and Tone

- Use clear, concise language
- Write in present tense
- Use active voice
- Be inclusive and respectful
- Address the reader directly using "you"

### Documentation Structure

Each document should include:

1. Title
2. Version number and last update date
3. Brief introduction/purpose
4. Table of contents (for documents longer than 2 screens)
5. Main content
6. Related resources (if applicable)

## File Organization

### File Naming

- Use lowercase letters
- Separate words with underscores
- Be descriptive but concise
- Example: `getting_started.md`, `api_reference.md`

### Directory Structure

```
docs/
├── images/             # Images and diagrams
├── api/                # API documentation
├── guides/             # User guides
└── reference/          # Reference documentation
```

## Formatting Standards

### Markdown Usage

- Use ATX-style headers (`#` syntax)
- Use fenced code blocks with language specification
- Use reference-style links for better maintainability
- Use tables for structured data

### Code Examples

```python
# Use descriptive examples
from smartsense import SensorNetwork

# Initialize network
network = SensorNetwork(name="Example Network")

# Add sensors
network.add_sensor(TemperatureSensor(name="Room Temp"))
```

### Admonitions

Use the following admonition styles:

> **Note:** For additional information

> **Warning:** For potential pitfalls

> **Tip:** For helpful suggestions

## Images and Diagrams

- Store images in docs/images/
- Use descriptive filenames
- Include alt text for accessibility
- Optimize images for web viewing
- Use SVG format for diagrams when possible

## Code Blocks

### Python Examples

```python
def example_function():
    """Docstring following Google style."""
    return True
```

### Configuration Examples

```yaml
# Configuration example
sensors:
  temperature:
    type: TemperatureSensor
    interval: 60
```

## API Documentation

### Method Documentation

```python
def method_name(param1: str, param2: int) -> bool:
    """Short description.

    Extended description of method.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: Description of when this error occurs
    """
    pass
```

## Versioning

### Version Numbers

Use semantic versioning for documentation:

- MAJOR.MINOR.PATCH (e.g., 1.0.0)
- Update version when making significant changes

### Change Documentation

- Maintain a changelog for documentation
- Note significant changes in release notes
- Include update dates in documents

## Links and References

### Internal Links

- Use relative paths for internal links
- Include anchor links for sections
- Verify links during documentation review

### External Links

- Use reference-style links
- Include link checking in CI pipeline
- Document required permissions for API endpoints

## Reviews and Updates

### Documentation Review

- Peer review all documentation changes
- Check for technical accuracy
- Verify formatting and style compliance
- Test code examples

### Regular Updates

- Review documentation quarterly
- Update version numbers appropriately
- Archive outdated documentation
- Update examples with new features

## Community Contributions

### Contributing Guidelines

- Follow project CONTRIBUTING.md
- Use pull request templates
- Include documentation in feature PRs
- Update relevant docs during code changes

## Best Practices

1. Keep documentation close to code
2. Update docs with code changes
3. Use clear, consistent terminology
4. Include examples for complex features
5. Consider international audiences

## Terms and Conventions

- Use consistent capitalization
- Define acronyms on first use
- Maintain a glossary for technical terms
- Follow SmartSense naming conventions

---

Last updated: May 1, 2025
