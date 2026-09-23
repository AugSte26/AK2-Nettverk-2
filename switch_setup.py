# Importerer pySerial for kommunikasjon over seriellport
import serial

# Importerer time for å legge inn pauser mellom
import time

# Henter inn nødvendige verdier fra brukeren
port = input("Seriell port (f.eks COM3 eller /dev/ttyUSB0): ")
hostname = input("Hostname: ")
username = input("SSH brukernavn: ")
password = input("SSH passord: ")
enable_secret = input("Enable secret: ")
domain = input("Domain name: ")

# Liste med Cisco IOS-kommandoer som skal sendes til switchen
commands = [
    "enable",
    "configure terminal",
    f"hostname {hostname}",
    f"ip domain-name {domain}",
    "crypto key generate rsa",
    "1024",
    f"username {username} privilege 15 secret {password}",
    f"enable secret {enable_secret}",
    "line vty 0 15",
    "login local",
    "transport input ssh",
    "exit",
    "ip ssh version 2",
    "end",
    "write memory"
]

# Oppretter forbindelse til seriellporten
ser = serial.Serial(port, 9600, timeout=1)

# Sender kommandoene en etter en
for cmd in commands:
    ser.write((cmd + "\n").encode())
    time.sleep(2)

# Lukker seriellforbindelsen
ser.close()

# Skriver ut bekreftelse når jobben er ferdig
print("SSH konfigurert på switch.")
