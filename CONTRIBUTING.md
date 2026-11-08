# Contributing

This repository is a personal cybersecurity research portfolio. Contributions and refactors should improve clarity, reproducibility, safety, and technical accuracy.

## Before submitting

- Confirm that all testing is limited to an authorized lab or environment.
- Remove credentials, API keys, cookies, private keys, personal IP addresses, and other sensitive data.
- Replace machine-specific values with command-line arguments, environment variables, or clearly documented configuration.
- Add dependencies and tested versions where practical.
- Include timeouts and meaningful error handling in network scripts.
- Explain destructive operations and their impact.
- Do not disable TLS verification unless a lab-specific reason is documented.

## Python conventions

- Target a documented Python version.
- Use a virtual environment.
- Keep dependencies explicit; pin versions when reproducibility requires it.
- Prefer `argparse` for command-line configuration.
- Use `logging` instead of unexplained print-heavy output in reusable tools.
- Catch specific exceptions and return useful error messages.
- Add a short usage example and expected output (with sensitive values redacted).

## Machine write-ups

Use [docs/templates/MACHINE-WRITEUP.md](docs/templates/MACHINE-WRITEUP.md). A good write-up records:

1. Scope and lab context
2. Reconnaissance and enumeration
3. Findings and evidence
4. Initial access and privilege escalation
5. Root cause and lessons learned
6. References and cleanup notes

Do not publish flags, credentials, or personal data unless publication is explicitly permitted by the relevant platform and the content is appropriate for this portfolio.

## Commit messages

Use concise, imperative messages with a category prefix:

- `docs: improve Nimbus write-up`
- `fix: handle connection timeout`
- `refactor: make callback configurable`
- `chore: update development dependencies`

Keep changes focused and explain non-obvious decisions in the commit or pull request.
