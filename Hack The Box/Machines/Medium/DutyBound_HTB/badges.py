"""Compatibilita' con gli script che importano ancora `badges` localmente."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

_shared_path = Path(__file__).resolve().parents[2] / "common" / "badges.py"
_spec = spec_from_file_location("_shared_badges", _shared_path)
_shared = module_from_spec(_spec)
_spec.loader.exec_module(_shared)

errore = _shared.errore
informazione = _shared.informazione
successo = _shared.successo
avvertimento = _shared.avvertimento

if __name__ == "__main__":
    _shared.main()
