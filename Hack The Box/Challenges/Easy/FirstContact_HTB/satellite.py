from skyfield.api import load,EarthSatellite,wgs84
from datetime import timedelta
import pwn

def PrevisioneSatellite(tle1,tle2,lat,long):
    ts=load.timescale()
    satellite=EarthSatellite(tle1,tle2,"DIGITWIN HTB",ts)
    stazione=wgs84.latlon(latitude_degrees=lat,longitude_degrees=long)
    inizio=satellite.epoch
    fine=ts.from_datetime(inizio.utc_datetime()+timedelta(hours=24))
    [tempi,eventi]=satellite.find_events(stazione,inizio,fine,altitude_degrees=30)
    lista_date=[]
    attendi_tramonto=False
    for t,ev in zip(tempi,eventi):
        #print(t.utc_datetime().strftime("%d/%m/%Y - %H:%M:%S"))
        if ev==0 and not attendi_tramonto:
            lista_date.append(t.utc_iso())
            attendi_tramonto = True
        elif ev==2 and attendi_tramonto:
            lista_date.append(t.utc_iso())
            attendi_tramonto = False
    return lista_date

def EstrazioneDati(risposta):
    for riga in risposta.split("\n"):
        if riga.startswith("1"):
            riga_1=riga.strip()
        if riga.startswith("2"):
            riga_2=riga.strip()
        if "(Lat,Long):" in riga:
            testo_numeri = riga.split(":")[1]
            parti_coordinate = testo_numeri.split(",")
            latitudine=float(parti_coordinate[0].strip())
            longitudine=float(parti_coordinate[1].strip())
    return riga_1,riga_2,latitudine,longitudine

def main():
    ip='154.57.164.81'
    porta=32648

    try:
        r=pwn.remote(ip,porta)

        for i in range(3):
            risposta=r.recvuntil(b"When will it be visible next?>").decode()
            print(risposta)
            [riga_1,riga_2,latitudine,longitudine]=EstrazioneDati(risposta=risposta)
            esito=PrevisioneSatellite(riga_1,riga_2,latitudine,longitudine)
            risposta_stringa=" ".join(esito)
            r.sendline(risposta_stringa.encode())
        print(r.recvall().decode())

        r.close()

    except:
        print("ERRORE")

if __name__=='__main__':
    main()