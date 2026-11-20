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
| [`badges.py`](badges.py) | Defines colorized terminal status symbols and helper functions to print error, information, success, and warning messages. |

This list should be updated whenever a reusable module is added or its
responsibility changes.

## `badges.py`

The module uses [Colorama](https://pypi.org/project/colorama/) to format terminal
output with bright, colored markers. Install the dependency with:

```bash
pip install colorama
```

### Symbol functions

These functions return a formatted string containing the marker and the
terminal color/reset codes; they do not print anything themselves.

| Function | Marker | Color | Description |
|---|---|---|---|
| `simbolo_errore()` | `[X]` | Red | Error |
| `simbolo_informazione()` | `[*]` | Light blue | Information |
| `simbolo_successo()` | `[+]` | Green | Success |
| `simbolo_avvertimento()` | `[!]` | Yellow | Warning |

### Message functions

These functions accept a message string, prepend the corresponding symbol,
and print the result to the terminal. They do not return a message string.

| Function | Signature | Output |
|---|---|---|
| `errore` | `errore(msg)` | Red `[X]` followed by the message |
| `informazione` | `informazione(msg)` | Light-blue `[*]` followed by the message |
| `successo` | `successo(msg)` | Green `[+]` followed by the message |
| `avvertimento` | `avvertimento(msg)` | Yellow `[!]` followed by the message |

### Example

```python
from utils import badges

# Print a complete message with its status marker.
badges.errore("messaggio di errore")
badges.informazione("messaggio di informazione")
badges.successo("messaggio di successo")
badges.avvertimento("messaggio di avvertimento")

# Or retrieve a marker to compose custom output.
print(f"{badges.simbolo_successo()} Operazione completata")
```

Running `badges.py` directly executes its built-in demonstration: it prints
each standalone symbol and then one example message for each status.

## Maintenance guidelines

- Give each module one clear responsibility and use descriptive names.
- Avoid introducing dependencies when the standard library is sufficient.
- Document third-party dependencies and any relevant setup requirements.
- Keep utilities independent of individual lab targets and local machine state.
- Prefer clear interfaces and predictable return values.
- Update this document when adding, removing, or materially changing a utility.

Utilities are shared building blocks, not a general-purpose framework. Keep this
directory small and practical.
