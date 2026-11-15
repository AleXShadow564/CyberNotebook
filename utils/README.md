# Utilities

The `utils/` directory contains small, reusable components shared by scripts and
experiments across CyberNotebook.

Its purpose is to keep common functionality in one place instead of duplicating
the same implementation in multiple files. Utilities should remain focused,
reasonably independent, and useful in more than one context.

## What belongs here

Add a module to this directory when it:

- provides functionality that can be reused by multiple scripts or labs;
- has a clear, limited responsibility;
- does not depend on one specific machine, challenge, or write-up;
- can be understood and maintained independently.

Keep one-off scripts, lab-specific exploit code, and material that only makes
sense in a particular exercise alongside that exercise rather than here.

## Current modules

| Module | Purpose |
|---|---|
| [`badges.py`](badges.py) | Provides consistent, colorized status markers for terminal output, such as errors, information, success, and warnings. |

This list should be updated whenever a reusable module is added or its
responsibility changes.

## Usage

Import a utility from the repository root using its module path. For example:

```python
from utils.badges import errore, informazione, successo, avvertimento

print(errore())
print(informazione())
print(successo())
print(avvertimento())
```

Run scripts from the repository root, or make sure the repository root is
available on Python's import path.

## Maintenance guidelines

- Give each module one clear responsibility and use descriptive names.
- Avoid introducing dependencies when the standard library is sufficient.
- Document third-party dependencies and any relevant setup requirements.
- Keep utilities independent of individual lab targets and local machine state.
- Prefer clear interfaces and predictable return values.
- Update this document when adding, removing, or materially changing a utility.

Utilities are shared building blocks, not a general-purpose framework. Keep this
directory small and practical.
