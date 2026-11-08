# Diario — Cybersecurity Research & Automation

A technical knowledge base documenting hands-on cybersecurity labs, Hack The Box exercises, Linux troubleshooting, and Python automation.

> **Purpose:** demonstrate a repeatable methodology for security research, exploitation in authorized lab environments, technical documentation, and automation.

## Repository map

| Area | Description |
|---|---|
| `Hack The Box/` | Machine and challenge notes from authorized HTB labs |
| `Parrot OS/` | Linux configuration, drivers, and troubleshooting notes |
| `docs/` | Documentation standards and reusable write-up templates |
| `tools/` | Reusable utilities and automation (as they are extracted from individual notes) |

The existing material is being progressively standardized. Paths and naming may evolve as the repository is refactored.

## What you will find

- **Practical security research:** reconnaissance, enumeration, vulnerability analysis, exploitation, and post-exploitation notes in intentionally vulnerable lab environments.
- **Python automation:** scripts supporting repeatable testing and analysis.
- **Linux administration:** setup and troubleshooting notes for Parrot OS and related tooling.
- **Technical documentation:** commands, observations, evidence, lessons learned, and remediation context where applicable.

## Standards

New and updated contributions should:

1. State the lab, scope, assumptions, and prerequisites.
2. Separate observed facts from hypotheses.
3. Explain why a technique works, not only which command to run.
4. Keep target addresses, callback endpoints, credentials, and local paths configurable.
5. Avoid committing secrets, tokens, session cookies, or personal infrastructure details.
6. Include dependency and execution instructions.
7. Clearly label destructive actions and restrict testing to systems for which authorization exists.

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and the [machine write-up template](docs/templates/MACHINE-WRITEUP.md).

## Responsible use

All exploitation material is provided for education and authorized security testing only. Use it exclusively in Hack The Box, intentionally vulnerable environments, or systems for which you have explicit permission. Do not use these materials to access, disrupt, or damage systems without authorization.

## Language

The repository contains notes primarily written in Italian. New documentation may be written in English to improve accessibility, while preserving original Italian material where translation would add little value.

## Status

This is an evolving research portfolio. Existing notes are being reviewed for reproducibility, safe configuration, dependency clarity, and consistent documentation.

---
