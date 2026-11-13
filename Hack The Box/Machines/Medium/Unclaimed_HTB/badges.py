import colorama

# "colorama.Fore.COLORE" dà il colore al testo
# "colorama.Fore.RESET" fa ritornare il colore allo stile originale

def errore():
    err=f"[{colorama.Fore.RED}X{colorama.Fore.RESET}]"
    return err

def informazione():
    info=f"[{colorama.Fore.LIGHTBLUE_EX}*{colorama.Fore.RESET}]"
    return info

def successo():
    ok=f"[{colorama.Fore.GREEN}+{colorama.Fore.RESET}]"
    return ok

def avvertimento():
    warning=f"[{colorama.Fore.YELLOW}!{colorama.Fore.RESET}]"
    return warning

# main di prova
def main():

    print(errore())
    print(informazione())
    print(successo())
    print(avvertimento())

if __name__=='__main__':
    main()