# badges

Modulo condiviso per stampare badge colorati nei messaggi dei tool Python della cartella `Hack The Box/Machines`.

## Funzioni disponibili

| Funzione | Output | Uso |
|---|---|---|
| `errore()` | `[X]` in rosso | Errori |
| `informazione()` | `[*]` in azzurro | Informazioni |
| `successo()` | `[+]` in verde | Operazioni riuscite |
| `avvertimento()` | `[!]` in giallo | Avvisi |

I colori sono gestiti da [Colorama](https://pypi.org/project/colorama/), già elencato in `Hack The Box/requirements.txt`.

## Utilizzo

Gli script già presenti nelle cartelle delle macchine possono continuare a usare:

```python
import badges

print(f"{badges.informazione()} Avvio richiesta...")
print(f"{badges.successo()} Operazione completata")
print(f"{badges.avvertimento()} Controllare i parametri")
print(f"{badges.errore()} Richiesta non riuscita")
```

I file `badges.py` nelle singole cartelle macchina sono piccoli adattatori di compatibilità: inoltrano le chiamate a questo modulo condiviso. In questo modo gli script esistenti non richiedono modifiche e l'implementazione non viene duplicata.

## Dipendenze

Dalla directory `Hack The Box`:

```bash
python3 -m pip install -r requirements.txt
```

## Test rapido

È possibile eseguire direttamente il modulo condiviso:

```bash
python3 "Hack The Box/Machines/common/badges.py"
```
