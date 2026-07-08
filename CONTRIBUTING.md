# Contributing Guidelines - NetConnect

Thank you for your interest in contributing to NetConnect! We welcome contributions to enhance the Personalized Networking Assistant experience.

---

## 1. Code of Conduct
By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please report any unacceptable behavior to the project maintainers.

---

## 2. Getting Started

1. **Fork the Repository**: Create a personal copy of the repository on GitHub.
2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/your-username/Personalized-Networking-Assistant.git
   cd Personalized-Networking-Assistant
   ```
3. **Set Up Local Environment**: Follow the detailed local developer environment configuration in the [Setup Guide](docs/setup.md).
4. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-awesome-feature
   ```

---

## 3. Standards & Best Practices

- **Python Styling**: We adhere to standard PEP 8 formatting guidelines.
- **Imports**: Re-export models, schemas, and connection functions under package entries (`__init__.py`) where applicable and use absolute package path imports.
- **Testing**: Ensure that you run the unittest suite and that all tests pass before proposing modifications:
  ```bash
  python -m unittest discover -s backend/tests
  ```
  Write test coverage for any new features or endpoints introduced.

---

## 4. Commit Message Guidelines

We use human-readable, conventional style labels for commits to construct logical commit history chains:

- `feat:` A new feature or endpoint.
- `fix:` A bug fix.
- `docs:` Documentation revisions (e.g. updating README or architecture guides).
- `style:` Formatting edits (no code functionality change).
- `refactor:` Code reorganization or restructures that don't add features or fix bugs.
- `test:` Adding or editing unit tests.
- `chore:` Other maintenance updates (e.g. updating dependencies or templates).

Example:
```bash
feat: add custom system temperature setting for Gemini model
```

---

## 5. Submitting Pull Requests

1. Commit and push your changes to your feature branch.
2. Open a Pull Request from your fork against the `main` branch.
3. Complete the description using the [Pull Request Template](.github/pull_request_template.md).
4. Wait for maintainers to review your submissions.
