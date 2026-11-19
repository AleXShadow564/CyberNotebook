import colorama

# "colorama.Fore.COLORE" dà il colore al testo
# "colorama.Fore.RESET" fa ritornare il colore a quello di default
# "colorama.Style.RESET_ALL" resetta tutto: colore,stile e colore di sfondo

def errore():
    err=f"{colorama.Style.BRIGHT}{colorama.Fore.RED}[X]{colorama.Style.RESET_ALL}"
    return err

def informazione():
    info=f"{colorama.Style.BRIGHT}{colorama.Fore.LIGHTBLUE_EX}[*]{colorama.Style.RESET_ALL}"
    return info

def successo():
    ok=f"{colorama.Style.BRIGHT}{colorama.Fore.GREEN}[+]{colorama.Style.RESET_ALL}"
    return ok

def avvertimento():
    warning=f"{colorama.Style.BRIGHT}{colorama.Fore.YELLOW}[!]{colorama.Style.RESET_ALL}"
    return warning

# main di prova
def main():

    print(errore())
    print(informazione())
    print(successo())
    print(avvertimento())

if __name__=='__main__':
    main()
