# Contributing to NOVA AI

First off, thank you for considering contributing to **NOVA AI**! It is contributions like yours that make the open-source community an amazing place to learn, inspire, and create.

---

## 📜 Code of Conduct

By participating in this project, you agree to maintain a polite, inclusive, and professional environment for everyone. Please respect all contributors regardless of experience level.

---

## 🚀 How to Contribute

### 1. Reporting Bugs
- Search existing GitHub Issues before opening a new one to avoid duplicates.
- If you find a new bug, open an Issue using the **Bug Report** template.
- Include OS details, Python version, steps to reproduce, and relevant logs from `logs/assistant.log`.

### 2. Suggesting Features
- Open an Issue with the tag `enhancement`.
- Describe the feature clearly and explain why it would be beneficial to users.

### 3. Pull Request Process
1. **Fork the Repository**: Create your own fork of `nova-ai-voice-assistant`.
2. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/amazing-new-feature
   ```
3. **Set Up Environment & Dependencies**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. **Make Your Changes**:
   - Follow PEP 8 guidelines for Python code style.
   - Keep modules decoupled and follow single-responsibility design.
   - Do not commit API keys or personal credentials (`.env` is gitignored).
5. **Commit Your Changes**:
   ```bash
   git commit -m "feat(module): add amazing new feature"
   ```
6. **Push to Your Fork**:
   ```bash
   git push origin feature/amazing-new-feature
   ```
7. **Submit a Pull Request**: Open a PR against the `main` branch of the original repository.

---

## 🎨 Coding Standards

- **PEP 8 Compliance**: Follow Python PEP 8 style conventions (4 spaces indentation, snake_case function/variable names).
- **Docstrings & Comments**: Provide clear docstrings for all top-level module functions.
- **Error Handling**: Use explicit `try-except` blocks and log exceptions using `logger_mod.log_error()`.
- **Fallback Mechanisms**: Always provide local/offline fallbacks for web API integrations.

Thank you for helping build NOVA AI! 🌟
