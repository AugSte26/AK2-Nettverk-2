Cisco SSH Automation med Python og pySerial

## Beskrivelse ##

Dette prosjektet automatiserer oppsett av SSH på Cisco-routere og Cisco-switcher ved hjelp av Python og pySerial.

Konfigurasjonen sendes over konsollporten, noe som gjør det mulig å klargjøre en enhet for SSH selv om nettverksforbindelse ikke er konfigurert enda.

Løsningen består av to Python-skript:

- router_setup.py
- switch_setup.py

Begge skriptene er laget for å være gjenbrukbare ved at nødvendige verdier hentes fra brukeren under kjøring i stedet for å være hardkodet i koden.



## Funksjoner ##

Skriptene utfører følgende oppgaver:

- Setter hostname
- Konfigurerer domenenavn
- Genererer RSA-nøkler
- Oppretter lokal administratorbruker
- Setter enable secret
- Aktiverer SSH versjon 2
- Konfigurerer VTY-linjer for SSH
- Lagrer konfigurasjonen



## Krav ##

Programvare

- Python 3.x
- pySerial
- Visual Studio Code eller annen Python-editor

Maskinvare

- Cisco-router eller Cisco-switch
- Konsollkabel
- PC med USB-port


## Installasjon ##

Installer pySerial:

pip install pyserial