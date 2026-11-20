import colorama

# "colorama.Fore.COLORE" dà il colore al testo
# "colorama.Fore.RESET" fa ritornare il colore a quello di default
# "colorama.Style.RESET_ALL" resetta tutto: colore,stile e colore di sfondo

# simboli colorati
def simbolo_errore():
    simbolo_err=f"{colorama.Style.BRIGHT}{colorama.Fore.RED}[X]{colorama.Style.RESET_ALL}"
    return simbolo_err

def simbolo_informazione():
    simbolo_info=f"{colorama.Style.BRIGHT}{colorama.Fore.LIGHTBLUE_EX}[*]{colorama.Style.RESET_ALL}"
    return simbolo_info

def simbolo_successo():
    simbolo_ok=f"{colorama.Style.BRIGHT}{colorama.Fore.GREEN}[+]{colorama.Style.RESET_ALL}"
    return simbolo_ok

def simbolo_avvertimento():
    simbolo_warning=f"{colorama.Style.BRIGHT}{colorama.Fore.YELLOW}[!]{colorama.Style.RESET_ALL}"
    return simbolo_warning

# funzioni per i messaggi
def errore(msg):
    err=f"{simbolo_errore()} {msg}"
    print(err)

def informazione(msg):
    info=f"{simbolo_informazione()} {msg}"
    print(info)

def successo(msg):
    ok=f"{simbolo_successo()} {msg}"
    print(ok)

def avvertimento(msg):
    warning=f"{simbolo_avvertimento()} {msg}"
    print(warning)

# main di prova
def main():

    print(f"simbolo di errore: {simbolo_errore()}")
    print(f"simbolo di informazione: {simbolo_informazione()}")
    print(f"simbolo di successo: {simbolo_successo()}")
    print(f"simbolo di avvertimento: {simbolo_avvertimento()}")

    errore("messaggio di errore")
    informazione("messaggio di informazione")
    successo("messaggio di successo")
    avvertimento("messaggio di avvertimento")

if __name__=='__main__':
    main()
